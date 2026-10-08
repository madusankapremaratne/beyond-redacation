# Annotation guidelines: relations between people in Enron email

Purpose: independent gold edges for the organizational graph. Three annotators label independently (A, B, C), must not see any model output, and must not discuss labels with each other until the tie meeting.

## What to annotate
You read `packets/documents.md` and fill `packets/packet_<you>.csv`. Each row is a candidate pair of people in one document. Leave `relation` **blank** when the document gives no evidence of a relationship between them. Do not use the From/To header on its own as evidence: being a recipient is not a relationship.

A relationship counts only if the **body text** states or clearly implies it. If you need outside knowledge, leave it blank and set `unsure=1`.

## Relation types (use exactly these strings)
| `relation` | Use when the text shows... | `direction` |
|---|---|---|
| `reports_to` | one person is the other's subordinate or the other gives them instructions | `a>b` means a reports to b |
| `manages` | one person directs the other's work (inverse of reports_to; use one, not both) | `a>b` means a manages b |
| `collaborates_with` | two people work on the same task, deal, project or meeting | none |
| `requests_from` | one asks the other for an action or information | `a>b` means a asks b |
| `informs` | one gives the other information or a decision (not a request) | `a>b` means a informs b |
| `same_team` | stated membership of the same team or department | none |
| `none` | text mentions both but shows no relationship | none |

If several apply, pick the most specific; do not label a pair twice. Write the supporting words (at most 15) in `evidence`.

## Same person under two names
If two candidates are the same person ("Jeff" / "Jeffrey Shankman"), label the pair `none` and write `same person` in `notes`; the adjudicator merges them.

## Missed relations
If a document shows a relationship between people the candidates miss, add a row: fill `group`, `doc`, `person_a`, `person_b`, set `source=added`, and label it.

## Process
1. Pilot: both annotators label the calibration groups (2, 4, 10, 13, 26; see `freeze_manifest.json`) and meet to resolve unclear rules; revise this file; the pilot groups are then discarded from agreement statistics.
2. Independent labelling of all groups.
3. `python3 annotation/agreement.py done_A.csv done_B.csv done_C.csv` reports Fleiss' kappa (and pairwise Cohen's kappa) for edge presence and relation-type agreement, and writes `gold_edges.csv`.
4. Gold rule, fixed before labelling: a pair is an edge if at least 2 of 3 annotators marked it; its relation is the plurality among those who marked it, and its direction the plurality among those who agree on the relation. If a plurality is tied the pair gets status `discuss`; the three annotators settle those pairs together in one meeting and the result goes in `final_relation` / `final_direction`. The annotators' files are kept unchanged.
5. Report kappa, the guideline version, annotator background and how many rows were `unsure`.

Targets (set before labelling): Fleiss' kappa >= 0.6 for edge presence; if lower, revise guidelines and relabel, do not average.
