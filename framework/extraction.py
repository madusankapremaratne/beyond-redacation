"""Entity and relation extraction for relation-aware semantic generalization.

Hybrid extraction strategy, motivated by measured failures in the N=50 holistic
evaluation (evaluation/07_Evaluation_Harness_N50.ipynb):

- Deterministic detectors run first: spaCy PERSON entities and an email-address
  regex (the same pattern validation/02 uses, so the notebooks agree on what an
  email is). spaCy alone missed bare first names ("Scott") and some full names
  ("Raetta Zadow"); the regex exists because 07's worst outlier leaked 29 raw
  recipient addresses that no prose-oriented detector considered in scope.
- One structured LLM call to the local edge model then extends and types the
  entity set (PROJECT, ROLE, ORG, LOCATION -- categories spaCy's small model
  can't reliably produce) and catches the names the deterministic pass missed.
- Relation extraction is a second structured LLM call, grounded on the merged
  entity list: the model may only connect entities we already extracted, which
  keeps triples anchored to real text instead of hallucinated endpoints.

All LLM calls go to a local Ollama server -- the defense side of this framework
is meant to be genuinely on-device, not simulated via a hosted API.
"""

import json
import re
import time

import requests
import spacy

# Same pattern as validation/02_Privacy_Baseline_Profiling.ipynb's PII_PROFILES.
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

ENTITY_TYPES = ("PERSON", "ORG", "PROJECT", "ROLE", "LOCATION", "EMAIL")

_NLP = None


def _nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")
    return _NLP


def call_with_retry(fn, max_retries=4, base_delay=2.0):
    """Exponential-backoff wrapper, same discipline as notebook 07."""
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"    [retry] call failed ({e}); backing off {delay:.1f}s...")
            time.sleep(delay)


def _ollama_json(ollama_url, model, system, user, timeout=120):
    def _call():
        r = requests.post(ollama_url, json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.0},
        }, timeout=timeout)
        r.raise_for_status()
        return json.loads(r.json()["message"]["content"])
    return call_with_retry(_call)


def _local_part_to_name(email):
    """Best-effort person-name guess from an email local part.

    'randy.young@gulfsouthpl.com' -> 'Randy Young'. Single-token local parts
    ('jarregu', 'gsuga') are returned title-cased as-is -- they still identify a
    person and must map to a placeholder even if we can't split them nicely.
    """
    local = email.split("@", 1)[0]
    parts = [p for p in re.split(r"[._\-]+", local) if p and not p.isdigit()]
    if not parts:
        return None
    return " ".join(p.capitalize() for p in parts)


ENTITY_EXTRACTION_PROMPT = """You are an entity extraction engine for a privacy system.
From the text you are given, extract every entity of these types:
- PERSON: personal names of people (including bare first names)
- ORG: company, division, department, or team names
- PROJECT: named projects, initiatives, meetings, or events
- ROLE: job titles or role names
- LOCATION: named places, buildings, venues

Output strict JSON: {"entities": [{"text": "...", "type": "PERSON|ORG|PROJECT|ROLE|LOCATION"}, ...]}
Only include entities whose text appears verbatim in the input. Do not invent entities."""


RELATION_EXTRACTION_PROMPT = """You are a relation extraction engine for a privacy system.
You are given a text and a list of entities already extracted from it.
Identify relationships between those entities that the text states or clearly implies.

Use short snake_case relation labels, e.g.: holds_role, works_in, manages, member_of,
organizes, attends, hosted_at, contact_for, vendor_of, client_of, part_of.

Output strict JSON: {"relations": [{"a": "<entity text>", "rel": "<label>", "b": "<entity text>"}, ...]}
Both "a" and "b" MUST be copied exactly from the provided entity list. Do not introduce
new entities. If no relations are evident, output {"relations": []}."""


def _person_key(surface):
    """Canonical dedupe key for person surfaces: 'Maureen.riter', 'Maureen Riter'
    and 'Riter, Maureen' are the same identity and must share one placeholder."""
    tokens = [t for t in re.split(r"[.\s_\-,]+", surface.lower()) if t]
    return " ".join(sorted(tokens))


