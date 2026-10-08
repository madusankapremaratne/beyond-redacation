# P0: evidence audit

Audit date: 8 October 2026. Branch: `jev`.

**Audit work completed; experimental readiness remains blocked.** The code and saved summaries support a prototype and preliminary proxy measurements. They do not establish complete structural privacy, preserved downstream utility, cumulative protection, or a reproducible full mobile LLM pipeline.

## Scope and provenance

The current Enron repository was audited at [eed6b58aa86b95cca5d5a3c0e7d9a8d0120aca68](https://github.com/madusankapremaratne/beyond-redacation/tree/eed6b58aa86b95cca5d5a3c0e7d9a8d0120aca68). All 46 tracked files are inventoried using Git blob IDs. Nine notebooks, framework code, native benchmark sources, README, overview and plan were inspected.

An earlier eight-page educational manuscript, “Beyond Redaction: Intent-Preserving Semantic Generalization for Inference-Time Privacy in LLM Based Learning,” and its revision plan were recovered from the user's existing files. Its cited [Sovereign Learner repository](https://github.com/madusankapremaratne/sovereign-learner/tree/fe193db297e807668a96a559ea48feffbb0de903) was inspected at the pinned commit. This earlier OULAD work is distinct from the current Enron project. No authoritative current Enron manuscript was located.

Three small proof-of-concept artifacts were recovered from the existing beyond-redaction-data folder. The N=50 per-sample caches/CSVs, raw device results and historical model digests were not recovered. The large archive was located but not downloaded or checksummed. No private manuscript, raw recovered records, credentials, or new corpus extracts are included in this commit.

## Findings that change the paper

1. **Recorded results are not independently reproduced results.** Notebook 07 reports mean SER0.393002; notebook 08 reports0.209 and a paired mean difference+0.184. The raw files needed to recompute these are missing. Name flags5/46 versus4/46 are heuristic detector outcomes with known label noise.
2. **The metrics do not establish structural privacy.** SER matches flattened strings against attacker-generated baseline strings. RER measures raw endpoint co-survival, ignoring the relationship label and whether an edge was recovered. Zero RER can coexist with preserved anonymous topology.
3. **The experimental input and runtime claims need qualification.** The cleaner retains X-Origin/X-FileName metadata in all20 committed benchmark samples. N=50 samples come from the first2,000 eligible messages. Mobile timings cover deterministic detection/substitution only; “peak memory” is a post-call reading using different platform definitions.
4. **Novelty is narrower than the plan initially assumed.** PrivScope already combines task necessity and abstraction hierarchies; PlanTwin already has structured abstraction and cumulative object disclosure budgets. Jev already evaluates privacy violations. See the primary-source matrix.
5. **The older manuscript has concrete evidence problems.** Its available OULAD report gives an F1 gap9.9337 percentage points, rather than25.8. Its portability code sets interaction reductions and accuracy using assumed formulas, including target outcomes. These are not measured transfer-learning benefits.
6. **The older bibliography needs correction.** Two cited arXiv IDs resolve to unrelated papers; multiple author lists and the PRV accountant citation are wrong. One cited student-data paper remains unresolved, not declared nonexistent.
7. **Historical reproducibility cannot be honestly frozen retroactively.** Mutable model aliases and lower-bound dependencies do not identify the original environment. Missing digests remain unknown rather than being replaced by guessed versions.

## Deliverables

- [Claims–evidence matrix](claims-evidence-matrix.md): 26 current-project claims and 15 historical claim groups.
- [Related-work matrix](related-work-matrix.md): 20 entries covering the closest methods and foundational evaluation concepts.
- [Historical reference audit](audit/p0-reference-audit.md): all21 references checked, including unresolved/blocked retrievals.
- [Comparison protocol](audit/p0-comparison-protocol.md): proposed baselines, independent labels, cumulative attacks, calibration and statistics.
- [Reproducibility and recovery audit](audit/p0-reproducibility.md): what exists, what is missing and exact revalidation limits.
- [Artifact manifest](audit/p0-artifact-manifest.json), [historical manifest](audit/p0-historical-manifest.json), and [validation record](audit/p0-validation.json).

## P0 exit criteria

| Original criterion | Outcome |
|---|---|
| Audit claims | Completed for available repository prose and recovered older manuscript; unseen current manuscript remains unassessed. |
| Research closest prior work | Completed targeted primary-source audit; not a claim of exhaustive systematic-review coverage. |
| Recover historical results | Partially recovered; missing N50 caches, score tables and raw device measurements explicitly listed. |
| Pin historical environment | Blocked by absent historical locks/digests. Source snapshot is pinned; runtime is not. |
| Agree comparison protocol | Concrete protocol prepared; collaborator agreement is not claimed. |
| Revalidate | Source IDs, notebook records, arithmetic, diagnostic findings and document consistency checked. No new model/device experiments performed. |

## Next work in priority order

1. Obtain the authoritative current manuscript and missing per-sample results, or retire unrecoverable runs and rerun under a new immutable configuration.
2. Correct the input parser, cache provenance, metric ground truth and misleading claims before treating the pilot as a confirmatory experiment.
3. Annotate a pilot and finalize comparisons against PrivScope-/PlanTwin-style controls and attack-guided anonymization. Freeze test groups and thresholds.
4. Proceed to P1 and later controller implementation. P0 does not implement a live Jev gate or establish publication readiness.

**Defensible current statement:** the repository implements relation-assisted entity substitution and retains summaries of a preliminary exposure-proxy comparison. Stronger privacy, utility and novelty conclusions await independent, reproducible evaluation.
