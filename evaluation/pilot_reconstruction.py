"""Pilot: cumulative graph reconstruction from released Enron email, without and with sanitization.

Pilot only. It is NOT the confirmatory study of docs/audit/p0-comparison-protocol.md:
the gold graph comes from message headers (not independent annotation), the
"with method" arm is the existing relation-aware pipeline (no ledger/controller),
and the sample is small. See evaluation/results/pilot_reconstruction/README.md.

Design
  groups   : GROUPS custodians x MSGS_PER_GROUP messages, taken in tar order (deterministic).
  gold     : undirected sender-recipient pairs from From/To/Cc headers, persons keyed by address.
  released : the email as a user would paste it (From/To/Cc/Subject + body, <=200 words).
  arms     : raw | masked (every detected entity -> [REDACTED]) | relation (framework pipeline,
             fluency off).
  defense  : qwen3-local (entity + relation extraction). attacker: llama3.2 (different family).
  attack   : after k = 1..MSGS_PER_GROUP released messages, the attacker lists who communicated
             with whom. Scored identity-linked (real names) and, for labelled placeholders,
             anonymous-topology (placeholder mapped back to the person by the evaluator).
"""

import email
import json
import random
import re
import sys
import tarfile
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from framework.extraction import EMAIL_REGEX, extract_entities, extract_relations  # noqa: E402
from framework.generalization import apply_mapping, build_mapping  # noqa: E402

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFENSE_MODEL = "qwen3-local:latest"
ATTACK_MODEL = "llama3.2:latest"
GROUPS = 10
MSGS_PER_GROUP = 4
TAR = ROOT / "data" / "enron_mail.tar.gz"
OUT = ROOT / "evaluation" / "results" / "pilot_reconstruction"
ARMS = ("raw", "masked", "relation")


# ---------------------------------------------------------------- sampling
def local_tokens(addr):
    local = addr.split("@", 1)[0]
    return [t for t in re.split(r"[._\-\d]+", local.lower()) if len(t) >= 2]


def parse_message(raw):
    msg = email.message_from_string(raw)
    frm = EMAIL_REGEX.findall(msg.get("From", ""))
    rcpt = []
    for h in ("To", "Cc"):
        for a in EMAIL_REGEX.findall(msg.get(h, "") or ""):
            if a.lower() not in [r.lower() for r in rcpt]:
                rcpt.append(a)
    body = msg.get_payload() if not msg.is_multipart() else ""
    lines = [l.strip() for l in str(body).split("\n")
             if l.strip() and not re.match(r"^[=\-_*#\s/\\>]+$", l.strip())]
    body = " ".join(" ".join(lines).split()[:200])
    return frm, rcpt, " ".join(msg.get("Subject", "").split()), body


def sample_groups():
    groups, cur_name, cur = [], None, []
    seen = set()
    with tarfile.open(TAR, "r:gz") as tar:
        for m in tar:
            if not (m.isfile() and m.name.endswith(".")):
                continue
            parts = m.name.split("/")
            if len(parts) < 3:
                continue
            cust = parts[1]
            if cust in seen:
                continue
            if cust != cur_name:
                cur_name, cur = cust, []
            raw = tar.extractfile(m).read().decode("utf-8", errors="ignore")
            frm, rcpt, subj, body = parse_message(raw)
            if len(frm) != 1 or not (2 <= len(rcpt) <= 5) or not (25 <= len(body.split()) <= 200):
                continue
            if any(tokens == [] for tokens in map(local_tokens, frm + rcpt)):
                continue
            cur.append({"file": m.name, "from": frm[0], "rcpt": rcpt, "subject": subj, "body": body})
            if len(cur) == MSGS_PER_GROUP:
                groups.append({"custodian": cust, "messages": cur})
                seen.add(cust)
                cur = []
                if len(groups) == GROUPS:
                    return groups
    return groups


def released_raw(m):
    return (f"From: {m['from']}\nTo: {', '.join(m['rcpt'])}\nSubject: {m['subject']}\n\n{m['body']}")


# ---------------------------------------------------------------- defenses
def defend(text):
    ents = extract_entities(text, OLLAMA_URL, DEFENSE_MODEL)
    rels = extract_relations(text, ents, OLLAMA_URL, DEFENSE_MODEL)
    mapping = build_mapping(ents, rels)
    relation = apply_mapping(text, mapping)
    masked = apply_mapping(text, {k: "[REDACTED]" for k in mapping})
    return {"entities": ents, "relations": rels, "mapping": mapping,
            "raw": text, "masked": masked, "relation": relation}


# ---------------------------------------------------------------- attacker
ATTACK_PROMPT = """You are analysing leaked, possibly redacted business emails. Documents are numbered.
List every pair of people (or placeholders such as "Person-A") that the documents show
communicating with each other (sender to recipient). Use the exact names, addresses or
placeholders as they appear. Output strict JSON:
{"edges": [{"doc": <document number>, "a": "<name>", "b": "<name>"}]}
If nothing can be determined, output {"edges": []}."""


def attack(docs):
    body = "\n\n".join(f"DOCUMENT {i + 1}:\n{d}" for i, d in enumerate(docs))
    last = None
    for _ in range(3):
        try:
            r = requests.post(OLLAMA_URL, json={
                "model": ATTACK_MODEL,
                "messages": [{"role": "system", "content": ATTACK_PROMPT},
                             {"role": "user", "content": body}],
                "format": "json", "stream": False,
                "options": {"temperature": 0.0, "seed": 7, "num_predict": 700,
                            "repeat_penalty": 1.1}}, timeout=120)
            r.raise_for_status()
            edges = json.loads(r.json()["message"]["content"]).get("edges", [])
            return [e for e in edges if isinstance(e, dict) and e.get("a") and e.get("b")]
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2)
    print("   attacker failed:", last)
    return []


