"""Relation-aware generalization: consistent placeholder mapping + deterministic substitution.

The core structural idea, and the difference from the holistic rewrite evaluated
in notebook 07: every extracted entity gets exactly one typed placeholder for the
whole document, and substitution is performed deterministically by string
replacement -- never by trusting an LLM to follow a redaction instruction.
The N=50 holistic evaluation measured instruction-following redaction failing on
~11% of samples; a substitution pass cannot fail that way.

Consistency is what preserves utility while severing identity: the downstream
reader can still tell that Person-A booked the venue and Person-B must confirm,
but cannot tell who Person-A is, which division "an operations division" is, or
link either to anything outside the document.

An optional LLM fluency pass smooths grammar around the substitutions; it is
guarded -- after it runs, every raw entity surface is scrubbed again, so the
fluency model re-introducing a name is caught deterministically.
"""

import json
import re
import string

import requests

from .extraction import EMAIL_REGEX, call_with_retry

# Placeholder vocabularies per entity type. PERSONs get stable letter labels
# (Person-A, Person-B, ...) because distinguishing individuals from each other
# is exactly the utility we want to keep; other types get indefinite generic
# descriptions because their individual identity is the leak, not their count.
_TYPE_TEMPLATES = {
    "PERSON": None,  # handled specially: Person-A, Person-B, ...
    "EMAIL": "[a redacted email address]",
    "ORG": "an internal organizational unit",
    "PROJECT": "an internal initiative",
    "ROLE": "a functional role",
    "LOCATION": "an external location",
}


def build_mapping(entities, relations=None):
    """Assign one placeholder per entity, enriched by relations where possible.

    Returns {entity_text: placeholder}. Persons are lettered in order of
    appearance (Person-A, Person-B, ...). If relations identify a person's role
    (holds_role / works_in style triples), the placeholder carries a generic
    role hint -- "Person-A (a coordinator role)" -- because keeping *that* a
    person has a role, without which role or which person, is retained utility.

    A person's email address maps to their person placeholder, not to a generic
    email placeholder: 'randy.young@gulfsouthpl.com' and 'Randy Young' are the
    same identity and must not generalize to two different things (that split is
    precisely how notebook 07's sample-36 outlier leaked -- the name was redacted
    while the address, carrying both name and employer, survived).
    """
    relations = relations or []
    mapping = {}
    person_labels = {}
    letters = list(string.ascii_uppercase)

    # Role hints from relations: person-entity text (lower) -> role text.
    role_hint = {}
    for rel in relations:
        if rel["rel"] in ("holds_role", "works_as", "has_role", "role_of"):
            role_hint[rel["a"].lower()] = rel["b"]

    # Pass 1: persons, in listed order. Each person maps not just their listed
    # surface but its variants: the comma-inverted form ("Hudson, Todd") and each
    # individual name token of >= 3 chars -- so a stray first or last name in the
    # text still resolves to the same placeholder instead of leaking. Substitution
    # is word-boundary anchored (see apply_mapping), so short-token variants can't
    # corrupt unrelated words.
    persons = [e for e in entities if e["type"] == "PERSON"]
    for i, ent in enumerate(persons):
        label = f"Person-{letters[i % 26]}" if i < 26 else f"Person-{i + 1}"
        hint = role_hint.get(ent["text"].lower())
        placeholder = f"{label} (a functional role)" if hint else label

        surface = ent["text"]
        tokens = [t for t in re.split(r"[\s,]+", surface) if t]
        variants = {surface}
        if len(tokens) >= 2:
            variants.add(", ".join([tokens[-1]] + tokens[:-1]))   # "Last, First..."
            variants.update(t for t in tokens if len(t) >= 3)
        for v in variants:
            mapping.setdefault(v, placeholder)
        person_labels[ent["text"].lower()] = label

    # Pass 2: emails -- inherit the owning person's label when the local part
    # matches a mapped person; otherwise the generic email placeholder.
    from .extraction import _local_part_to_name
    for ent in entities:
        if ent["type"] != "EMAIL":
            continue
        owner = _local_part_to_name(ent["text"])
        label = person_labels.get(owner.lower()) if owner else None
        mapping[ent["text"]] = f"[{label}'s address]" if label else _TYPE_TEMPLATES["EMAIL"]

    # Pass 3: everything else gets its type's generic description. Numbering
    # ("an internal initiative (2)") only when a document has several of a type
    # AND they participate in relations -- otherwise indistinguishability is fine.
    for etype in ("ORG", "PROJECT", "ROLE", "LOCATION"):
        of_type = [e for e in entities if e["type"] == etype]
        for i, ent in enumerate(of_type):
            base = _TYPE_TEMPLATES[etype]
            mapping[ent["text"]] = base if len(of_type) == 1 else f"{base} ({i + 1})"

    return mapping


