"""Inter-annotator agreement and majority-vote gold labels for relation annotation.

    python3 annotation/agreement.py done_A.csv done_B.csv done_C.csv [--out=gold_edges.csv]

Works for 2 or more annotators. An edge is (group, doc, unordered person pair); a row counts as an
edge when `relation` is non-empty and not 'none'. Pairs an annotator did not list count as no edge
for them. Reports Fleiss' kappa on edge presence (and Cohen's kappa for every annotator pair),
raw agreement, and relation-type agreement among edges at least two annotators marked.

Gold rule (fixed before labelling):
  * edge = at least ceil(n/2) annotators marked an edge (2 of 3);
  * relation = plurality among annotators who marked an edge; direction = plurality among those who
    agree on the relation;
  * if the plurality is tied, the pair is written with status `discuss` and the three annotators
    settle it in a meeting; the settled value goes in `final_*` columns.
Writes gold_edges.csv (all pairs with >=1 edge vote). Never edit the annotators' files.
"""
import csv, re, sys
from collections import Counter
from itertools import combinations
from pathlib import Path


def pairkey(a, b):
    f = lambda s: " ".join(sorted(re.findall(r"[a-z]{2,}", s.split("<")[0].lower()))) or s.lower()
    return tuple(sorted((f(a), f(b))))


def load(path):
    out = {}
    for r in csv.DictReader(open(path, newline="")):
        key = (r["group"], r["doc"]) + pairkey(r["person_a"], r["person_b"])
        rel = (r["relation"] or "").strip().lower()
        out[key] = {"edge": rel not in ("", "none"), "rel": rel, "dir": (r["direction"] or "").strip(), "row": r}
    return out


def edge(a, k):
    return a.get(k, {"edge": False})["edge"]


def fleiss(anns, keys):
    n, N = len(anns), len(keys)
    p_i, yes = [], 0
    for k in keys:
        y = sum(edge(a, k) for a in anns); yes += y
        p_i.append((y * (y - 1) + (n - y) * (n - y - 1)) / (n * (n - 1)))
    Pbar = sum(p_i) / N
    py = yes / (n * N)
    Pe = py ** 2 + (1 - py) ** 2
    return (Pbar - Pe) / (1 - Pe) if Pe < 1 else 1.0, Pbar


def cohen(a, b, keys):
    x = [edge(a, k) for k in keys]; y = [edge(b, k) for k in keys]; N = len(keys)
    po = sum(i == j for i, j in zip(x, y)) / N
    pe = (sum(x) / N) * (sum(y) / N) + (1 - sum(x) / N) * (1 - sum(y) / N)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def plurality(values):
    c = Counter(v for v in values if v)
    if not c:
        return "", False
    top = c.most_common()
    tie = len(top) > 1 and top[0][1] == top[1][1]
    return top[0][0], tie


def main(paths, out="annotation/packets/gold_edges.csv"):
    anns = [load(p) for p in paths]
    n = len(anns)
    keys = sorted(set().union(*[set(a) for a in anns]))
    kf, po = fleiss(anns, keys) if n > 2 else (cohen(anns[0], anns[1], keys), None)
    print(f"annotators {n}  pairs {len(keys)}  edge-presence kappa {kf:.3f}" +
          (f" (Fleiss)  raw agreement {po:.3f}" if po is not None else " (Cohen)"))
    for (i, a), (j, b) in combinations(enumerate(anns), 2):
        print(f"  Cohen {chr(65 + i)}-{chr(65 + j)}: {cohen(a, b, keys):.3f}")
    need = (n + 1) // 2
    typed = same = 0
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["group", "doc", "person_a", "person_b", "edge_votes", "relation", "direction", "status",
                    "final_relation", "final_direction"])
        for k in keys:
            votes = [a[k] for a in anns if edge(a, k)]
            if not votes:
                continue
            row = next(a[k]["row"] for a in anns if k in a)
            isedge = len(votes) >= need
            rel, tie = plurality([v["rel"] for v in votes])
            dirn, dtie = plurality([v["dir"] for v in votes if v["rel"] == rel])
            if len(votes) >= 2:
                typed += 1; same += len({v["rel"] for v in votes}) == 1
            status = "gold" if isedge and not tie and not dtie else ("discuss" if isedge else "minority")
            w.writerow([row["group"], row["doc"], row["person_a"], row["person_b"], len(votes), rel, dirn,
                        status, "", ""])
    print(f"relation-type agreement among edges with >=2 votes: {same}/{typed}" if typed else "no multi-vote edges")
    print("wrote", out, "(status: gold / discuss / minority)")


if __name__ == "__main__":
    args = sys.argv[1:]
    out = next((a.split("=", 1)[1] for a in args if a.startswith("--out=")), "annotation/packets/gold_edges.csv")
    main([a for a in args if not a.startswith("--out=")], out)
