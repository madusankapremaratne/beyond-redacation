# Beyond Redaction: Hybrid EdgeLLM Architectures for Query-Time Privacy

This repository contains the official experimental framework, dataset validation pipelines, and evaluation benchmarks for the *Beyond Redaction* research project. 

## 🎯 Research Core & Thesis

Traditional privacy-preserving methods focus strictly on *Instance-Level Anonymization* (protecting explicit PII data strings using regex or basic Named Entity Recognition). However, they are fundamentally blind to **Inference-Time Structural Leakage**—where cumulative, unredacted corporate context across multiple queries allows cloud providers to algorithmically reconstruct sensitive organizational matrices and employee profiles over time.

*Beyond Redaction* introduces a dual-layer defense mechanism running entirely on-device across heterogeneous edge platforms (Android, iOS, and macOS via Ollama):
1. **EdgeLLM Proxy Execution:** Traps the user query lifecycle locally, breaking the centralized collection of multi-turn transaction histories.
2. **Intent-Preserving Semantic Generalization:** Instead of brute-force token deletion (which destroys semantic utility when dealing with dense entity clusters), the local edge runtime intelligently abstracts operational concepts, entity networks, and corporate context before they exit the security perimeter. 

The cloud-bound LLM receives a highly generalized prompt that preserves processing utility while ensuring the underlying organizational infrastructure remains completely closed to reverse-engineering.

---

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


Here is the cleaned and formatted Markdown snippet, removing the excessive blank lines so it renders perfectly in your `README.md`:

### Active Validation Notebooks

Select a notebook below to inspect or run the interactive data processing and distribution checks:

| Validation Task | Focus Area | Environment Link |
| --- | --- | --- |
| **01_Enron_Structural_Validation** | Verifying raw text integrity, formatting parsing, and volume distribution. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fDe7z5c2Hp1sfYZbXamLAbzJAe_QX7TE?usp=sharing) |
| **02_Privacy_Baseline_Profiling** | Statistical analysis of sensitive entities and PII density within the target corpus. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/14gREjrVYZxmq0qZQsipD5Wzaw2Cm3Ioq?usp=sharing) |
| **03_Context_Window_Simulation** | Profiling token limits and formatting variations for constrained EdgeLLM runtimes. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1rNsJLGIgojbMiqJzAeG631cREI6SbRqD?usp=sharing) |


---

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

---

## 🛠️ Repository Architecture (Under Development)

* `/validation` — Google Colab synchronization scripts, local text validation parsers, and profile artifacts.
* `/edge-runtime` — Local deployment configuration layers for mobile (Android/iOS) and desktop (macOS via Ollama).
* `/framework` — The core semantic generalization implementation logic.
* `/evaluation` — Scripts tracking downstream utility metrics vs. information leakage rates.

```

```
