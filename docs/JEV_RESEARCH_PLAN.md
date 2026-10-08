# Beyond Redaction: JEV Research and Implementation Plan

Date: 8 October 2026

Branch: `jev`

Reviewed baseline: `c7f052b7c37321c199f79c79275763796d227c48` (`main`)

Status: P0 evidence audit completed on 8 October 2026 with unresolved readiness gates. See [audit report](P0_EVIDENCE_AUDIT.md), [claim matrix](claims-evidence-matrix.md), [related work](related-work-matrix.md), and [refined comparison protocol](audit/p0-comparison-protocol.md). Original experiment caches/model digests and the authoritative current manuscript remain missing. No new model experiments or live Jev implementation are implied.

P0 changes the novelty assessment: PrivScope already covers task necessity and abstraction hierarchies; PlanTwin already covers structured abstraction and cumulative disclosure budgets. A new combination is not sufficient novelty. The proposed study must demonstrate incremental value against these close baselines, with independently grounded graph leakage, task utility and release coverage. The refined P0 protocol governs subsequent study design where it differs from this initial plan.

## 1. Decision and intended contribution

Investigate **evidence-aware, selective disclosure for relation-preserving query generalization**. Use TypeSafe's Jev as one replaceable decision model, initially in offline experiments on approved public benchmark material. Keep private extraction, rewriting, identity mappings, and release enforcement local.

The research question is whether a controller can select the least destructive transformation that preserves the information needed for a task while limiting the sensitive organizational facts inferable from accumulated disclosures. The controller must be able to keep a request local or abstain when available evidence cannot support a release decision.

Adding Jev, a typed interface, a confidence threshold, or another agent is not by itself a research contribution. The candidate contribution is the combination of a defined disclosure policy, cumulative evidence accounting, adaptive transformation, and an independently evaluated privacy–utility trade-off. Novelty remains a hypothesis until a targeted prior-art review and held-out experiments support it. MDPI is a publisher; acceptance depends on the selected journal and reviewers, not on using a particular model.

Working paper framing: **Beyond Redaction: Evidence-Aware Control of Structural Disclosure in Hybrid Edge–Cloud LLM Systems**. Treat this as a working title, not an instruction to rename the existing paper.

## 2. Repository-grounded starting point

| Existing component | What is present | Required follow-up |
| --- | --- | --- |
| `framework/extraction.py` | Local spaCy/regex detection and Ollama entity/relation extraction | Annotate extraction recall and relation correctness; grounding endpoints does not prove a relation is true |
| `framework/generalization.py` | Consistent mapping, deterministic replacement, optional local fluency rewrite and re-scrubbing | Add task-conditioned abstraction levels and explicit release checks; mapped-surface removal does not establish semantic privacy |
| Evaluation notebooks 07/08 | Paired N=50 holistic and relation-aware experiments | Reproduce before extension; retain original methods as baselines |
| Sampling in 07/08 | Seeded draw of 50 from the first 2,000 qualifying archive records | Replace archive-order convenience sampling for the confirmatory study; deduplicate and split by conversation/person groups |
| SER/RER | Fuzzy fact survival and raw relation endpoint co-survival | Keep as historical proxies; add independent semantic and graph reconstruction metrics |
| Notebook 09 / `edge-runtime/` | Deterministic native mobile pipeline comparison | Do not label these results full mobile LLM/Jev execution; platform detectors differ |
| Dependencies and outputs | Broad dependency bounds, model aliases, result directories ignored | Freeze environment/model digests and publish an artifact manifest with hashes and regeneration instructions |

README-reported N=50 results (not rerun for this plan): mean SER 0.393 for holistic rewriting and 0.209 for relation-aware processing; name leaks 5/46 versus 4/46; RER 0 for the 46 samples with relations. RER here checks endpoint co-survival, not whether an adversary recovers relationships among anonymous people. It cannot substantiate zero structural leakage.

No standalone manuscript was found in the tracked checkout. A manuscript-to-evidence audit remains a prerequisite to submission. Do not import claims from earlier educational-privacy work into this Enron study without matching data, code, and results. Audit the README's absolute claims about reverse engineering and wholly on-device execution against the implemented scope.

## 3. Research questions and falsifiable hypotheses

