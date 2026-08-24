# Beyond Redaction: Hybrid EdgeLLM Architectures for Query-Time Privacy

This repository contains the official experimental framework, dataset validation pipelines, and evaluation benchmarks for the *Beyond Redaction* research project. 

## 🎯 Research Core & Thesis

Traditional privacy-preserving methods focus strictly on *Instance-Level Anonymization* (protecting explicit PII data strings using regex or basic Named Entity Recognition). However, they are fundamentally blind to **Inference-Time Structural Leakage**—where cumulative, unredacted corporate context across multiple queries allows cloud providers to algorithmically reconstruct sensitive organizational matrices and employee profiles over time.

*Beyond Redaction* introduces a dual-layer defense mechanism running entirely on-device across heterogeneous edge platforms (Android, iOS, and macOS via Ollama):
1. **EdgeLLM Proxy Execution:** Traps the user query lifecycle locally, breaking the centralized collection of multi-turn transaction histories.
2. **Intent-Preserving Semantic Generalization:** Instead of brute-force token deletion (which destroys semantic utility when dealing with dense entity clusters), the local edge runtime intelligently abstracts operational concepts, entity networks, and corporate context before they exit the security perimeter. 

The cloud-bound LLM receives a highly generalized prompt that preserves processing utility while ensuring the underlying organizational infrastructure remains completely closed to reverse-engineering.



## 📁 Storage Architecture & Persistence Layer

To bridge active notebook memory spaces and survive volatile cloud container recycling across sessions, the evaluation environment enforces a persistent storage directory structure mapped directly to your Google Drive partition:

```text
📁 /content/drive/MyDrive/beyond-redaction-data/
├── 📦 enron_mail.tar.gz                     # Raw target transaction corpus archive
├── 📄 protected_generalized_context.txt     # Anonymized semantic text output from Gemma-4
├── 📊 adversarial_baseline_reconstruction.json  # Raw unprotected vulnerability profile (Notebook 04)
└── 🛡️ adversarial_protected_reconstruction.json # Post-defense metric matrix (Notebook 06)

```



## 🚀 Active Evaluation Pipelines

The downstream validation framework is driven sequentially across dedicated runtime blocks:

### 04_Adversarial_Profile_Reconstruction

* **Objective:** Establish the baseline leakage vulnerabilities of the raw corpus.
* **Mechanism:** Routes unredacted narrative sequences directly to `deepseek-ai/deepseek-r1` (pinned 2026-08-22, replacing deprecated `deepseek-ai/deepseek-v4-pro`) to construct a structural organizational map.
* **Output Artifact:** `adversarial_baseline_reconstruction.json` (cached to Drive).

### 05_Semantic_Generalization_Defensive_Layer

* **Objective:** Simulate localized text-to-text transformation via a reasoning-capable edge layer.
* **Mechanism:** Sanitizes raw communication metadata streams using regular expressions and forwards the payload to `google/gemma-4-31b-it` with latent reasoning active (`enable_thinking: True`).
* **Output Artifact:** `protected_generalized_context.txt` (cached to Drive).

### 06_Adversarial_Evaluation_Comparison

* **Objective:** Expose the protected context layer to the original profiling vector to calculate defense efficacy.
* **Mechanism:** Re-injects the sanitized text block back into the DeepSeek-R1 profiling gateway to compute the operational metric delta.
* **Output Artifact:** `adversarial_protected_reconstruction.json` (cached to Drive).

### 07_Evaluation_Harness_N50

* **Objective:** Scale the single-sample proof-of-concept above (04→05→06) into an automated N=50 benchmark — real repeated measurement instead of one manually-compared example.
* **Mechanism:** For each of 50 seeded-random Enron samples, runs baseline reconstruction → semantic generalization → post-defense reconstruction, using **local Ollama models** (`qwen3-local` for adversarial reconstruction, `llama3.2` for generalization) rather than the hosted NIM models above — chosen after live testing found the originally-planned NIM models unreliable, and because on-device inference better matches the "edge LLM" framing being evaluated. The generalization step includes two deterministic safety nets (personal-name and email-address redaction) layered on top of the LLM's own rewrite.
* **Scoring:** Structural Exposure Retention (SER) — the fraction of baseline-extracted structural facts (roles, project names, vendors/clients) that survive into the post-defense reconstruction via fuzzy string match — plus a per-sample personal-name-leak flag, since SER as an aggregate can mask a severe single-name leak.
* **Output Artifacts:** 150 cached raw JSON/text files (baseline, generalized, post-defense per sample) plus `ser_scores.csv`, all under `evaluation/results/07_evaluation_harness_n50/` (gitignored — regenerate by rerunning the notebook against a local Ollama install).
* **Status:** SER is an explicitly-labeled *starting proxy metric*, not the paper's final SER/RER definition. This arm serves as the **holistic-rewrite baseline** against which the relation-aware framework (Notebook 08, below) is measured — see that section for the head-to-head comparison and the item-5 decision this evaluation motivated.

