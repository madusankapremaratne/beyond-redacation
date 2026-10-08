"""Build annotation packets for independent relation labels on Enron email.

Draws GROUPS groups of MSGS messages (same sampling rules as the pilot, but from custodians
the pilot did not use), then writes one CSV per annotator with candidate person pairs per
document. Annotators fill the blank columns; they also add rows for relations the candidates
miss (doc, person_a, person_b filled by hand, source=added).

    python3 annotation/make_packets.py --groups 30 --seed 11 --annotators A B C

Outputs (annotation/packets/): groups.json (frozen sample), documents.md (the text annotators
read), packet_<id>.csv. The packets contain NO model output, so annotators stay independent of
every defense and attacker.
"""
import argparse, csv, json, random, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evaluation"))
sys.path.insert(0, str(ROOT))
import pilot_reconstruction as pr  # noqa: E402
from framework.extraction import _nlp  # noqa: E402

OUT = Path(__file__).resolve().parent / "packets"
FIELDS = ["group", "doc", "person_a", "person_b", "source", "relation", "direction",
          "evidence", "unsure", "notes"]


JUNK = {"dl", "all", "staff", "shift", "worldwide", "group", "team", "info", "admin", "list", "desk",
        "support", "help", "inc", "corp", "company", "cement", "energy", "llc", "ltd", "services",
        "communications", "participants", "settle", "contacts", "center", "department", "helpdesk", "desk"}


def is_junk(name):
    toks = re.findall(r"[a-z]{2,}", name.lower())
    return not toks or any(t in JUNK for t in toks) or bool(re.search(r"[\d_]", name.split("<")[-1]))


def candidates(m):
    """People a relation could be about, as display strings.

    Header people and PERSON names in the body, minus distribution lists / organisations
    (JUNK), with aliases merged (token-subset). A pair is kept only if body text could
    evidence it: the sender with anyone, or any pair where an endpoint is named in the body.
    Recipient-recipient pairs that the body never mentions are dropped (nothing to label).
    """
    body_l = m["body"].lower()
    people = []   # (display, token set, is_sender)
    def add(name, sender=False):
        if "<" not in name:                       # body name: tidy Lotus Notes forms, drop fragments
            name = re.sub(r"/.*$", "", name).strip(" :,;")
            if ":" in name or "@" in name or len(name) < 3:
                return
        toks = set(re.findall(r"[a-z]{2,}", name.split("<")[0].lower())) or set(pr.local_tokens(name))
        if not toks or is_junk(name):
            return
        for i, (d, t, s_) in enumerate(people):
            if toks <= t or t <= toks:   # same person under a shorter/longer alias
                people[i] = (d if len(t) >= len(toks) else name, t | toks, s_ or sender)
                return
        people.append((name, toks, sender))
    add(" ".join(t.capitalize() for t in pr.local_tokens(m["from"])) + f" <{m['from']}>", True)
    for a in m["rcpt"]:
        add(" ".join(t.capitalize() for t in pr.local_tokens(a)) + f" <{a}>")
    for ent in _nlp()(m["body"]).ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) <= 3:
            add(ent.text.strip())
    people = people[:5]
    named = [any(len(t) >= 3 and re.search(r"(?<![a-z])" + t + r"(?![a-z])", body_l) for t in tk)
             for _, tk, _ in people]
    out = []
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            if people[i][2] or people[j][2] or named[i] or named[j]:
                out.append((people[i][0], people[j][0]))
    return out


def sample(n_groups, seed, exclude):
    used = set(exclude)
    pool, cur, cur_name = [], [], None
    import tarfile
    with tarfile.open(pr.TAR, "r:gz") as tar:
        for mem in tar:
            if not (mem.isfile() and mem.name.endswith(".")):
                continue
            parts = mem.name.split("/")
            if len(parts) < 3 or parts[1] in used:
                continue
            cust = parts[1]
            if cust != cur_name:
                cur_name, cur = cust, []
            if any(g["custodian"] == cust for g in pool):
                continue
            raw = tar.extractfile(mem).read().decode("utf-8", errors="ignore")
            frm, rcpt, subj, body = pr.parse_message(raw)
            if len(frm) != 1 or not (2 <= len(rcpt) <= 5) or not (25 <= len(body.split()) <= 200):
                continue
            cur.append({"file": mem.name, "from": frm[0], "rcpt": rcpt, "subject": subj, "body": body})
            if len(cur) == pr.MSGS_PER_GROUP:
                pool.append({"custodian": cust, "messages": cur}); cur = []
                if len(pool) >= max(4 * n_groups, 40):
                    break
    random.Random(seed).shuffle(pool)
    return pool[:n_groups]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groups", type=int, default=30)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--annotators", nargs="+", default=["A", "B", "C"])
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    pilot = json.loads((ROOT / "evaluation/results/pilot_reconstruction/groups.json").read_text()) \
        if (ROOT / "evaluation/results/pilot_reconstruction/groups.json").exists() else []
    groups = sample(a.groups, a.seed, [g["custodian"] for g in pilot])
    (OUT / "groups.json").write_text(json.dumps(groups, indent=1))
    rows, md = [], []
    for gi, g in enumerate(groups):
        md.append(f"# Group {gi}\n")
        for di, m in enumerate(g["messages"]):
            md.append(f"## Group {gi}, document {di + 1}\n\nFrom: {m['from']}\nTo: {', '.join(m['rcpt'])}\n"
                      f"Subject: {m['subject']}\n\n{m['body']}\n")
            for pa, pb in candidates(m):
                rows.append({"group": gi, "doc": di + 1, "person_a": pa, "person_b": pb, "source": "candidate"})
    (OUT / "documents.md").write_text("\n".join(md))
    for ann in a.annotators:
        with open(OUT / f"packet_{ann}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
    print(f"{len(groups)} groups, {len(rows)} candidate pairs, packets for {a.annotators}")


if __name__ == "__main__":
    main()