| ID | Question | Evidence needed |
| --- | --- | --- |
| RQ1 | Does adaptive disclosure reduce sensitive fact reconstruction versus fixed generalization at comparable utility and release coverage? | Paired held-out privacy–utility curves and uncertainty intervals |
| RQ2 | Does explicit evidence-sufficiency assessment improve on confidence-only gating? | Missing, contradictory, truncated and shifted-context cases; false-release and correct-abstention rates |
| RQ3 | Does a local history ledger reduce cumulative leakage beyond independent per-query decisions? | Real linked conversation sequences, controlled sequence tests, and history-off ablation |
| RQ4 | Does Jev add value over deterministic rules and a local LLM judge? | Matched judge inputs, identical candidates/controller, independent labels, accuracy/calibration/latency/cost comparisons |

H1: adaptive selection improves the privacy–utility frontier over fixed processing. H2: explicit sufficiency checks reduce unsafe release at matched coverage. H3: history-aware control reduces incremental sensitive fact recovery. H4: Jev offers a measurable quality or efficiency advantage. All four are testable hypotheses, not assumed outcomes; report null and negative findings.

## 4. Threat model and disclosure policy

The adversary is a cloud recipient that retains all material sent to it across a defined session and attempts to reconstruct protected facts. Evaluate both transcript-only attacks and attacks with a fixed auxiliary-information collection. Keep the local device, mapping store and local ledger outside this adversary's access. Device compromise is out of scope.

Define a policy per task before constructing candidates: allowed task facts, forbidden identity/organization facts, and forbidden relationship types. Examples include identity–role links, reporting lines, project membership, vendor associations and cross-session identity linkage. Some relationships are needed for a task; preserving an authorized relationship is not automatically a privacy failure. Cases requiring a forbidden fact must be handled locally or refused, not solved by quietly weakening policy.

Record exactly which facts are available in auxiliary knowledge. Public Enron information may already occur in model training: distinguish prior knowledge from evidence acquired through the transcript using a no-transcript baseline and separately labelled counterfactual controls. No claim of differential privacy or a formal privacy guarantee is planned.

### Hosted-judge boundary

A candidate sent to hosted Jev is already disclosed to a cloud provider, even if Jev subsequently rejects it. Removing names does not remove structural information. Sending several candidates can reveal more than sending the final candidate alone.

Use these explicitly separated modes:

1. **Offline research mode (initial Jev implementation):** evaluate Jev with approved public benchmark inputs. A paired raw/generalized comparison may be used only in a separately labelled offline arm. It does not demonstrate an on-device gate or protection from the judge provider. Count all candidate transmissions when evaluating the combined-recipient exposure.
2. **Private runtime mode (core deployment design):** a local rules/LLM judge sees local originals and candidates; only the selected, locally approved result leaves the device. Jev remains an offline comparator. A local model trained with Jev assistance is optional later work and must be independently evaluated; it is not Jev and does not inherit its properties.
3. **Optional hosted deployment experiment:** permit only inputs already approved locally for disclosure to that recipient. Jev can impose an additional restriction but cannot authorize the first disclosure to itself. Report trust assumptions, data sent, and exposure to each recipient separately. Do not send mappings, raw private queries, sensitive graph ledgers, or raw/generalized pairs.

No verified on-device Jev runtime is assumed. Remote advice must never override a local hard deny. Raw context, derived features, hashes and logs all require review for linkability; calling a feature “metadata” does not make it safe.

## 5. Proposed pipeline

1. **Local intake:** assign session/task IDs; check policy; identify task-critical facts and prohibited facts. Sanitize the task instruction itself before any permitted external request.
2. **Local extraction:** reuse the existing entity/relation pipeline; retain uncertainty and evidence spans locally.
3. **Candidate generation:** construct a small ordered set: L1 current typed substitution; L2 coarsened roles/organizations/dates and selected relation suppression; L3 a minimal task-specific abstract summary. Keep local-only handling as an explicit alternative. L2/L3 are new work, not existing features.
4. **Independent checks:** validate every candidate for raw surfaces, missed PII, policy violations and task-critical omissions. Review the union of prior disclosures and the candidate, not only the latest message.
5. **Decision assessment:** use one interchangeable judge to assess atomic privacy, task-sufficiency and ambiguity questions. Run Jev only in the modes allowed above.
6. **Deterministic selection:** select the least destructive eligible candidate. If none passes, route to local execution; if unavailable or policy disallows it, abstain. Bound regeneration to at most two additional attempts and log the reason for termination.
7. **Release and ledger:** revalidate the exact serialized payload; record what actually crossed each boundary. Commit ledger state only on confirmed transmission and track ambiguous delivery failures conservatively. Reconstruct any permitted identity references locally after the response arrives.

The ledger stores local canonical facts and approved disclosure history; placeholder identifiers rotate across unrelated sessions. Within-session consistency is task-dependent and is tested for its linkage cost. The history-risk score is an empirical controller signal, not an additive privacy budget with mathematical guarantees.

