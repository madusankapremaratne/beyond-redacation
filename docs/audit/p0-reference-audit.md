# Historical manuscript reference audit

Checked 2026-10-08. Numbers refer to the recovered eight-page educational PDF. Identity/metadata verification does not validate the citing argument or experiment. Failed retrievals are explicit.

| Ref | Finding | Primary record / correction |
|---|---|---|
|1|Matched Romero/Ventura survey,2020 WIREs10(3)e1355.|[Author record](https://arxiv.org/abs/2402.07956) gives DOI10.1002/widm.1355;2024 upload is not publication year.|
|2|Unresolved exact title/author combination: Raza/Ghassemi/Bhatt, “Privacy-preserving synthetic student data generation for learning analytics,” IEEE Access2025.|Title and author searches did not identify a primary record. Obtain DOI/PDF; do not declare nonexistent or substitute a similar work.|
|3|Incorrect PREEMPT arXiv ID/authors.|[2503.01491](https://arxiv.org/abs/2503.01491) is “What's Behind PPO's Collapse in Long-CoT? Value Optimization Holds the Secret.” Use [NDSS2026 paper](https://www.ndss-symposium.org/wp-content/uploads/2026-s1277-paper.pdf), DOI10.14722/ndss.2026.231277: Amrita Roy Chowdhury, David Glukhov, Divyam Anshumaan, Prasad Chalasani, Nicholas Papernot (PDF spelling), Somesh Jha, Mihir Bellare.|
|4|PP-TS ID/title matched, author list wrong.|[2306.08223](https://arxiv.org/abs/2306.08223): Zhigang Kan, Linbo Qiao, Hao Yu, Liwen Peng, Yifu Gao, Dongsheng Li.|
|5|GAMA ID/authors wrong.|[2501.03857](https://arxiv.org/abs/2501.03857) is “Progressive Document-level Text Simplification via Large Language Models.” Correct [2509.10018](https://arxiv.org/abs/2509.10018): Hailong Yang, Renhuo Zhao, Guanjin Wang, Zhaohong Deng; version2 title ends “Disproof Mechanism.”|
|6|CrewAI repository matched; used version not identified.|[Official repo](https://github.com/crewAIInc/crewAI). Cite actual release/commit; repository existence does not prove agent execution.|
|7|OULAD publication metadata located; primary full text blocked.|[DOI10.1038/sdata.2017.171](https://doi.org/10.1038/sdata.2017.171), Kuzilek/Hlosta/Zdrahal, Scientific Data2017. Nature redirected to inaccessible sign-in infrastructure; [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5704676/) returned challenge. No unseen full-text claims relied on.|
|8|Dwork/Roth matched.|[Author page](https://www.cis.upenn.edu/~aaroth/privacybook.html),2014. Does not confer DP on this project.|
|9|IRON title/venue matched, author list/order wrong.|[NeurIPS2022](https://papers.neurips.cc/paper_files/paper/2022/hash/64e2449d74f84e5b1a5c96ba7b3d308e-Abstract-Conference.html): Meng Hao, Hongwei Li, Hanxiao Chen, Pengzhi Xing, Guowen Xu, Tianwei Zhang.|
|10|Casper identity matched.|[2408.07004](https://arxiv.org/abs/2408.07004). Select explicit version; scope broader than regex alone.|
|11|PAPILLON matched, first author's name inverted in PDF.|[NAACL2025](https://aclanthology.org/2025.naacl-long.173/): Siyan Li, Vethavikashini Chithrra Raghuram, Omar Khattab, Julia Hirschberg, Zhou Yu. Replace “L. Siyan.”|
|12|InferDPT matched, authors wrong.|[2310.12214](https://arxiv.org/abs/2310.12214): Meng Tong, Kejiang Chen, Jie Zhang, Yuang Qi, Weiming Zhang, Nenghai Yu, Tianwei Zhang, Zhikun Zhang. Current title says “Closed-box Large Language Model”; exact journal pagination not verified.|
|13|FedAvg matched.|[PMLR54](https://proceedings.mlr.press/v54/mcmahan17a.html), AISTATS2017,1273–1282. Training communication differs from inference disclosure.|
|14|Crescendo matched, threat use needs qualification.|[2404.01833](https://arxiv.org/abs/2404.01833). Multi-turn jailbreak is not a passive-reconstruction privacy bound.|
|15|Agentic-AI survey title/authors matched.|[2603.11088](https://arxiv.org/abs/2603.11088): Juhee Kim, Xiaoyuan Liu, Zhun Wang, Shi Qiu, Bo Li, Wenbo Guo, Dawn Song. Record notes USENIX Security2026 acceptance/extended version.|
|16|Code Council title/authors/DOI matched.|[Preprints.org](https://www.preprints.org/manuscript/202603.0350/v1), DOI10.20944/preprints202603.0350.v1. Label preprint.|
|17|AI4Privacy dataset exists, but is not piiranha model identity.|[Dataset card](https://huggingface.co/datasets/ai4privacy/pii-masking-200k). EXP05 needs model author/checkpoint/revision/tokenizer/config.|
|18|Official FERPA source located; no compliance determination.|[US Department of Education](https://studentprivacy.ed.gov/ferpa). Original ed.gov path failed. Metrics do not establish legal compliance.|
|19|Sovereign Learner code recovered.|[Pinned commit](https://github.com/madusankapremaratne/sovereign-learner/tree/fe193db297e807668a96a559ea48feffbb0de903). Mixed simulations, real-mode labels and local feature-ablation experiments.|
|20|AttaQ matched, author/title attribution wrong.|[IBM card](https://huggingface.co/datasets/ibm-research/AttaQ) links [Unveiling Safety Vulnerabilities of Large Language Models](https://arxiv.org/abs/2311.04124), George Kour and colleagues,2023. Card states1,402 questions. Replace “I. Bhatt et al.” using primary metadata.|
|21|Accountant title, authors, venue/pages and PRV attribution wrong.|[Koskela/Jälkö/Prediger/Honkela](https://proceedings.mlr.press/v130/koskela21a.html), AISTATS2021,3358–3366, “…Subsampled Gaussian Mechanism Using FFT.” PRV reference: [Gopi/Lee/Wutschitz, Numerical Composition](https://arxiv.org/abs/2106.02848). Neither validates deterministic mapping-table privacy.|

The PDF was not rewritten or committed. Update the authoritative manuscript bibliography using the selected publication versions. A correct reference cannot repair an unsupported experiment.
