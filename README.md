# Karpathy: Deep Dive into LLMs like ChatGPT

**Source:** [YouTube — Andrej Karpathy (3.5 hrs)](https://www.youtube.com/watch?v=7xTGNNLPyMI)  
**NotebookLM:** `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`  
**Goal:** Understand the full LLM training stack — from raw internet data to a RLHF-aligned assistant — through hands-on experiments at each stage.

---

## Structure

Each sub-folder is one chapter of the video. Work through them in order — theory first, then code, then commit.

```
karpathy-llm-deep-dive/
├── 01-pretraining-data/          # Web scraping, Common Crawl, data quality
├── 02-tokenization/              # BPE tokenization, vocabulary construction
├── 03-transformer-architecture/  # Transformer internals, attention, FFN
├── 04-pretraining-inference/     # GPT-2 training run, base model behavior, Llama 3.1
├── 05-supervised-finetuning/     # Conversation data format, SFT training
├── 06-llm-psychology/            # Hallucinations, tool use, memory, jagged intelligence
└── 07-reinforcement-learning/    # RLHF, reward models, DeepSeek-R1, AlphaGo analogy
```

---

## Chapters at a Glance

| # | Topic | Key Concept |
|---|-------|-------------|
| 01 | Pretraining Data | How the internet becomes training data; filtering & deduplication |
| 02 | Tokenization | BPE merges; why models struggle with spelling |
| 03 | Transformer Architecture | Self-attention, residual streams, how tokens become predictions |
| 04 | Pretraining & Inference | Training GPT-2 from scratch; base model completions |
| 05 | Supervised Finetuning | From base model to assistant; conversation data structure |
| 06 | LLM Psychology | Mental models for hallucination, tool use, working memory |
| 07 | Reinforcement Learning | RLHF, reward hacking, DeepSeek-R1, thinking tokens |

---

## Approach

- [ ] 01 — Pretraining data: what goes in, how it's filtered
- [ ] 02 — Tokenization: implement BPE from scratch
- [ ] 03 — Transformer: build and inspect a minimal transformer
- [ ] 04 — Pretraining: train GPT-2 (small), run base model inference
- [ ] 05 — SFT: format conversation data, fine-tune on it
- [ ] 06 — LLM Psychology: explore hallucination / tool use / memory limits hands-on
- [ ] 07 — RL: implement a basic RLHF loop; study DeepSeek-R1 approach

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# .env is symlinked from labs/.env — add project-only overrides in .env.local
```

## Session Protocol

- **Theory before code** — every step starts with an explanation before any implementation.
- **Run it yourself** — terminal commands are given as blocks; you run them and paste output back.
- **Commit after every working step** — git log = learning log.
- **One chapter at a time** — don't start the next until current output is confirmed.
