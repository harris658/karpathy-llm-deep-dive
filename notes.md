# Notes

Running log. One entry per working session. Newest at the top.

---

## 2026-06-09

**What we covered:** Chapter 4 complete — Concepts 2–5: Scale (batch size, loss curve, GPT-2 run, why pretraining costs millions, scaling laws, model size vs training), Base Model (internet document simulator, lossy zip file), Inference (biased coin flip, stochastic generation, remixes), Base Model Behavior (zebra demo, 2024 election hallucination, "what is 2+2" demo).
**What worked:** Deep Q&A on model size vs training (common misconception fully resolved). Scaling laws and Chinchilla ratio clicked well. Hallucination demos made the base model limitations concrete.
**What broke / open questions:** None.
**Next:** Chapter 5 — Supervised Fine-Tuning. How a base model becomes an assistant: conversation data format, what fine-tuning changes vs preserves, why it's cheap relative to pretraining.

---

## 2026-06-04

**What we covered:** Chapter 4 started — Concept 1: The Training Loop (loss, labels free from text structure, backprop runs through entire Ch.3 pipeline, pretraining vs fine-tuning distinction). Heavy Q&A: what "free labels" means, how backprop touches token IDs and embeddings, why humans don't write labels during pretraining.
**What worked:** Pretraining vs fine-tuning distinction landed well after Q&A. "Free labels" click from the table showing how one sentence contains its own labels.
**What broke / open questions:** None.
**Next:** Chapter 4 Concept 2 — Scale. 1 million tokens per step, live GPT-2 training run Karpathy shows, loss curve, why pretraining costs tens of millions of dollars.

---

## 2026-06-03

**What we covered:** Chapter 3 — Transformer Architecture, complete. All 6 concepts: (1) neural network as a stateless math function, parameters as knobs, (2) token embeddings — token IDs to vectors, (3) attention block — tokens look at each other to update context, (4) MLP block — each token processes alone, world knowledge lives here, (5) logits and softmax — raw scores to probability distribution, (6) scale — 85K demo to 405B Llama 3 to ~1T frontier.
**What worked:** Very heavy Q&A session — Harshit challenged almost every analogy. Vending machine analogy for the math function was dropped and replaced with plain explanation. Memory question was a great catch — led to the "folder of letters" explanation of context window. Parameters vs tokens confusion resolved well. "How does it decide blue scores highest?" was handled by telling him that's what the next 5 concepts answer.
**What broke / open questions:** None broken. Several analogies needed iteration to land.
**Next:** Chapter 4 — Pretraining & Inference. Training loop detail, base model inference, sampling strategies (temperature, top-k), what base model behaviour looks like before fine-tuning.

---

## 2026-06-02

**What we covered:** Chapter 2 — Tokenization, complete. All 3 concepts: (1) how conversations become flat token sequences with special tokens, (2) cognitive deficits from tokenization — ubiquitous/strawberry/dots demos + "use code" fix, (3) why character-level models aren't feasible (sequence length). Good Q&A throughout.
**What worked:** Strawberry test confirmed live — "skillfully" gave wrong answer (3 L's, correct is 4), which nailed the "patched not fixed" point. LinkedIn post drafted mid-session on the tokenization blindspot.
**What broke / open questions:** Nothing broken. Car wash question led to a Ch.6 preview (Swiss cheese model).
**Next:** Chapter 3 — Transformer Architecture. Token embeddings → attention heads → residual stream → logits.

---

## 2026-06-01

**What we covered:** Chapter 2 — Tokenization, Concept 1: how conversations become flat token sequences (special tokens im_start/im_sep/im_end, TCP/IP analogy, the 49-token demo). Good Q&A on token IDs, why IDs are preset, and why different models have different IDs for the same word.
**What worked:** Token ID concept clicked well. Q&A was focused and clear.
**What broke / open questions:** Nothing broken.
**Next:** Chapter 2 Concept 2 — cognitive deficits from tokenization: the "ubiquitous" spelling failure, the "strawberry" R-counting problem, and the dots counting demo.

---

## 2026-05-29

**What we covered:**
Chapter 1 — Pretraining Data, complete. All 8 concepts taught end-to-end:
internet → Common Crawl → filtering pipeline → tokens → BPE → training compute → next-token prediction loop → base model quirks (memorisation + hallucination).

**What worked:**
Full concept-by-concept session. Good Q&A — BPE greedy merges clicked after the worked example. Diagram exported to Excalidraw.

**What broke:**
First diagram export had blank boxes (label shorthand doesn't carry to excalidraw.com JSON). Fixed by using explicit text elements.

**Next:**
Chapter 2 — Tokenization. Deeper BPE dive, Karpathy's live TikTokenizer demos, why tokenization choices affect model behaviour (arithmetic, coding, multilingual).