### Jev decision contract

Official documentation describes Choice, Score and Noul typed decisions [S1]. Start with the following application-level schema; verify exact SDK syntax in implementation rather than treating these names as vendor fields.

| Question | Output design | Intended use |
| --- | --- | --- |
| Does the visible evidence expose a prohibited identity–role link? | Atomic Noul per protected category | Estimate risk against the declared rubric |
| Is the visible evidence sufficient to answer this task? | Choice: sufficient / insufficient / contradictory | Distinguish missing evidence from disagreement |
| Which permitted handling mode fits this case? | Choice: candidate eligible / stronger abstraction / local only / abstain | Advisory classification; deterministic policy makes the final decision |
| How much task-critical information remains? | Score with explicit ordinal rubric | Diagnostic utility estimate, checked against actual downstream performance |

Questions evaluated within one call must be independent; compose dependent decisions in code or separate calls. Store full answer distributions and missing/error states. Jev's Choice/Score confidence summarizes a distribution; it is not an independently measured probability that releasing a request is safe. Noul has no separate confidence field [S2]. Calibrate question probabilities against development labels, and freeze thresholds before test evaluation.

Eligibility is a conjunction: hard checks pass, assessed protected-fact risk is below the development-selected threshold, task sufficiency meets its threshold, history policy passes, and no required decision is missing. Never multiply risk probabilities as though independence were established. Contradiction, timeout, invalid output, unavailable model, or an unknown policy version causes local handling/abstention. An error must never be converted into a low-risk score.

## 6. Data, labels and experimental design

### Data and splits

- Reproduce the existing 50-sample experiment as a historical pilot, not as a new test set.
- Prepare a target of **300 independent Enron conversation groups** for the first expanded study: 100 development, 50 calibration and 150 held-out test groups. These are planning targets, not obtained data or a power guarantee. Use pilot variance and cluster size to choose the final sample count before opening test outcomes.
- Sample across the archive, remove duplicate/quoted email overlap, and use conversation plus identity-component grouping to avoid split leakage. If identity components make this infeasible, document the compromise and add a separate unseen-person split; never silently split duplicates across partitions.
- Use up to five turns per group where genuine thread linkage is supported. Treat missing turns as missing. Separately create controlled counterfactual and topology stress cases, explicitly marked synthetic; do not present invented organizational facts as Enron observations.
- Include structured lists, signatures, aliases, email domains, rare role combinations, paraphrases, obfuscated identifiers, context truncation, instruction attacks and contradictory evidence.
- Version sample IDs, source archive paths/checksum, inclusion/exclusion rules and group splits. Review redistribution permissions and privacy exposure before publishing any corpus-derived artifact; public availability is not blanket permission to republish personal data.

### Independent ground truth

Two annotators label a shared subset before finalizing the rubric, then independently label the confirmatory set with adjudication. Label source-supported entities/relations, allowed/forbidden facts, task answers and evidence sufficiency. Permit “unknown/not established.” Report agreement and disagreements. Keep annotations hidden from judges, generators and attackers during inference.

Do not use the defense extractor's triples, baseline attacker output, or Jev verdicts as the sole gold standard. Evaluate identity recovery and topology recovery separately. Ground-truth organizational structure is limited to facts supported by the chosen documents/auxiliary material, not a presumed complete Enron chart.

### Experimental arms

| Arm | Transformation and controller | Purpose |
| --- | --- | --- |
| B0 | Raw context, offline authorized benchmark only | Utility/leakage reference |
| B1 | Deterministic PII masking | Basic privacy baseline |
| B2 | Existing holistic rewrite (07) | Published-in-repository baseline |
| B3 | Existing fixed relation-aware generalization (08) | Primary defense comparator |
| B4 | Same adaptive candidates + deterministic rules | Separate adaptive transformation from judge capability |
| B5 | Same adaptive candidates + local structured-output LLM judge | Deployable private-runtime comparison |
| J1 | Same adaptive candidates + Jev in offline mode | Isolate decision-model effect |
| O1 | Best candidate under gold labels, offline only | Diagnostic oracle upper bound, never a deployable method |

For B4/B5/J1, hold candidate pool, task policy, generator, history availability and selection code fixed. Compare both shared minimized inputs and, separately, full local/offline inputs; different information access must not be mistaken for model superiority. Add a simple supervised classifier if sufficient development labels exist. Select relevant published privacy/generalization baselines after the literature review and document unavailable implementations.

