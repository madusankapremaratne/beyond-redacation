# Beyond Redaction — Engineering Handover Plan

**Repo:** https://github.com/madusankapremaratne/beyond-redacation
**Context:** Research paper project. Co-authors: Moraliyage, De Silva, Mills (CDAC/La Trobe) — buy-in confirmed for this reframe (Enron-based, replacing the OULAD/SemanticGuard direction they lost confidence in). Goal: small paper with real benchmarks, published with existing co-authors.

---

## Current State (verified by reading the actual repo, not the README's description of it)

- `/validation/` — 3 notebooks, real, executed, numbers reproducible. Regex-based PII counting (email/phone/IP/forwarding-header) over 50,000 Enron records. This is solid.
- `/evaluation/` — 3 notebooks, real API calls to NVIDIA NIM, but:
  - N=3 emails, single run, no repeats
  - No automated scoring — outputs are two JSON blobs a human has to compare by eye
  - The "semantic generalization" step is one LLM prompt rewriting the whole email — **not** structured entity/relation extraction
  - This is a working proof-of-concept of the mechanism, not an evaluation
- README describes `/framework`, `/edge-runtime` directories that don't exist. Written in present tense as if built. Needs correcting or building out — don't leave it overstating repo state.

---

## Fix Immediately (mechanical, low-risk)

1. **Model deprecation.** `deepseek-ai/deepseek-v4-pro` was pulled from NVIDIA NIM ~2026-08-07. Its replacement (`deepseek-v4-flash-0731`) has reported instability/hallucination issues per NVIDIA dev forum reports.
   - Replace `deepseek-ai/deepseek-v4-pro` in `evaluation/04_Adversarial_Profile_Reconstruction.ipynb` and `evaluation/06_Adversarial_Evaluation_Comparison.ipynb` with `deepseek-ai/deepseek-r1` (or `deepseek-ai/deepseek-v3.2` as a fallback) — pick whichever gives more stable, reproducible JSON output across a handful of smoke-test runs before committing.
   - Document the exact model string + date pinned, in both notebook and README. Given how fast these catalog entries have already turned over, don't assume any model name stays valid for the life of the project.

2. **Notebook 05 header/code mismatch.** Header comment says "Simulating Edge EdgeLLM Performance via Hosted Phi-4-Mini"; code actually calls `google/gemma-4-31b-it`. Fix the comment to match reality (or vice versa if Phi-4-Mini was actually intended — confirm which).

3. **README overstatement.** Update "Repository Architecture" section to reflect what actually exists (`/validation`, `/evaluation`) vs. what's planned (`/framework`, `/edge-runtime`). Don't describe unbuilt components in present tense.

---

## Build Next (the real lift)

4. **Evaluation harness at scale.** Current N=3 single-run demo needs to become an actual benchmark:
   - Sample a held-out set (start small and verifiable — e.g. 50–100 emails — before scaling toward the compact plan's 1,000/500/150 splits)
   - Run baseline (raw) → adversarial profiler, and generalized → adversarial profiler, for every sample, not one
   - Build an automated scoring step — don't leave comparison to manual reading of JSON blobs. At minimum: does a given sensitive fact (entity, relation, project name) from the baseline reconstruction appear in the post-defense reconstruction? This is the seed of the SER/RER metrics from the compact paper plan.
   - Cache every raw response (baseline JSON, generalized text, post-defense JSON) per sample so results are auditable and reruns are cheap.

5. **Entity/relation extraction — build vs. reframe decision needed.** Current generalization step is a single holistic LLM rewrite prompt, not structured relation extraction. Two paths, not yet decided (see Open Decisions below):
   - (a) Build an actual relation-extraction step (detect entities, detect relations between them, generalize jointly) — bigger lift, supports a "relation-aware" claim honestly.
   - (b) Keep the current prompt-based approach and reframe the paper's language to match what it actually does (contextual/holistic generalization, not relation-aware extraction).
   - **Do not start building (a) until this is confirmed** — it's a meaningfully bigger scope than (b).

---

## Open Decisions (do not resolve unilaterally — flag and wait)

- RQ2 final wording: relation-aware vs. reframed to match actual mechanism (depends on item 5 above)
- Whether the 4-zone privacy architecture (from the related sovereign-learner repo) gets folded into this paper's threat model, or kept simple/binary
- Final venue target and page budget (unresolved as of last discussion)
- Ontology finalization — five-group collapse from the compact plan is provisionally fine, revisit only if scope changes

---

## Explicitly Out of Scope for Now

- Anything from the SemanticGuard/sovereign-learner repo — separate project, not to be merged in
- Multi-model benchmark (4 LLMs × 4 methods × 3 tasks) from the compact plan — that's the eventual target, not the next step. Get single-model baseline-vs-generalized scoring working and validated first.

---

## Suggested Sequencing

1. Fix model deprecation + header mismatch (items 1–2) — unblocks everything else
2. Correct README to match actual repo state (item 3)
3. Build small-scale (N=50) automated scoring harness (item 4) — this is the thing that turns "demo" into "evaluation"
4. Bring results back for a decision on item 5 (relation extraction vs. reframe) before scaling further