#### N=50 results (2026-08-23)

| Metric | Value |
| --- | --- |
| Samples evaluated | 50 / 50 |
| SER — mean / median | 0.393 / 0.345 |
| SER — min / max | 0.100 / 0.909 |
| Samples fully suppressed (SER = 0) | 0 / 50 |
| Samples mostly leaked (SER > 0.7) | 6 / 50 (12%) |
| Personal-name leak rate | 5 / 46 evaluable samples (10.9%) |

No sample in this run achieved full suppression, and residual leakage clustered around two identifiable weak spots rather than being evenly distributed: structured/list-formatted emails (CC lists, personnel tables) and organization/infrastructure names, which the current single-prompt rewrite abstracts less reliably than personal names. The adversarial reconstruction model was also observed inferring identity from partial leftovers contextually (e.g. parsing a company name out of an un-redacted email domain) even where direct string redaction succeeded elsewhere in the same sample.

This pattern — name/role/org triples surviving together, and identity being re-inferred from structural leftovers — is exactly what a single undifferentiated text rewrite has no mechanism to prevent: it has no representation of the entity-relation structure it's meant to break. That gap motivated building the relation-aware framework below.

### 08_Relation_Aware_Evaluation_N50

* **Objective:** Replace the holistic single-prompt rewrite with genuine entity/relation-aware generalization, and measure it head-to-head against Notebook 07 on the **identical** 50 samples (same seed, same pool, same baseline reconstructions reused).
* **Mechanism:** Implemented in `/framework` (`extraction.py`, `generalization.py`) as an explicit pipeline rather than a single rewrite instruction:
  1. **Entity extraction** — hybrid deterministic (spaCy PERSON spans, an email-address regex shared with `validation/02`, `Lastname, Firstname` header-form detection) + one grounded LLM call typing PROJECT/ROLE/ORG/LOCATION entities and filling spaCy's known recall gaps.
  2. **Relation extraction** — one LLM call producing typed triples (`holds_role`, `hosted_at`, `manages`, ...), constrained to only connect entities already extracted (no hallucinated endpoints).
  3. **Consistent placeholder mapping** — every entity gets exactly one typed placeholder for the whole document (`"Lynn Blair"` → `"Person-A"`, all occurrences), so intra-document utility is preserved (who did what stays legible) while identity linkability is severed.
  4. **Deterministic substitution** — applied by boundary-anchored string replacement, not by trusting an LLM to follow a redaction instruction. This is the core fix for the ~11% instruction-following failure rate measured in Notebook 07.
  5. **Guarded fluency pass** — an optional LLM smoothing pass, followed by re-scrubbing every mapped entity so the smoothing step cannot reintroduce a leak.
* **Scoring:** Same SER and name-leak functions as Notebook 07 (directly comparable numbers) plus a new **Relation Exposure Retention (RER)** seed metric — the fraction of raw-text relation triples whose both endpoints co-survive into the post-defense reconstruction.
* **Output Artifacts:** 250 cached files (entities/relations/mapping/generalized/post-defense per sample) plus `relation_aware_scores.csv`, under `evaluation/results/08_relation_aware_n50/` (gitignored).

#### Holistic vs. relation-aware (N=50, 2026-08-23)

| Metric | Holistic rewrite (07) | Relation-aware (08) |
| --- | --- | --- |
| SER — mean | 0.393 | **0.209** |
| SER — median | 0.345 | **0.200** |
| SER — max | 0.909 | **0.583** |
| Personal-name leak rate | 10.9% (5/46) | **8.7% (4/46)** |
| RER (relation co-survival) | n/a | 0.000 (46/46 samples) |

