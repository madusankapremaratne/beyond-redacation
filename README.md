Here is the correctly formatted Markdown block for your `README.md`. The broken code block syntax from the snippet has been fixed, and trailing spacing has been cleaned up for seamless rendering on GitHub.

```markdown
# Beyond Redaction: Hybrid EdgeLLM Architectures for Query-Time Privacy

This repository contains the official experimental framework, dataset validation pipelines, and evaluation benchmarks for the *Beyond Redaction* research project. The core framework introduces an intent-preserving semantic generalization layer running entirely on-device across heterogeneous edge platforms (Android, iOS, and macOS via Ollama) to secure cloud-bound LLM queries.

---

## 📊 Dataset Validation & Reproducibility

To ensure maximum transparency, reproducibility, and architectural compliance before executing our core hybrid experiments, the data distribution is validated using open-access notebook environments. 

We utilize the **Enron Email Corpus** to benchmark organic human communication containing sensitive structural entity features (PII, operational schedules, proprietary data structures). For clean, reproducible data validation, we use the structured Hugging Face mirror:

* **Dataset Repository:** [Hugging Face - corbt/enron-emails](https://huggingface.co/datasets/corbt/enron-emails)

### Programmatic Ingestion (Google Colab)
You can directly stream and parse the target dataset within your validation pipeline using the following snippet:

```python
!pip install datasets pandas
from datasets import load_dataset

# Stream the dataset to bypass local storage constraints in edge simulations
dataset = load_dataset("corbt/enron-emails", split="train")

# Convert to Pandas DataFrame for downstream validation profiling
df = dataset.to_pandas()
print(f"Successfully loaded {len(df)} records for validation.")

```

Here is the updated Markdown block with the Google Colab badge syntax fixed.

The issue usually happens if the raw HTML image tag or markdown link formatting has a typo or gets stripped by GitHub's markdown renderer. Replacing them with direct standard Markdown image links resolves the issue:

### Active Validation Notebooks
Select a notebook below to inspect or run the interactive data processing and distribution checks:

| Validation Task | Focus Area | Environment Link |
| :--- | :--- | :--- |
| **01_Enron_Structural_Validation** | Verifying raw text integrity, formatting parsing, and volume distribution. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](YOUR_COLAB_LINK_HERE) |
| **02_Privacy_Baseline_Profiling** | Statistical analysis of sensitive entities and PII density within the target corpus. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](YOUR_COLAB_LINK_HERE) |
| **03_Context_Window_Simulation** | Profiling token limits and formatting variations for constrained EdgeLLM runtimes. | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](YOUR_COLAB_LINK_HERE) |

---

## 🛠️ Repository Architecture (Under Development)

* `/validation` — Google Colab synchronization scripts and local text validation parsers.
* `/edge-runtime` — Local deployment configuration layers for mobile (Android/iOS) and desktop (macOS via Ollama).
* `/framework` — The core semantic generalization implementation logic.
* `/evaluation` — Scripts tracking downstream utility metrics vs. information leakage rates.

