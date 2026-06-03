# Chapter 2: Tokenization — Session Notes

**Date:** 2026-06-02
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Diagram

https://excalidraw.com/#json=dhzGNxZLgnuF1hCC2LTME,0M2nw0wQC5EtnvhtbRthhQ

---

## Concept 1 — How conversations become a flat token sequence

**The problem:** A base model was trained on continuous internet text — no concept of "turns" or "roles." To build a chat assistant, you need to encode the structure of a conversation (user speaks, assistant replies) into a flat 1D sequence of token IDs.

**The TCP/IP analogy (Karpathy's):** Just like the internet solved "how do two machines talk on one wire?" by inventing packet headers (TCP/IP), developers solved "how do conversations fit in a flat token sequence?" by inventing special tokens — new tokens that never appeared in pretraining data, added purely to mark the shape of a conversation.

**Special tokens (GPT-4's format):**

| Token | Meaning |
|---|---|
| `<\|im_start\|>` | Start of a turn ("im" = imaginary monologue) |
| `<\|im_sep\|>` | Separator between role label and message content |
| `<\|im_end\|>` | End of a turn |

A two-turn conversation encoded in this format:

```
<|im_start|>user<|im_sep|>what is 2 plus 2<|im_end|>
<|im_start|>assistant<|im_sep|>2 plus 2 is four<|im_end|>
```

This entire exchange becomes **49 tokens** — Karpathy's TikTokenizer demo.

**Why the model understands it:** During fine-tuning, the model sees millions of conversations in this exact format. It learns the statistical pattern: after `assistant` + `<|im_sep|>`, generate a reply. After `<|im_end|>`, a new turn starts. The model isn't "understanding" dialogue — it's reading a structured sequence and following a trained pattern.

**Common misconception:** The model does not "know" it's talking to a user. It sees token IDs and matches patterns learned during training. The special tokens are as meaningful as any other token — their meaning is entirely learned from context.

---

## Concept 2 — Cognitive Deficits From Tokenization

**Root cause:** Models cannot read text. By the time any text reaches the model — during training or during use — it has already been converted to token IDs. The individual letters are gone, absorbed into compressed chunks. The model has never seen raw text, ever.

This creates three specific failure modes Karpathy demonstrates:

**Demo 1 — The "ubiquitous" spelling failure**
- Prompt: "print only every third character starting with the first one" — given "ubiquitous"
- Model gets it wrong
- TikTokenizer shows "ubiquitous" = **3 tokens**, not 10 characters
- The model sees 3 opaque chunks. To extract every third character, it would need to mentally unpack which letters are inside each chunk and index into them. It can't do this reliably.

**Demo 2 — The "strawberry" R-counting problem**
- Prompt: "how many R's are in strawberry?"
- State-of-the-art models confidently said **2** for years. The answer is 3.
- Two failures compounding: (1) model can't see individual characters, (2) model is bad at mental counting
- Modern models now get "strawberry" right — but only because they were drilled on that specific word in fine-tuning. The underlying problem wasn't fixed. The hole was patched.
- Tried "skillfully": model said **3 L's**. Correct answer is **4**. Same failure, unpatched word.

**Demo 3 — The dots counting failure**
- Prompt: "how many dots are below" + a block of 177 dots
- Model guesses **161**. Wrong.
- TikTokenizer shows consecutive dots get grouped — 20 dots → 1 token. The model sees a handful of IDs, not 177 individual items. Mental arithmetic on abstract IDs in a single forward pass fails.

**The fix — "use code":**
Add "use code" to any prompt requiring character-level precision. The model writes a Python snippet and delegates to the interpreter, which natively handles strings and counting. Instantly correct. Not because the model got smarter — because it stopped trying to read and started delegating.

---

## Concept 3 — Why Character-Level Models Aren't the Fix

**The obvious question:** if tokens cause all these problems, why not feed the model raw characters or bytes instead?

**Why it doesn't work — sequence length:**
Sequence length is a finite, expensive resource in neural networks. Every position costs compute.

| | Token sequences | Character sequences |
|---|---|---|
| "ubiquitous" | 3 positions | 10 positions |
| Sequence length | Short (efficient) | 3–4× longer |
| Character access | Lost | Direct |
| Current feasibility | Yes | Not at scale |

BPE is a deliberate compression deal: sacrifice character-level visibility to keep sequences short enough to train and run efficiently. Karpathy: until researchers figure out how to handle very long sequences, we remain in "the token world."

**Practical conclusion:** don't fight the architecture. For character-level tasks, use code.

---

## Key numbers

| Thing | Number |
|---|---|
| "ubiquitous" → tokens | 3 |
| "strawberry" → tokens | 2–3 |
| Karpathy's conversation demo | 49 tokens |
| Dots in counting demo | 177 (model guessed 161) |
| user token ID in GPT-4 | 428 |
| `<\|im_start\|>` token ID | 100,264 |

---

## Q&A from the session

**Q: Why doesn't "ubiquitous" become 1 token?**
A: BPE only merges frequent pairs. Common words like "the" appear billions of times → merged early → 1 token. "Ubiquitous" is rare — BPE never justified giving it its own token, so it stays as 3 chunks. Token count ≈ how common the word is. Nonsense strings fragment all the way to individual bytes.

**Q: Why do modern models get "strawberry" right now?**
A: They were drilled on it. That exact question appeared enough times in fine-tuning data that the model memorised the answer. It didn't develop the ability to count characters — it memorised the answer for that word. Try any other word and the failure reappears.

**Q: A car wash is 100ft away — walk or drive? Why might a model fail this?**
A: Not a tokenization failure — this is the "Swiss cheese" model of LLM capabilities (covered in Ch.6). Models can solve PhD-level physics but randomly fail trivial common-sense questions. Karpathy's example: "which is bigger, 9.11 or 9.9?" — models said 9.11 because Bible verse neurons fired (9:11 comes after 9:9 in scripture). The model applied the wrong context. Car wash is the same shape: model reasons about distance, misses the obvious constraint that you need the car there.

**Q: "Models convert words into tokens" — is that right?**
A: Almost. The order matters: the tokenizer runs before the model ever exists — at training time, and again instantly when you send a message. The model has never seen raw text at any point. Always token IDs, all the way through. Tighter: "Models can't read text — they only ever see token IDs. Your words get converted to numbers before the model touches them."

---

## Next

**Chapter 3: Transformer Architecture** — token embeddings, attention heads, residual stream, logits. How the model actually processes those token IDs and produces a prediction.