Relation-aware generalization improved SER on 29/50 samples, was worse on 8/50, tied on 13/50 — mean improvement +0.184 SER on the identical sample set. RER = 0.000 across every sample with extracted relations: partly a designed consequence of the substitution guarantee (raw entity surfaces cannot appear in the generalized text, by assertion, so a raw-text triple's endpoints structurally cannot co-survive) rather than solely an independent empirical finding — it confirms the mapping mechanism holds without exception, but a deeper RER definition (can the adversary still infer relationship *structure* between anonymized placeholders?) remains future work.

**Item 5 (relation-aware vs. reframe) is resolved as of this evaluation: relation-aware generalization was built and measurably outperforms the holistic rewrite on the same 50 samples.** See `.madus/plans/Item5-Findings-N50.md` for the pre-build decision brief.

### 09_Edge_Runtime_Benchmark_Comparison

* **Objective:** Validate the paper's own thesis claim — a defense running "entirely on-device across heterogeneous edge platforms (Android, iOS, and macOS via Ollama)" — with real measurements on all three named platforms, not just macOS.
* **Scope (Phase 1, explicit):** benchmarks the **deterministic half** of the relation-aware framework only — entity detection + consistent-placeholder mapping + substitution. Relation extraction and the LLM fluency pass require bundling a mobile LLM runtime per platform (llama.cpp/MLC-LLM on iOS, MediaPipe LLM Inference/llama.cpp on Android) and are **Phase 2, not started** — this notebook does not measure them and does not imply they exist.
* **Hardware:** iOS and Android numbers are from **real physical devices**, not simulator/emulator — iPhone 16 Pro Max (iOS 26.6) and Pixel 7 Pro (Android 17), both deployed and run via `xcrun devicectl` / `adb` with results pulled back programmatically. macOS uses the same Python + spaCy detector as `framework/extraction.py`.
* **Entity detection per platform** (a deliberate difference, documented not hidden): iOS uses Apple's `NaturalLanguage` (`NLTagger`) framework — genuinely on-device, comparable in approach to spaCy. Android has no equivalent on-device general-NER API (ML Kit's Entity Extraction only covers structured entities like dates/addresses, and would need an online model download); it uses a simpler deterministic regex/heuristic detector instead, which over-redacts (privacy-safe, lower utility) rather than under-detects.
* **All three platforms ran the identical N=20 sample subset** — `edge-runtime/shared/benchmark_samples.json`, the first 20 of the same seeded 50-sample draw used in Notebooks 07/08.
* **Output Artifacts:** `edge-runtime/results/{macos,ios,android}_*.json` (raw per-sample timings), plus source: `edge-runtime/ios/` (Xcode/Swift), `edge-runtime/android/` (Gradle/Kotlin).

#### Deterministic pipeline latency (N=20, real hardware, 2026-08-24)

| Platform | Cold start (ms) | Steady-state mean (ms) | Steady-state median (ms) | Peak memory (mean, MB) |
| --- | --- | --- | --- | --- |
| macOS (Python/spaCy) | 10.5 | 19.04 | 14.18 | n/a |
| **iOS** (NLTagger, real device) | 114.0 | **1.20** | **0.83** | 72.7 |
| **Android** (heuristic, real device) | 9.5 | 16.17 | 5.83 | 50.4 |

All three platforms run the deterministic entity-detection + substitution pipeline in low single-digit-to-low-double-digit milliseconds at steady state on real hardware — confirming this half of the framework is genuinely edge-viable, not just viable in principle. iOS's higher cold-start cost is NLTagger's one-time model load; its steady-state numbers are the fastest of the three. Android's numbers reflect its simpler detector and aren't directly comparable in *what* they're detecting to iOS/macOS, only in raw substitution-pipeline throughput.

