# Notes

Running log. One entry per working session. Newest at the top.

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
