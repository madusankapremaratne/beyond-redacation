# Plan: getting the paper to a submittable state

Written 8 October 2026 after the self-critique. Principle: H1 (identifier removal leaves relations recoverable) can be a standalone short paper if it is measured cleanly, so Phases 1-2 are on the critical path and the controller (Phase 3) is optional upside. Phase gates are stop/decide points, not promises.

## Phase 0: freeze and label (start now)
- **Independent labels** (item 2 of the critique). Kit in `annotation/`: `make_packets.py` (30 groups x 4 messages, 780 candidate pairs after filtering, custodians disjoint from the pilot), `GUIDELINES.md`, `agreement.py`. Three human annotators (planned: one from product management, one from engineering, one from marketing, all colleagues of an author, which the paper must disclose) label independently; gold edges by majority vote (2 of 3), with a tie meeting for unresolved relation type or direction. No model output is shown to them. Budget about 120 messages each; do a 5-group calibration round first.
- Freeze (done 8 Oct 2026: `annotation/freeze.py` -> `annotation/freeze_manifest.json`; split 5 calibration / 10 development / 15 test groups; re-run to verify): sample, split (development vs test groups), attacker prompts, model identifiers and digests (`ollama show`), seeds. Commit before test outputs exist.
- **Gate:** Fleiss' kappa for edge presence >= 0.6 and enough gold edges (target >= 150 on test groups). If not, revise guidelines; do not average over low agreement.

## Phase 1: re-measure H1 on independent labels
- Rescore the existing pilot arms (raw, masked, relation-aware) against the new gold, not headers. Strip headers from released text in one condition so raw is not trivially easy.
- Attackers: at least two model families including one strong model; one adaptive attacker that is told the defense. Three repeats where stochastic.
- Report recovery against the no-transcript baseline, identity-linked and anonymous topology, with cluster-bootstrap intervals; failed calls stay in denominators.
- Memorization check: ask attackers about the sampled people with no document; report that recovery rate as the contamination floor.
- **Gate:** if relation-aware text still leaks above baseline with a stronger attacker, H1 stands and the paper has a result. If not, the leakage claim must be rewritten as a negative or partial finding.

## Phase 2: comparison baselines
- Implement or adapt PrivScope-style and PlanTwin-style controls, documenting every adaptation (see `docs/audit/p0-comparison-protocol.md`); add attack-guided anonymization where a runnable version exists.
- Measure utility on defined tasks (not embedding similarity) with a frozen rubric.
- **Gate:** baselines run on the same frozen test groups with matched budgets, or the paper states plainly which comparisons are missing.

## Phase 3: controller (only if H1 holds)
- Build the candidate generator, ledger and keep-local/abstain decision with a rules judge first; add local LLM and Jev judges after.
- Run the ablations in Results Table 6 and the calibration and fault-injection tests.
- Keep the hosted-judge boundary: local enforcement before any permitted transmission.
- **Gate:** if H2 is null or small, report it and reframe the paper as a measurement study with an honest controller negative result.

## Phase 4: second corpus and device cost
- A second corpus (different domain or period), or at minimum a contamination analysis, so findings are not Enron-only.
- Full-pipeline timings and memory on the two target phones, with peak memory measured under one definition per platform.

## Phase 5: paper rewrite
- Replace every TBD from the frozen run manifest; delete the pilot (or keep it as a short, labelled preliminary).
- Move protocol detail, prompts and per-arm settings to appendices; keep the main text to the claims the data support.
- Rewrite the abstract, introduction, discussion and conclusions to the measured result; fill the MDPI generative-AI disclosure, funding, conflicts and data statements; deposit data and code.
- Review against Future Internet scope and length; check novelty claims once more against newly published work (PrivScope, PlanTwin and later).

## Cross-cutting
- Nothing is committed until the author validates. Results directories are gitignored; deposit what the data statement promises.
- Re-verify every reference before submission (`docs/audit/p0-reference-audit.md`).
