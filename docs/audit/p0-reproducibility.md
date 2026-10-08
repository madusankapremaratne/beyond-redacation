# Reproducibility and recovery audit

Date: 2026-10-08.

## What is pinned

The [artifact manifest](p0-artifact-manifest.json) identifies all46 files at Enron commit `eed6b58aa86b95cca5d5a3c0e7d9a8d0120aca68` by **Git blob SHA**, size and mode. These are Git content identifiers, not SHA-256 checksums. Historical sources/reports are separately pinned at Sovereign Learner `fe193db297e807668a96a559ea48feffbb0de903`.

These source pins do not identify the historical runtime. Mutable model aliases remain exactly as recorded: `llama3.2:latest` and `qwen3-local:latest`. Underlying weights, quantization, tokenizer, inference context and historical package lock are unknown. README's3B/7B identities are not independently verified. Requirements contain lower bounds and omit spaCy/en_core_web_sm despite their use.

## Recovered and missing evidence

| Artifact | Recovery and limitation |
|---|---|
| Nine tracked notebooks | JSON, source and saved outputs inspected.04–06 have no outputs;07–09 contain summaries. Notebook execution counts are not proof of reproducible lineage. |
| Three copies of20 benchmark samples | Committed copies share the same Git blob ID; all20 texts contain X-Origin and X-FileName. No new raw records published in audit. |
| Drive proof-of-concept files | Earlier in this task, adversarial_baseline_reconstruction.json, adversarial_protected_reconstruction.json and protected_generalized_context.txt were read. Their paired input/model/prompt lineage is unverified. No raw copies or unverified byte hashes committed. |
| Enron archive | Existing folder lists enron_mail.tar.gz (443,254,787 bytes). Not downloaded; checksum and equivalence to canonical archive unknown. [CMU source](https://www.cs.cmu.edu/~enron/) inspected for provenance; do not equate filename to version identity. |
| N50 caches and CSVs | Not recovered from checkout or targeted source searches:07_evaluation_harness_n50 and08_relation_aware_n50 result sets. No independent score recomputation. |
| Raw device measurements | Referenced macOS/iOS/Android result JSON absent. Saved aggregates only; no hardware rerun or peak-memory validation. |
| Earlier educational PDF/revision plan | Read during this task. Historical document, not authoritative current Enron paper; PDF byte hash unavailable. Revision instructions are not evidence. |
| Sovereign Learner reports |17 cloud-mode aggregate reports checked:16 simulated,1 marked real with10 biomedical queries. Selected OULAD report/code matched by commit. Full experimental provenance still missing. |
| Current manuscript and historical environment | Not recovered. Do not fabricate a lockfile or call a newly installed environment the original one. |

## Revalidation actually performed

Before the workspace interruption, a standard-library Python audit ran successfully on the pinned checkout. It parsed all nine notebooks after removing IPython shell/magic command lines; extracted and executed only pure metric/cleaner/substitution functions; reproduced header retention, SER substring, RER topology/co-occurrence and cascading-replacement counterexamples; checked sample-copy equivalence; and recomputed arithmetic. These were explicitly synthetic diagnostics, not model experiments. Python was3.12.14.

The local workspace subsequently became unavailable. Final documents and manifests were reconstructed from the recorded audit and refetched immutable GitHub sources. Revalidation after resumption independently:
- compared connector blob IDs against the pinned46-file tree;
- parsed all nine notebook JSON records and counted saved execution/output records;
- checked saved N50 summary strings and source-code conditions;
- counted retained headers in the20 committed samples and compared copy blob IDs;
- recomputed F1/MSE/AttaQ arithmetic from fetched reports or explicitly transcribed manuscript counts;
- re-read all17 historical cloud-mode reports and key simulation code;
- checked document links, claim counts and exact committed contents.

The earlier local generated manifests and audit script were not recoverable as files after interruption. They are not represented as newly rerun or committed executable tests. The committed validation JSON explicitly separates earlier Python execution from resumed source/arithmetic checks. No model calls, device benchmarks or missing-score recomputation occurred.

## Reproduce the key diagnostics locally

These are verification instructions, not a claim that every command was rerun after interruption. Check out the pinned Enron commit in an isolated directory. For notebooks07/08, parse JSON, join each code cell's source, remove IPython command lines, use Python ast to select only these FunctionDef nodes, and compile them into a namespace containing re and difflib.SequenceMatcher:

`clean_email_body, flatten_facts, fact_survives, compute_ser, compute_rer`

Select `apply_mapping` from framework/generalization.py the same way, without importing framework dependencies or invoking top-level notebook code.

| Synthetic input | Expected diagnostic result on audited source |
|---|---|
| Header lines From, X-Folder, X-Origin, X-FileName, blank line, body | Cleaner retains X-Origin/X-FileName. |
| SER baseline role “regional operations manager”, post role “manager” |1.0 due to substring match. |
| Raw relation Alice/manages/Bob; reconstructed “Person-A manages Person-B” |RER0.0 despite preserved anonymous edge description. |
| Same raw relation; post people=[Alice,Bob], linked=false |RER1.0 despite no recovered link. |
| apply_mapping("Alexandria works with Person", {"Alexandria":"Person-A","Person":"Person-B"}) |“Person-B-A works with Person-B” from sequential replacement. |

These synthetic names illustrate metric limitations; they are not observations about real people or estimates of failure prevalence.

## Required historical recovery / new-run manifest

For an independently reproducible study, obtain archive checksum and source indices, all per-item baseline/generalized/reconstruction/entity/relation/mapping files, score CSVs, exact prompts/settings, model/runtime digests, errors/retries and hardware result files. Hash all inputs and configuration into cache keys. Bind every table to a run ID and immutable manifest. Record whether outputs are real, simulated, cached or failed.

If artifacts cannot be recovered, retire the unsupported numerical claim and run a newly identified experiment. A fresh result must not be presented as recovery of the historical run.