def apply_mapping(text, mapping):
    """Deterministic substitution: longest entity surface first, case-insensitive,
    boundary-anchored.

    Longest-first ordering prevents partial-overlap corruption (substituting
    'Lynn' inside 'Lynn Blair' before 'Lynn Blair' itself is matched). Anchoring
    prevents short person-name variants from corrupting unrelated words ('Mary'
    must never match inside 'summary').

    Uses lookaround assertions ((?<!\\w) / (?!\\w)), not \\b, because \\b requires
    an actual word/non-word *transition* at the boundary -- it fails whenever the
    entity surface itself starts or ends with a non-word character (e.g. 'Mtg.',
    'Ava-35842/...'). Found live: an entity ending in '.' silently failed to
    substitute AND failed the leak-detection check below (both used \\b), letting
    a raw project identifier survive all the way through to the worst SER
    regression in the N=50 run. Lookaround has no such requirement -- it only
    asserts what's adjacent to *our* match, not a transition on both sides.
    Email surfaces contain '@'/'.' throughout and match unanchored, as before.
    """
    result = text
    for surface in sorted(mapping, key=len, reverse=True):
        if "@" in surface:
            pattern = re.escape(surface)
        else:
            pattern = r"(?<!\w)" + re.escape(surface) + r"(?!\w)"
        result = re.sub(pattern, mapping[surface], result, flags=re.IGNORECASE)
    return result


FLUENCY_PROMPT = """You are a text-smoothing filter. The text you receive has had named
entities replaced with placeholders like "Person-A" or "an internal organizational unit".
Rewrite it minimally so it reads as fluent prose, KEEPING every placeholder exactly as
written. Do not add information, do not remove placeholders, do not guess what any
placeholder stands for. Output only the smoothed text."""


def _fluency_pass(text, ollama_url, model):
    def _call():
        r = requests.post(ollama_url, json={
            "model": model,
            "messages": [{"role": "user", "content": f"{FLUENCY_PROMPT}\n\nTEXT:\n{text}"}],
            "stream": False,
            "options": {"temperature": 0.1},
        }, timeout=120)
        r.raise_for_status()
        return r.json()["message"]["content"]
    return call_with_retry(_call)


def _strip_preamble(text):
    """Drop a conversational lead-in line the fluency model sometimes adds
    despite instructions (observed live: 'Here is the smoothed text:')."""
    lines = text.lstrip().split("\n")
    if lines and re.match(r"(?i)^\s*(here('s| is)|sure|certainly|below is).{0,60}:\s*$", lines[0]):
        return "\n".join(lines[1:]).lstrip()
    return text


def _scrub(text, mapping):
    """Safety net: re-apply the mapping plus a blanket email scrub, so no raw
    entity surface survives regardless of what the fluency model did."""
    text = apply_mapping(_strip_preamble(text), mapping)
    return EMAIL_REGEX.sub("[a redacted email address]", text)


def generalize(text, entities, relations, ollama_url, model, fluency=True):
    """Full relation-aware generalization of one document.

    Returns (generalized_text, mapping). The output is guaranteed to contain no
    raw surface from the mapping table -- asserted here, not left to inspection.
    """
    mapping = build_mapping(entities, relations)
    generalized = apply_mapping(text, mapping)

    if fluency and mapping:
        try:
            smoothed = _fluency_pass(generalized, ollama_url, model)
            generalized = _scrub(smoothed, mapping)
        except Exception as e:
            print(f"    [warn] fluency pass failed ({e}); using raw substitution output")

    # Leak assertion uses the same lookaround boundary rules as apply_mapping,
    # for two reasons found live: (1) a bare surface like "Name" must not be
    # flagged for appearing inside "FileName", and (2) \b specifically (the
    # original anchor here and in apply_mapping) silently fails to match
    # entities ending in punctuation, which let one substitution failure slip
    # past this very assertion undetected -- see apply_mapping's docstring.
    def _still_present(surface):
        if "@" in surface:
            return re.search(re.escape(surface), generalized, re.IGNORECASE)
        return re.search(r"(?<!\w)" + re.escape(surface) + r"(?!\w)", generalized, re.IGNORECASE)

    leaked = [s for s in mapping
              if _still_present(s) and s.lower() not in mapping[s].lower()]
    assert not leaked, f"raw entity surfaces survived generalization: {leaked}"

    return generalized, mapping
