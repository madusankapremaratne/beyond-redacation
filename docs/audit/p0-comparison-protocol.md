# Proposed comparison protocol

Date: 2026-10-08. P0 produces a reviewable protocol, not collaborator sign-off, implemented controls or experimental results. This protocol refines the original plan where they differ.

## Threat boundary and hypothesis

The trusted local device retains raw text, private memory, mappings and protected relations. The cloud recipient observes every released payload and its permitted accumulated history. Report metadata exposure separately. Device compromise is outside this experiment, not declared safe.

Test whether local evidence-conditioned selection lowers cumulative forbidden-fact/edge reconstruction at a preregistered utility level and matched coverage compared with task-aware abstraction and a weighted disclosure ledger. Separately test calibrated rejection. Null/negative results are valid outcomes.

Hosted Jev is an offline comparator for approved benchmark material. It receives an input before it can reject it, so it cannot be the first gate protecting that same input from its provider. No P0 API inference or private-data uploads were performed.

## Data and labels

1. Preserve N50 as a historical convenience-sample track only if its caches and lineage are recovered. Otherwise label a rerun as a new experiment.
2. Index/checksum the complete source archive; document parsing, eligibility, deduplication and sampling seed. Use an email parser with explicit handling of forwarded/quoted material.
3. Split by linked identity/thread groups before tuning. Quantify unavoidable entity overlap and add a disjoint subset; no silent duplicate contamination.
4. Separate development, calibration and test. Original300-group target is a planning estimate; choose final cluster count and precision/power target using a pilot before opening test outcomes.
5. Independently annotate allowed/prohibited facts, aliases, directed typed relations, uncertainty and task-required information. Two annotators with blinded method identity and adjudication; report agreement/unknowns.
6. Source-supported facts are the gold standard, not an attacker's JSON or the defense extractor. Enron text assertions are not presumed verified real-world corporate truth.
7. Evaluate genuine linked histories where available, with proposed lengths1,5,10,20; do not invent missing real turns. Add explicitly synthetic topology/counterfactual fixtures. Chronological, shuffled and adaptive attack histories use matched budgets.

## Comparison arms

| Arm | Purpose and controls |
|---|---|
| Raw cloud, always local, deny all | Utility/exposure and zero-release references. Include local quality/cost and abstention in total-system outcomes. |
| Literal masking | Same detector as proposed pipeline; isolates replacement policy. |
| Existing07 and08 | Freeze original holistic and typed-mapping baselines with immutable prompts/models/cache keys. |
| PAPILLON-style; attack-guided anonymization/INTACT-style | Prefer authors' implementations; disclose adaptations rather than attaching an original method name to an arbitrary substitute. |
| PrivScope-style task necessity/abstraction | Closest task-aware comparison; match available evidence and calibration budget. |
| PlanTwin-style cumulative weighted-field budget | Closest history comparator; fix schema/weights/thresholds using development data only. |
| Proposed local policy | Match detector, candidate generator, models and compute budget across ablations. |
| Optional PREEMPT/PP-TS/GAMA/STAMP | Include where threat assumptions/workload allow faithful execution; state unavailable baselines. |
| Offline Jev and alternative judges | Same permitted evidence and candidate pool. Separate deployment-visible, history-aware and oracle-secret inputs; oracle results are not deployable performance. |

Primary comparisons must include closest task-aware/history baselines, rather than only weak fixed rewriting. Select the final primary contrast and utility margin before the test set.

Core ablations: history off; graph evidence off; task relevance off; calibration off; abstention off; fluency off; relation extraction off; matched versus oracle detection. Keep candidate search local before release. Sending all candidates to a hosted judge adds exposure and must be counted.

## Metrics and statistics

- Direct leakage: prohibited-attribute precision/recall in actual transmitted payloads and attacker outputs, with aliases/denominators. Distinguish copying, correct inference and hallucination.
- Structural recovery: directed typed-edge precision/recall/F1 against independent labels; separate identity-linked recovery from anonymous topology using a declared alignment procedure. Endpoint co-occurrence is not an edge.
- Cumulative recovery: union and newly recovered facts/edges by turn, history-only inference and linkage. A weighted operational ledger is not epsilon.
- Utility: task success, faithfulness and unsupported-answer rates for action extraction, scheduling, role-level QA or summarization under declared rubrics. Similarity is secondary. Include withheld/unanswerable cases, fallback and abstention.
- Selection: false-safe and false-block rates, release coverage, risk–coverage curves, calibration reliability/Brier score and ECE with declared bins. Report missing/invalid outputs.
- Resources: full-pipeline/component latency, p50/p95, cold/warm distributions, load time and consistent memory definitions. Include candidate/judge overhead; report energy only if measured.
- Inference: paired comparisons on identical inputs; cluster bootstrap by identity/session groups with fixed seed. Predeclare primary contrasts and multiplicity treatment. Report effective group count and failures; do not create confidence intervals from rounded means.
- Robustness: at least two held-out attacker families and multiple fixed seeds proposed. Match token/query/auxiliary-information budgets. Keep generation, attack, judgment and gold labels separate.

## Freeze and failure gates

Pin source/data/split/prompt/schema/policy hashes, weight/quantization/tokenizer digests, runtime lock, hardware/OS/build IDs, seeds, raw output provenance and timing definitions. Cache keys include all content/config/history inputs.

The proposed release policy must keep requests local or abstain on malformed outputs, timeout, unknown evidence, unsafe ambiguity or exhausted budget. Test this with fault injection; it is not an existing property of the current code. Never silently substitute simulated responses into experimental runs.

Freeze thresholds and test groups before final comparison. Protocol agreement and annotation remain future gates.
