# P0 related-work matrix

Accessed 8 October 2026. Targeted primary-source audit, not an exhaustive systematic review. No paper's experiments were independently replicated. **NR means not established from inspected material, not absent.** Abstract-only evidence cannot support detailed negative comparisons.

| ID / primary source | Evidence inspected | Mechanism and consequence |
|---|---|---|
| R01 [Beyond Memorization](https://arxiv.org/abs/2310.07298), ICLR2024 | Abstract and proceedings record | Private-attribute inference goes beyond literal memorization. Identifier removal alone is not sufficient privacy evidence. |
| R02 [Large Language Models are Advanced Anonymizers](https://arxiv.org/abs/2402.13846), v2 (2025) | Abstract | Inference-guided adversarial anonymization. Attack-guided rewriting is prior art; compare faithfully. |
| R03 [PAPILLON](https://aclanthology.org/2025.naacl-long.173/), NAACL2025 | Publisher abstract/metadata | Local/private and remote models cooperate through privacy-preserving prompt construction. Hybrid privacy orchestration is not new. |
| R04 [PREEMPT](https://www.ndss-symposium.org/wp-content/uploads/2026-s1277-paper.pdf), NDSS2026, DOI10.14722/ndss.2026.231277 | Full paper, introduction/evaluation | FPE and metric-DP token sanitization. Includes multi-turn financial-QA evaluation; contextual semantic leakage discussed as future work. Do not claim it lacks any multi-turn evaluation or import its guarantees into our code. |
| R05 [PP-TS](https://arxiv.org/abs/2306.08223),2023 | Abstract/metadata | User-defined privacy types, sanitization and restoration. Customized taxonomy/restoration already exist. Label adaptations accurately. |
| R06 [GAMA](https://arxiv.org/abs/2509.10018),2025 | Abstract/metadata | Private/public workspaces, domain rules and disproof address broader privacy reasoning. Not a pure token-masking comparator. Cumulative/graph guarantees: NR. |
| R07 [Casper](https://arxiv.org/abs/2408.07004),2024 | Abstract/metadata | Local sanitization combines explicit detection with sensitive-topic handling. Do not reduce to regex alone. Cross-turn reconstruction control: NR. |
| R08 [Truthful text sanitization guided by inference attacks / INTACT](https://nr.no/en/publication/10284282/), Applied Soft Computing2025, DOI10.1016/j.asoc.2025.114013 | Author-institution abstract | Ranks truthful abstraction candidates and selects informative replacements resistant to inference attacks. Candidate generalization plus attack-based selection is prior art. |
| R09 [PrivScope](https://arxiv.org/html/2605.16630v1),2026 preprint | Full text, especially§§IV-C–D,V | Trusted local controller, provenance/task necessity, typed abstraction hierarchies and offline-calibrated level selection; controls cross-workflow carryover. **Close overlap** with adaptive task-aware disclosure. Carryover control is not automatically a cumulative inference bound. |
| R10 [PlanTwin](https://arxiv.org/html/2603.18377v1),2026 preprint | Full text, especially§4.4/evaluation | Structured abstraction and local gatekeeper; cumulative object ledger charges newly disclosed fields. Explicitly operational, not a full information-theoretic guarantee. **Close overlap** with structural abstraction/history budgets; a ledger alone is not novel. |
| R11 [MINIM](https://proceedings.mlr.press/v306/yu26bq.html), ICML2026 | Publisher abstract | Trusted local UI-view broker scores necessity and sensitivity, then keeps/abstracts/removes content. Selective disclosure prior art; UI observations differ from narrative-email tasks. |
| R12 [STAMP](https://aclanthology.org/2026.eacl-long.61/), EACL2026 | Publisher abstract/metadata | Task relevance and sensitivity allocate token privacy budgets with directional embedding perturbation. Task-aware budgeting is not novel; its mechanism differs from heuristic exposure scores. |
| R13 [Adaptive Text Anonymization](https://arxiv.org/abs/2602.20743),v2 (2026) | Abstract; record reports ACL Findings acceptance | Prompt optimization for privacy–utility preferences. Adaptivity alone is insufficient novelty. |
| R14 [Just Ask Jev](https://arxiv.org/html/2609.29429v1),2026 preprint | Full text, especially§G.6 | Already evaluates ConfAIde, PrivaCI-Bench and PrivacyLens privacy violations. Judge performance depends on supplied evidence. No “first Jev privacy judge” claim; separate deployment-visible from oracle-secret evaluation. |
| R15 [InferDPT](https://arxiv.org/abs/2310.12214),v8 (2026) | Abstract/metadata | Specified randomized prompt perturbation and output extraction. Formal privacy requires mechanism/assumptions, not an accountant alone. |
| R16 [De-anonymizing Social Networks](https://arxiv.org/abs/0903.3276),2009 | Primary abstract | Graph topology can support re-identification after names are removed. Motivates structural evaluation without proving this project's particular vulnerability or safety. |
| R17 [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html), ICML2017 | Publisher abstract | Confidence need not match correctness; post-hoc calibration studied. Measure calibration on independent labels, not treat confidence as a privacy guarantee. |
| R18 [Selective Classification for Deep Neural Networks](https://arxiv.org/abs/1705.08500),2017 | Abstract | Rejection trades coverage for error. Report risk–coverage, local fallback and abstention. |
| R19 [The Algorithmic Foundations of Differential Privacy](https://www.cis.upenn.edu/~aaroth/privacybook.html),2014 | Author publication record | Foundational definitions/composition reference. Current deterministic substitution does not establish a DP guarantee. |
| R20 [Numerical Composition of Differential Privacy](https://arxiv.org/abs/2106.02848),2021, and [FFT accountant](https://proceedings.mlr.press/v130/koskela21a.html), AISTATS2021 | Primary abstracts/metadata | Numerical accounting composes defined privacy-loss guarantees. Correct historical PRV attribution; accounting does not make deterministic mapping private. |

## Revised research question

**Unvalidated proposal:** Can a local evidence-conditioned policy improve the measured privacy–utility–coverage frontier against task-aware abstraction and weighted-field budgets when an adversary accumulates sanitized narrative queries and reconstructs identities and relationships?

Potential contribution is a demonstrated incremental benefit under independently grounded relational labels, adaptive cumulative attackers, restricted local evidence, calibrated rejection and measured device costs. It is not the first semantic generalizer, local/cloud orchestrator, candidate selector, disclosure ledger or privacy judge. An untested combination does not establish novelty.

## Coverage and unresolved leads

The search covered prompt sanitization, inference attacks, task-aware abstraction, local/cloud orchestration, cumulative disclosure, graph re-identification, calibrated decisions and every cited work in the older manuscript. Both available search engines were used, followed by primary-source inspection. Representative actual queries:

- `"Privacy-preserving synthetic student data generation for learning analytics" Raza`
- `"Raza" "Ghassemi" "Bhatt" "student" privacy`
- `"Educational data mining and learning analytics" "e1355"`
- `"Numerical Composition of Differential Privacy" Gopi`
- `"De-anonymizing Social Networks" Narayanan Shmatikov 2009`
- `site.nature.com "Open University Learning Analytics dataset" Kuzilek`

ProSan (IEEE11352994) and Demystifying the Privacy-Utility Trade-off in LLM Interactions (arXiv2609.10992) were discovery leads, but full primary content was not successfully retrieved. Neither supports a claimed gap or performance ranking here. Revisit before submission.

Versioned URLs identify the closest full-text comparisons. Other rows specify inspected version/venue where established. Papers' own claims are not endorsements; incompatible experiments are not quantitatively ranked.
