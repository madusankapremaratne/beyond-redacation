# Claims–evidence matrix

Checked 2026-10-08. Current baseline: `eed6b58aa86b95cca5d5a3c0e7d9a8d0120aca68`. Historical baseline: `fe193db297e807668a96a559ea48feffbb0de903` in Sovereign Learner. See [manifest](audit/p0-artifact-manifest.json) for immutable file identities.

**Supported (code)** is an implementation property. **Supported (record)** means an artifact contains a result, not that it was replicated. **Provisional** has missing provenance. **Unsupported** exceeds available evidence. **Contradicted** conflicts with a concrete source or counterexample. No unseen current manuscript is purportedly audited.

## Current Enron project

| ID | Claim / location | Finding and defensible treatment |
|---|---|---|
| C01 | Prior methods only protect literal instances; README introduction | **Contradicted as a universal claim.** Attack-guided anonymization, GAMA, INTACT, PrivScope and PlanTwin cover broader mechanisms. Compare specifically named implementations. |
| C02 | Entire dual-layer pipeline runs on all three devices | **Unsupported for mobile LLM stages.** Native code and notebook09 cover deterministic detection/mapping/substitution; relation extraction and fluency are explicitly excluded. |
| C03 | Infrastructure completely closed to reverse-engineering | **Unsupported.** No cumulative or anonymous-graph reconstruction study. Remove absolute guarantee. |
| C04 | Context lengths prove routing/hardware necessity; validation01/03 | **Supported (record)** for first50,000 archive-record character summaries: median1,719 characters, estimated429.75 tokens. Characters/4 is not tokenization or a device-memory test. |
| C05 | 100% structural privacy exposure, mean18.7 entities; validation02 | **Supported (record)** as regex counts on raw messages including headers, not independently validated structural facts or unique persons. Mean email16.90586, phone1.81290, IP0.03044. |
| C06 | Truncation14.47/5.10/1.40/0.51%; validation03 | **Supported (record)** for estimated1K/2K/4K/8K budgets. Not physical hardware measurements; dropped text fraction is not semantic information loss. |
| C07 | Notebooks04–06 establish a paired proof-of-concept | **Provisional.** No saved notebook outputs. Three recovered files lack matched input/prompt/model hashes. Protected reconstruction contains detail unsupported by the recovered summary; hallucination versus version mismatch unresolved. |
| C08 | N50 is random over Enron; notebooks07/08 | **Qualified code support only:** seed42 draw from first2,000 eligible cleaned messages, each truncated to200 words. No dedup/thread split; not corpus-wide sampling. |
| C09 | Cleaner strips all headers | **Contradicted.** X-Folder ends header mode before X-Origin/X-FileName. Synthetic diagnostic confirms retention; all20 committed benchmark texts contain both fields. |
| C10 | SER mean0.393002, median0.345238; notebook07 | **Supported (record), provisional empirically.** N50 summary present, cache/CSV absent; latest saved loop uses cache. Say “saved notebook reports.” |
| C11 | SER0.209 and paired gain+0.184; notebook08 | **Supported (record), provisional empirically.**29 improved,8 worse;13 ties follows arithmetic. Same baseline reuse intended, but content hashes absent. No significance/CI claim. |
| C12 | Name leakage5/46 versus4/46 | **Supported (record)** as heuristic flags. Saved labels include a group noun and organizational token. Four samples excluded as non-evaluable; independently label persons before interpreting true leakage. |
| C13 | SER measures true factual reconstruction | **Unsupported interpretation.** Flattened nonempty string leaves matched by bidirectional substring or SequenceMatcher≥0.85 against attacker output. No truth/field validation; generic substring can score1. |
| C14 | RER0 proves structural protection | **Unsupported.** Both raw endpoints surviving is not an edge. Diagnostics score0 for preserved anonymous topology and1 for disconnected named endpoints. Saved zero is only endpoint co-survival on46 samples. |
| C15 | Grounded extraction cannot hallucinate | **Supported (code)** for substring-constrained entity additions and known relation endpoints; **unsupported** for entity type or edge truth. Endpoint existence is not relation validation. |
| C16 | Mapping disrupts relation structure | **Unsupported.** build_mapping mainly substitutes entities; selected role edges add a generic hint. No edge-suppression policy; topology/counts may survive. |
| C17 | One consistent placeholder per identity and universal raw-surface guarantee | **Unsupported universally.** Shared token aliases use first-wins assignment; sequential replacements can alter inserted placeholders. Assertion excludes surfaces contained in placeholders and disappears under Python -O. Synthetic cascade reproduced. |
| C18 | Fluency safety net prevents all leakage | **Unsupported.** It re-scrubs known mappings/emails, not missed PII or inference. Failure falls back to substitution. Test unknown entities and utility separately. |
| C19 | Existing framework is fail-closed | **Contradicted if attributed to current code.** Entity failure uses deterministic subset, relation failure returns[], and no release gate/history ledger exists. Fail-closed routing is proposed. |
| C20 | Model/environment pins exist | **Contradicted.** Mutable llama3.2:latest and qwen3-local:latest; no weight/tokenizer digests. Broad requirements omit spaCy/model; inference seed/context not fixed. Claimed underlying7B/3B identities remain unverified. |
| C21 | Cache reuse guarantees valid pairing | **Unsupported.** Sample-number/file-existence keys lack content/config hashes.08 checks only sample_000 baseline and can skip regeneration when mapping is missing. |
| C22 | Device steady means19.04/1.20/16.17ms (mac/iOS/Android) | **Supported (record), hardware provenance provisional.** Raw JSON absent.20 documents include first cold sample; steady values use19 different texts, not repeated measurements per input. |
| C23 | Peak memory72.7MB/50.4MB (iOS/Android) | **Contradicted label.** Post-call memory readings, not instrumented peaks; resident memory versus PSS differs. No direct memory-efficiency ranking. |
| C24 | Android heuristic over-redaction is privacy-safe | **Unsupported.** No independent recall validation; over-redaction does not exclude missed entities. |
| C25 | Utility preserved and method superiority resolved | **Unsupported beyond design intent/proxy comparison.** No recovered labeled downstream Enron task or human utility evaluation. |
| C26 | Cumulative privacy/calibrated Jev selection validated | **Unsupported/proposed.** Research plan only. Jev already evaluates privacy violations; hosted judgment cannot protect its own inputs from its provider. |