def extract_entities(text, ollama_url, model):
    """Merged deterministic + LLM entity extraction.

    Returns a list of {"text": str, "type": str} dicts. Person surfaces are
    deduplicated on a normalized token key (so dotted/inverted variants of one
    name collapse into a single identity); other types dedupe case-insensitively.
    Deterministic detections take precedence on type.
    """
    entities = {}  # dedupe key -> {"text", "type"}

    def add(surface, etype):
        # Sanitize quoted-reply artifacts and stray punctuation -- spaCy happily
        # returns spans like "Kirk > >" from '>'-quoted email bodies.
        surface = re.sub(r"[>|]+", " ", surface)
        surface = " ".join(surface.split()).strip("'\" \t,;:")
        if not surface or len(surface) < 2:
            return
        key = _person_key(surface) if etype == "PERSON" else surface.lower()
        if key not in entities:
            entities[key] = {"text": surface, "type": etype}

    # 1. Deterministic: email addresses, and the person names hidden inside them.
    for email in EMAIL_REGEX.findall(text):
        add(email, "EMAIL")
        name = _local_part_to_name(email)
        if name:
            add(name, "PERSON")

    # 2. Deterministic: spaCy PERSON spans.
    for ent in _nlp()(text).ents:
        if ent.label_ == "PERSON":
            add(ent.text, "PERSON")

    # 3. Deterministic: "Lastname, Firstname" header/list forms ("Hudson, Todd").
    #    spaCy and the LLM both miss these reliably; observed leaking live in the
    #    first framework smoke test. Normalized to "Firstname Lastname" so the
    #    person-key dedupe merges them with any other surface of the same name.
    #    Over-catching here errs toward over-redaction, which is the safe side --
    #    except calendar words: "Wednesday, September" matched this pattern live
    #    and turned a date into a person placeholder, hence the stoplist.
    calendar = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
                "sunday", "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"}
    for last, first in re.findall(r"\b([A-Z][a-z]{2,}), ([A-Z][a-z]{2,})\b", text):
        if last.lower() in calendar or first.lower() in calendar:
            continue
        add(f"{first} {last}", "PERSON")

    # 4. LLM pass: extend and type the set (fills spaCy's known recall gaps and
    #    the categories it can't produce). Failures degrade gracefully -- the
    #    deterministic entities above still stand.
    try:
        result = _ollama_json(ollama_url, model, ENTITY_EXTRACTION_PROMPT, text)
        for ent in result.get("entities", []):
            surface = str(ent.get("text", "")).strip()
            etype = str(ent.get("type", "")).strip().upper()
            if etype in ENTITY_TYPES and surface and surface.lower() in text.lower():
                add(surface, etype)
    except Exception as e:
        print(f"    [warn] LLM entity pass failed ({e}); using deterministic entities only")

    return list(entities.values())


def extract_relations(text, entity_list, ollama_url, model):
    """Grounded relation extraction: triples over the pre-extracted entity list.

    Returns a list of {"a": str, "rel": str, "b": str}. Triples whose endpoints
    are not in the entity list are dropped (grounding filter) rather than kept.
    """
    if len(entity_list) < 2:
        return []

    entity_lines = "\n".join(f"- {e['text']} ({e['type']})" for e in entity_list)
    user = f"TEXT:\n{text}\n\nENTITIES:\n{entity_lines}"

    try:
        result = _ollama_json(ollama_url, model, RELATION_EXTRACTION_PROMPT, user)
    except Exception as e:
        print(f"    [warn] relation extraction failed ({e}); returning no relations")
        return []

    known = {e["text"].lower() for e in entity_list}
    relations = []
    for rel in result.get("relations", []):
        a = str(rel.get("a", "")).strip()
        b = str(rel.get("b", "")).strip()
        label = str(rel.get("rel", "")).strip()
        if a.lower() in known and b.lower() in known and label and a.lower() != b.lower():
            relations.append({"a": a, "rel": label, "b": b})
    return relations