Run two different attacker model families, including one independent of the defense/judge family. Freeze attacker prompts, auxiliary knowledge, output schemas and query budgets. Measure targeted fact recovery, open-ended graph reconstruction and cross-turn linkage. Repeat stochastic arms at least three times where feasible; repeated calls are not independent documents.

Core ablations: history on/off; adaptive/fixed level; sufficiency check on/off; raw/recalibrated probabilities; identity-only versus relation-aware checks; fluency pass on/off. Use development results to bound the confirmatory matrix and predeclare primary comparisons before testing.

## 7. Metrics and analysis

| Dimension | Required measurements |
| --- | --- |
| Direct leakage | Source-annotated PII span recall in transmitted content; severe identity leak rate |
| Semantic leakage | Precision/recall/F1 of attacker-recovered forbidden facts against independent labels; false inferred facts reported separately |
| Structural leakage | Typed-edge and topology recovery after evaluator-only node alignment; separate identity-linked edges from anonymous topology |
| Cumulative leakage | Unique prohibited facts recovered by turn, marginal recovery over previous turns, cross-session link accuracy; include all visible candidates per recipient |
| Utility | Held-out task correctness/F1, evidence-supported answers and blinded rubric-based summary quality; embedding similarity only secondary |
| Decision quality | Unsafe-release rate, false block rate, sufficiency classification, correct abstention; distinguish unsafe/all releases from unsafe/all unsafe inputs |
| Calibration | Brier score, reliability plots, ECE with declared bins; raw and calibrated probabilities; score-rubric agreement separately |
| Coverage | Released/all requests, local fallback and abstention rates, successful tasks/all requests and success among released requests |
| Runtime | End-to-end p50/p95 including extraction, candidates, judge, retries, network and fallback; peak memory; cold/warm runs; measured API usage/cost |

Primary outcome: paired forbidden-fact recovery difference against B3 at matched release coverage with a predeclared downstream-utility non-inferiority margin. Choose and justify the numeric margin and risk tolerance using development data and the task rubric before test results are visible. If matching coverage cannot be achieved, report the full curves and the limitation instead of selecting a favorable point.

Use paired cluster bootstrap confidence intervals by conversation/identity group (target 2,000 resamples), not per turn. Predeclare one primary comparison, adjust exploratory multiple comparisons where applicable, and report effect sizes. A small or zero observed leak count requires an uncertainty bound, not a “zero leakage” claim. Missing/failed requests remain in coverage and failure denominators. Report undefined metrics as undefined, including groups with no protected facts.

## 8. Implementation work packages and acceptance criteria

Indicative schedule: eight weeks after data, API access and annotation capacity are available. Dependencies determine progress; dates are estimates.

| Phase | Timing | Work and planned files | Exit criterion |
| --- | --- | --- | --- |
| P0: evidence audit | Audit completed 8 Oct 2026 | Claim/reference/related-work matrices, artifact manifests, reproducibility audit and proposed protocol delivered | Available claims audited; historical runtime pinning, missing result recovery, current manuscript and collaborator protocol agreement remain unresolved |
| P1: labels/protocol | Weeks 1–2 | `evaluation/protocols/jev_protocol.md`, manifests, annotation guide, split validator | Pilot adjudicated; no duplicate/thread overlap; metrics and held-out analysis frozen |
| P2: controller | Weeks 2–3 | `framework/decision_schema.py`, `framework/disclosure_policy.py`, `framework/disclosure_ledger.py`, `framework/candidate_generation.py`, `framework/controller.py` | Deterministic rules path works with local fixtures; no release on missing required evidence |
| P3: judge adapters | Weeks 3–4 | `framework/judges/base.py`, `rules.py`, `local_llm.py`, `jev.py`; explicit offline/hosted modes; optional dependency and environment examples | Adapters preserve typed distributions/errors; minimized payload contract verified; Jev version recorded |
| P4: evaluation | Weeks 4–5 | `evaluation/run_jev_benchmark.py`, `evaluation/metrics/structural.py`, `utility.py`, `calibration.py`; notebook 10 as a thin report | End-to-end pilot reproduces from manifest; no test-label access; independent attack scoring works |
| P5: held-out study | Weeks 5–7 | Locked run configurations, raw-output hashes, paired results, ablations and audit logs | All predefined arms complete or failures reported; measured CIs/cost/latency; test set used once |
| P6: paper package | Week 8 | Evidence-linked tables/figures, limitations, artifact instructions and manuscript revision | Claims match actual data and deployment mode; no unsupported on-device or novelty claims |

P0 audit documents and manifests have now been added; P1–P6 implementation files remain planned additions. Keep notebooks 07–09 reproducible. Add reusable Python modules and let new notebooks call them. Check dependencies such as spaCy and its model explicitly; they are used in code but not fully represented in the current requirements list.