Full-pipeline on-device latency (matching Notebook 08's Mac/Ollama numbers, including relation extraction and the LLM fluency pass) remains future work — see Phase 1 scope note above.



## 📊 Dataset Validation & Reproducibility

To ensure maximum transparency, reproducibility, and architectural compliance before executing our core hybrid experiments, the data distribution is validated using open-access notebook environments.

We utilize the canonical academic distribution of the **Enron Email Corpus** to benchmark organic human communication containing sensitive structural entity features (PII, operational schedules, proprietary data structures).

* **Official Dataset Source:** [Carnegie Mellon University - Enron Corpus](https://www.cs.cmu.edu/~enron/)

### Programmatic Ingestion (Canonical CMU Stream)

You can directly stream, download, and parse the target dataset within your validation pipeline using the following standard library snippet:

```python
import os
import tarfile
import urllib.request
import pandas as pd
from tqdm import tqdm

TAR_URL = "[https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz](https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz)"
TAR_FILE = "enron_mail.tar.gz"

# Download canonical archive directly to workspace
if not os.path.exists(TAR_FILE):
    urllib.request.urlretrieve(TAR_URL, TAR_FILE)

# Stream and parse into unified validation matrix
sample_records = []
with tarfile.open(TAR_FILE, "r:gz") as tar:
    for member in tqdm(tar):
        if member.isfile() and member.name.endswith('.'):
            f = tar.extractfile(member)
            if f is not None:
                content = f.read().decode('utf-8', errors='ignore')
                sample_records.append({"file": member.name, "text": content})

df = pd.DataFrame(sample_records)

```

### Active Validation Notebooks

Select a notebook below to inspect or run the interactive data processing and distribution checks:

| Validation Task | Focus Area | Environment Link |
| --- | --- | --- |
| **01_Enron_Structural_Validation** | Verifying raw text integrity, formatting parsing, and volume distribution. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fDe7z5c2Hp1sfYZbXamLAbzJAe_QX7TE?usp=sharing) |
| **02_Privacy_Baseline_Profiling** | Statistical analysis of sensitive entities and PII density within the target corpus. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14gREjrVYZxmq0qZQsipD5Wzaw2Cm3Ioq?usp=sharing) |
| **03_Context_Window_Simulation** | Profiling token limits and formatting variations for constrained EdgeLLM runtimes. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1rNsJLGIgojbMiqJzAeG631cREI6SbRqD?usp=sharing) |

## 📈 Empirical Validation Baselines (N=50,000 Sample)

The following metrics were established during the baseline validation phase to justify the hybrid architecture and contextual window thresholds:

### 1. Text Context & Token Distributions

* **Median Character Profile:** 1,719 characters (~430 estimated tokens).
* **95th Percentile Boundary:** 8,275 characters (**2,068 estimated tokens**).
* **The Outlier Bound:** Max length observed reaches 424,440 tokens, mathematically establishing the failure mode of unmanaged localized memory allocation and proving the necessity of an active hybrid routing architecture.

### 2. Privacy Vulnerability Baseline

* **Corpus Exposure:** **100.00%** of the audited interaction proxies contained raw structural privacy entities.
* **Density Metrics:** An average of **18.7 PII entities** detected per prompt payload (Mean: 16.9 emails, 1.8 phone numbers per transaction). Maximum single-prompt risks peaked at 1,155 email entities, indicating that traditional string-replacement or token deletion masks would corrupt downstream semantic intent.

### 3. Local Hardware Operational Constraints

Simulations of hardware execution environments demonstrate the following data degradation thresholds prior to semantic optimization:

| Edge Hardware Profile | Target Context Limit | Prompt Truncation Rate | Avg. Context Information Dropped |
| --- | --- | --- | --- |
| **Ultra-Light Edge (1K)** | 1024 Tokens | 14.47% | 5.80% |
| **Standard Mobile (2K)** | 2048 Tokens | 5.10% | 1.88% |
| **High-End Mobile (4K)** | 4096 Tokens | 1.40% | 0.56% |
| **Desktop Ollama (8K)** | 8192 Tokens | 0.51% | 0.22% |



## 🛠️ Repository Architecture

**Built:**
* `/validation` — Google Colab synchronization scripts, local text validation parsers, and profile artifacts.
* `/evaluation` — Notebooks running the adversarial-reconstruction and semantic-generalization mechanism: 04–06 as a single-sample proof-of-concept against NVIDIA NIM-hosted models, 07 as an automated N=50 holistic-rewrite benchmark, 08 as the relation-aware benchmark, 09 as the cross-platform (macOS/iOS/Android) real-device latency comparison.
* `/framework` — The core relation-aware semantic generalization implementation: entity extraction, relation extraction, and consistent-placeholder generalization (`extraction.py`, `generalization.py`). Evaluated in Notebook 08.
* `/edge-runtime` — Native iOS (Swift/Xcode) and Android (Kotlin/Gradle) ports of the deterministic half of the framework (entity detection + mapping + substitution), benchmarked on real hardware in Notebook 09. LLM-based relation extraction and fluency-pass steps are not yet ported (Phase 2).