## Earlier educational manuscript

Source: recovered eight-page “Beyond Redaction: Intent-Preserving Semantic Generalization for Inference-Time Privacy in LLM Based Learning.” This is OULAD/Sovereign Learner work, not the current Enron implementation. Its revision plan is not empirical evidence. All seven experiment families and major methodological conclusions are represented below.

| ID | Claim / manuscript location | Finding and required action |
|---|---|---|
| H01 | Four-zone CrewAI design, fail-closed execution,34,018 lexicon types and threshold.85; methods | **Provisional.** Identify actual executing commit, lexicon hash and boundary traces. Historical experiments include simulated routing; do not transfer architecture claims across repos. |
| H02 | EXP01 n300, IPP99.8%, ZLR99.3%, STS.342, judge.619,292.86ms/12.2s; TableIV | **Unsupported by matched recovered run.**17 top-level cloud-mode reports:16 simulated,1 labeled real (n10 biomedical, utility0). None identifies the claimed n300 run; real-mode label does not exclude exception fallback. |
| H03 | IPP establishes privacy from cloud provider | **Unsupported interpretation.** Defined using entity absence in cloud response; provider already sees its input. Measure transmitted payload and adversarial recovery. |
| H04 | Leakage similarity.119 proves infeasibility;99.8% is a lower bound; discussion | **Unsupported.** Embedding distance and exact-match omission do not bound inference. Remove infeasibility/lower-bound claims. |
| H05 | EXP02a F1.910 vs.652,25.8pp; TableV | **Conflicts with available report; lineage unresolved.** OULAD report20260122_112323 records .9100025069 vs.8106653620,9.9337145pp,8,769 test rows each. Both are local random forests using12 versus3 features, not cloud LLM inference. |
| H06 | EXP02b hybrid MSE247.01 vs357.51,−30.9%, R².346/.053 | **Supported (record), interpretation unsupported.** Rounded values match; code uses local regression feature subsets. Feature ablation does not validate a hybrid LLM deployment. |
| H07 | EXP02c48.4% fewer interactions,+17.1pp accuracy,n3,538 | **Contradicted as measured transfer benefit.** Cold-start accuracy fixed.5; transfer reduction uses min(.6,first_course_clicks/1000); accuracy assigned.75/.6 using matching final outcomes. Label assumption-driven simulation; require held-out outcome-blind predictions. |
| H08 | EXP03 IP.968/.964/.962 across3 models proves architectural model independence | **Unsupported by matched raw runs and overgeneralized.** Recover per-query results/configs; three models do not establish universality. |
| H09 | EXP04 n80,100% routing; TableVII | **Unsupported as independent accuracy.** PDF notes deterministic labels. Historical exp04 calls simulated pipeline and assigns expected zone; mock-metric fallback exists. Require real traces/blind labels. |
| H10 | EXP05 n50 superiority over PREEMPT/PP-TS/GAMA/piiranha; TableVIII | **Unsupported by matched baseline/output lineage.** Faithful implementations/configs absent from recovered comparison evidence. Dataset citation is not piiranha model identity. Explain no-protection IPP.52 versus redaction.48. |
| H11 | EXP06 AttaQ1,402, ARR96.58%, AA94.8%, PII resistance100%; TableIX | **Arithmetic supported only:**1,354/1,402=96.5763%. Raw traces missing. PII neutralized22/23=95.65%;100% architectural attribution among blocked cases does not mean100% all-case resistance. |
| H12 | EXP07 v2 IP99/question recall100/bleed0 versus88/65/12; TableX | **Unsupported by matched raw run.** Table lacks sample count;1.2/2.5s timings lack reproducible provenance. |
| H13 | PRV accountant on mapping table supplies formal guarantee;§V-C | **Unsupported prescription.** No adjacency, randomized mechanism or per-release privacy-loss bound. Accountant citation also wrong; deterministic ledger is not DP. |
| H14 | Per-query results establish guarantees that can inform cross-turn protection | **Unsupported.** Manuscript acknowledges unaddressed cross-turn inference; Crescendo is a jailbreak reference, not a passive-reconstruction guarantee. |
| H15 | Bibliography supports comparison/theory | **Partly contradicted.** Two wrong arXiv IDs, wrong author lists/accountant metadata, one unresolved paper. See [reference audit](audit/p0-reference-audit.md). |

An available artifact conflicting with a manuscript is not proof that no other run exists. It means the claim cannot be verified from the supplied lineage. Missing evidence must be recovered or the claim revised.