# ---------------------------------------------------------------- scoring
def toks(x):
    x = str(x)
    if "@" in x:
        return set(local_tokens(x))
    return {t for t in re.split(r"[^a-z]+", x.lower()) if len(t) >= 2}


def match_unique(x, persons):
    """Index of the single gold person that string x names, else None."""
    tx = toks(x)
    if not tx:
        return None
    hits = [i for i, p in enumerate(persons) if tx <= set(local_tokens(p)) or set(local_tokens(p)) <= tx]
    return hits[0] if len(hits) == 1 else None


def gold_for(group, k):
    persons, edges = [], set()
    def pid(a):
        for i, p in enumerate(persons):
            if p.lower() == a.lower():
                return i
        persons.append(a)
        return len(persons) - 1
    per_doc = []
    for m in group["messages"][:k]:
        s = pid(m["from"])
        de = set()
        for r in m["rcpt"]:
            t = pid(r)
            if s != t:
                e = frozenset((s, t))
                edges.add(e)
                de.add(e)
        per_doc.append(de)
    return persons, edges, per_doc


def placeholder_person(label, mapping, persons):
    """Evaluator-side alignment: which gold person does this placeholder stand for?"""
    lab = str(label).strip().lower().replace("[", "").replace("]", "")
    lab = re.sub(r"'s address$", "", lab).strip()
    lab = re.sub(r"\s*\(.*\)$", "", lab).strip()
    surfaces = [s for s, ph in mapping.items()
                if re.sub(r"\s*\(.*\)$", "", ph.lower().replace("[", "").replace("]", "")
                          .replace("'s address", "").strip()) == lab and lab.startswith("person")]
    ids = {match_unique(s, persons) for s in surfaces}
    ids.discard(None)
    return ids.pop() if len(ids) == 1 else None


def score(group, k, arm, edges_out, defended):
    persons, gold, per_doc = gold_for(group, k)
    ident, anon = set(), set()
    n_out = 0
    seen_id, seen_an = set(), set()
    for e in edges_out:
        n_out += 1
        a, b = e["a"], e["b"]
        ia, ib = match_unique(a, persons), match_unique(b, persons)
        if ia is not None and ib is not None and ia != ib:
            ident.add(frozenset((ia, ib)))
            seen_id.add(frozenset((ia, ib)))
        if arm in ("relation",):
            try:
                d = int(e.get("doc", 0)) - 1
            except (TypeError, ValueError):
                continue
            if not 0 <= d < k:
                continue
            mp = defended[d]["mapping"]
            pa, pb = placeholder_person(a, mp, persons), placeholder_person(b, mp, persons)
            if pa is not None and pb is not None and pa != pb and frozenset((pa, pb)) in per_doc[d]:
                anon.add((d, frozenset((pa, pb))))
            seen_an.add((d, a, b))
    tp_id = len(ident & gold)
    fp_id = len(ident - gold)
    # anonymous: denominator = per-doc gold edges
    gold_an = sum(len(x) for x in per_doc)
    return {"gold": len(gold), "gold_an": gold_an, "out": n_out,
            "tp_id": tp_id, "fp_id": fp_id,
            "tp_an": len(anon), "out_an": len(seen_an)}


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    gfile = OUT / "groups.json"
    if gfile.exists():
        groups = json.loads(gfile.read_text())
    else:
        groups = sample_groups()
        gfile.write_text(json.dumps(groups, indent=1))
    print(f"{len(groups)} groups, {sum(len(g['messages']) for g in groups)} messages")

    dfile = OUT / "defended.json"
    defended = json.loads(dfile.read_text()) if dfile.exists() else {}
    for gi, g in enumerate(groups):
        for mi, m in enumerate(g["messages"]):
            key = f"{gi}-{mi}"
            if key in defended:
                continue
            t0 = time.time()
            defended[key] = defend(released_raw(m))
            dfile.write_text(json.dumps(defended, indent=1))
            print(f"defended {key} ({time.time() - t0:.0f}s)", flush=True)

    afile = OUT / "attacks.json"
    attacks = json.loads(afile.read_text()) if afile.exists() else {}
    for gi, g in enumerate(groups):
        for k in range(1, MSGS_PER_GROUP + 1):
            for arm in ARMS:
                key = f"{gi}-{k}-{arm}"
                if key in attacks:
                    continue
                docs = [defended[f"{gi}-{j}"][arm] for j in range(k)]
                attacks[key] = attack(docs)
                afile.write_text(json.dumps(attacks, indent=1))
        print(f"attacked group {gi}", flush=True)

    rows = []
    for gi, g in enumerate(groups):
        for k in range(1, MSGS_PER_GROUP + 1):
            dl = [defended[f"{gi}-{j}"] for j in range(k)]
            for arm in ARMS:
                s = score(g, k, arm, attacks[f"{gi}-{k}-{arm}"], dl)
                rows.append({"group": gi, "k": k, "arm": arm, **s})
    (OUT / "scores.json").write_text(json.dumps(rows, indent=1))
    print("scores written")


if __name__ == "__main__":
    main()