Cache keys must include dataset/item hash, split, candidate, prompt/schema/policy version, model identifier/digest, settings, history hash and pipeline revision. Record request/response times, retries, token usage when provided and unknown cost when unavailable. Do not infer an immutable model from `latest`. Private mappings and raw private logs stay local and excluded from git; publish only reviewed artifacts and regeneration metadata.

### Required implementation checks

- Regression cases for aliases, punctuation, overlapping names, placeholder collisions, email ownership and fluency reintroduction.
- End-to-end network-capture checks: local-only mode performs no remote call; forbidden fields and mappings never enter an external payload; an unsafe hosted candidate is rejected before transmission.
- Controller cases for timeout, rate limit, malformed/missing probabilities, contradictory evidence, unsupported model, exceeded retry budget and stale history.
- Injection tests in source text and candidate text: an instruction to choose “safe” must not change deterministic policy or bypass validation.
- Metric sanity cases where all names are removed but the sensitive graph is preserved; where an attacker invents a graph; and where an allowed relation remains intact.
- Split isolation and cache invalidation checks; aggregate counts reconcile with attempts, successes, skips, fallbacks and failures.

Jev access is a P3 dependency, not a reason to block P0–P2. If unavailable, continue rules/local-LLM work and mark Jev evaluation unexecuted. Never substitute mocked Jev responses into experimental result tables.

## 9. Novelty and submission gates

Before asserting novelty, search primary papers on task-aware anonymization, semantic generalization, graph/relational privacy, cumulative inference, adaptive disclosure, selective prediction and privacy-aware routing. Maintain query/date/source records and a comparison matrix covering threat model, task dependence, multi-turn exposure, decision model, independent gold labels and privacy–utility analysis.

A concrete overlap is **Just Ask Jev / RLCDAlignBench**, whose September 2026 preprint includes privacy-violation detection and varies judge context [S4]. Therefore “Jev as a privacy judge” must not be claimed as new. P0 has now inspected the full Jev paper, especially §G.6, alongside PrivScope and PlanTwin; no replication is claimed. Our proposed distinction—cumulative disclosure control before release with independently measured graph leakage and task utility—still needs validation against broader prior art.

Proceed to a stronger methodological paper only if adaptive control yields a reproducible improvement over fixed generalization and rules/local-LLM controllers under matched conditions. If Jev adds only speed/cost value, report that as an engineering finding. If it adds no value, retain the broader privacy study and report the null result. If gains rely on sending protected content to a hosted judge, they do not validate the private-runtime claim.

Submission checklist: obtain the actual manuscript; choose a specific journal and verify its current scope; map every quantitative statement to a versioned result; distinguish experiments from targets; report public-corpus memorization, annotation uncertainty, proprietary API drift, domain limits and mobile scope. Do not claim that Enron results generalize to education, HR, medical or private enterprise data without additional evidence. This plan does not establish that the work is already novel enough for acceptance.

## 10. Verified starting sources

Sources checked on 8 October 2026. Documentation is mutable; capture versions/access dates with implementation and refresh the literature review before submission.

- **[S1]** TypeSafe, [Jev introduction](https://docs.typesafe.ai/introduction): typed Choice, Score and Noul decisions; independent questions evaluated against shared state.
- **[S2]** TypeSafe, [Confidence](https://docs.typesafe.ai/confidence): probability distributions versus derived confidence, and Noul's probability-only response.
- **[S3]** TypeSafe, [Quick start](https://docs.typesafe.ai/introduction/quickstart): hosted API request structure. API access and deployed model version must be checked during implementation.
- **[S4]** Guo et al., [Just Ask Jev: Reinforcement Learning for Calibrated Decisions as a Zero-Shot Detector of AI Alignment Failures](https://arxiv.org/abs/2609.29429), preprint, 24 September 2026: overlapping Jev privacy-judge evaluation; not proof of this proposed controller's effectiveness.
- **[S5]** Repository sources at the baseline commit: [generalization](../framework/generalization.py), [extraction](../framework/extraction.py), [README](../README.md), [notebook 07](../evaluation/07_Evaluation_Harness_N50.ipynb), [notebook 08](../evaluation/08_Relation_Aware_Evaluation_N50.ipynb), [notebook 09](../evaluation/09_Edge_Runtime_Benchmark_Comparison.ipynb).

**Next implementation step:** resolve the documented evidence blockers and finalize the P1 labeled pilot protocol before adding a live Jev gate. The P0 audit does not initiate paid inference, upload datasets, or change runtime behavior.
