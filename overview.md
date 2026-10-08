# Beyond Redaction: Project Overview

Updated after the evidence audit, 8 October 2026. See the [P0 report](docs/P0_EVIDENCE_AUDIT.md) for findings and evidence limits.

Beyond Redaction studies how much sensitive identity and relationship information can remain in queries sent to cloud language models after local generalization. Removing explicit names does not by itself establish protection against inference from context.

The repository implements hybrid entity detection, LLM-assisted relation extraction, typed placeholder mapping, deterministic replacement and an optional local fluency pass. Native iOS and Android prototypes implement the deterministic portion. Full LLM processing on both phones, cumulative disclosure control and a Jev controller remain unimplemented or unvalidated here.

The mapping can preserve who did what using placeholders, but that can also retain sensitive topology. Known-name removal, low string overlap and zero raw-endpoint co-survival are not guarantees against structural reconstruction. Missed entities, alias collisions and sequential replacement also require further validation.

## Saved pilot results

These are recorded notebook summaries, not newly reproduced experiments.

| Metric | Holistic rewrite07 | Relation-assisted mapping08 |
|---|---:|---:|
| Mean SER string-overlap proxy |0.393|0.209|
| Median SER |0.345|0.200|
| Heuristic name flags |5/46|4/46|

The saved paired summary reports29 improved,8 worse and13 tied out of50. Sampling used a seeded draw from the first2,000 eligible archive messages, with text truncated to200 words. Per-sample caches and score tables have not been recovered, so independent recomputation and uncertainty estimation remain blocked. Name flags have label noise.

Notebook09 records deterministic-pipeline median steady latencies of14.18ms (macOS),0.83ms (iOS), and5.83ms (Android). Detectors differ, raw device measurements are missing, and full mobile LLM stages were not measured. The memory readings were post-call measurements, not established peaks.

## Research direction

The next study should evaluate independently annotated fact and graph reconstruction, actual task utility, cumulative histories and calibrated release/abstention. Compare against close task-aware abstraction and history-budget methods, including PrivScope and PlanTwin, as well as the existing baselines.

Jev can be an offline comparison judge. A hosted judge receives its input before it rejects it, so local privacy enforcement must precede any permitted external transmission.

The [research plan](docs/JEV_RESEARCH_PLAN.md) and [comparison protocol](docs/audit/p0-comparison-protocol.md) describe the next work. Novelty and publication readiness remain unproven.
