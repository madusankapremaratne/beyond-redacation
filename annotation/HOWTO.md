# How to annotate: step-by-step

Read `GUIDELINES.md` for the relation definitions. This page is the practical walkthrough. It uses an invented example, not text from the packets.

## Roles
- **Annotators A, B and C**: three people label independently (planned: one from product management, one from engineering, one from marketing). Never compare, discuss or share files until all three have finished.
- **Coordinator**: sends packets, runs the scripts, keeps the originals untouched. The coordinator does not label.

You will not see any model output. If you have seen one of the project's model results, tell the coordinator.

## What you need
1. `packets/documents.md`: the emails (groups of 4, numbered "Group 7, document 2").
2. `packets/packet_A.csv` (or `_B`): your labelling sheet. Open it in a spreadsheet (Excel, Numbers, Google Sheets). Make a copy named `done_A.csv` and work in that; keep the original.
3. `GUIDELINES.md` open beside it.

Roughly 120 emails. Plan 2 to 3 minutes per email once you are used to it, in sessions of at most 45 minutes. Quality drops when you rush.

## The sheet
Each row is a candidate pair of people in one email. Columns you fill: `relation`, `direction`, `evidence`, `unsure`, `notes`. Do not edit `group`, `doc`, `person_a`, `person_b` or `source`.

## Procedure for each email
1. In `documents.md`, read the whole email, headers included, so you know who sent it and to whom.
2. In the sheet, filter to that `group` and `doc`.
3. For every row, ask: **does the body text show a relationship between these two people?** Use the decision flow below.
4. Fill `relation` only if yes; otherwise leave it blank. Blank means "no evidence". Use `none` only for the case "both are discussed together but nothing links them".
5. Add rows for relationships the sheet missed (see "Adding rows").
6. Move to the next email. Do not go back and relabel using later emails; each email is judged on its own text.

### Decision flow
1. Is there any sentence in the body about both people, or between them (one asks, tells, assigns, thanks or answers the other)? If no, blank.
2. Is the only link that one wrote and the other received? That is not enough. Blank, unless the body also shows a request or information passed to them (then `requests_from` or `informs`).
3. Choose the most specific type from `GUIDELINES.md`. If two fit, prefer: `reports_to` / `manages`, then `requests_from`, then `informs`, then `collaborates_with`, then `same_team`.
4. Set `direction` (`a>b` or `b>a`) for the directed types. Check which person is `person_a` in that row.
5. Copy the key words (at most 15) into `evidence`.
6. If you could only decide by using what you know about Enron from outside the email, leave `relation` blank and set `unsure` to 1.

## Worked example (invented)

Email:

> From: dana.cole@corp.com  To: lee.park@corp.com, sam.ortiz@corp.com
> Lee, please send me the Q3 volumes by Friday. Sam will review the contract language with you. Thanks, Dana

| person_a | person_b | what to enter |
|---|---|---|
| Dana Cole | Lee Park | `requests_from`, direction `a>b`, evidence "please send me the Q3 volumes by Friday" |
| Dana Cole | Sam Ortiz | blank (Sam is only mentioned as a reviewer; no link to Dana stated) |
| Lee Park | Sam Ortiz | `collaborates_with`, direction blank, evidence "Sam will review the contract language with you" |

Not entered: `reports_to` for Lee and Dana. A request alone does not show that Lee is Dana's subordinate.

## Adding rows
If the email shows a relation the sheet missed (a person not in the candidates, or a pair left out), copy the last row, then set: `group`, `doc`, `person_a`, `person_b`, `source` = `added`, and fill the label as usual. Spell names as they appear in the email.

## Calibration round (do this first)
All three annotators label only the five calibration groups: **2, 4, 10, 13, 26**. Then, and only then, meet. For each disagreement, agree what the rule should say, update `GUIDELINES.md`, and record the change with a date. These five groups are then dropped from the agreement statistics and from the gold set.

## Finishing
1. Save as `done_A.csv`, `done_B.csv` or `done_C.csv` (your letter), UTF-8 CSV, same columns, same row order plus any added rows.
2. Do not delete rows, rename columns or merge cells.
3. Send the file to the coordinator and record: time spent, how many rows you marked `unsure`, and anything in the guidelines that was unclear.

## Coordinator checklist
1. Verify the freeze: `python3 annotation/freeze.py` must print "manifest verified: unchanged".
2. Send `documents.md`, `GUIDELINES.md`, `HOWTO.md` and one packet (`packet_A/B/C.csv`) to each annotator, separately.
3. After calibration, collect, revise guidelines, re-run `python3 annotation/freeze.py --force` (the guidelines hash changes) and record why.
4. After full labelling:
   ```bash
   python3 annotation/agreement.py annotation/packets/done_A.csv annotation/packets/done_B.csv annotation/packets/done_C.csv
   ```
   Target: Fleiss' kappa for edge presence of at least 0.6. If it is lower, revise the guidelines and relabel; do not average.
5. `packets/gold_edges.csv` has one row per pair with at least one edge vote. Status `gold` is final; `minority` (one vote) is not an edge; `discuss` rows (tied relation or direction) are settled by the three annotators in a single meeting, who fill `final_relation` and `final_direction`. Keep the `done_*.csv` files unchanged.
6. Count gold edges on the test groups (0, 1, 3, 5, 7, 8, 11, 14, 16, 19, 20, 22, 23, 25, 27). If there are fewer than about 150, add groups (`make_packets.py --groups N`) or lower the target and say so in the paper.

## Independence and disclosure
The annotators are colleagues of an author. Report this in the paper, give the annotators' roles (not names), and record that none saw any model output. Annotators should not be told which arm or hypothesis the labels will test.

## Common mistakes
- Labelling a pair because they appear in the To/From lines. That is the header, not evidence.
- Using outside knowledge about who managed whom at Enron.
- Labelling both `manages` and `reports_to` for one pair.
- Filling `direction` the wrong way round; check which name is `person_a` in that row.
- Changing names or deleting rows.
