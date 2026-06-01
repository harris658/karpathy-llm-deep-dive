# Chapter 2: Tokenization — Session Notes

**Date:** 2026-06-01
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

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

## Q&A from the session

**Q: What exactly are the 49 tokens — why so many for such a short exchange?**
A: Every word, space, newline, and special delimiter becomes its own token (or part of one). The special delimiters alone account for 8+ tokens before any actual words. `<|im_start|>` × 2 (once per turn) + `<|im_sep|>` × 2 + `<|im_end|>` × 2 + role labels + newlines + every word in both messages = 49 total.

**Q: Why multiply by 2 for the special tokens?**
A: Two turns in the conversation — user turn and assistant turn. Each turn uses the full `<|im_start|> [role] <|im_sep|> [message] <|im_end|>` template. So each special token appears once per turn × 2 turns = 2 total. A 4-turn conversation would have each special token appear 4 times.

**Q: What is a token ID?**
A: The model only works with numbers, not text. Every token in the vocabulary is assigned a permanent number — its ID. `user` = ID 428 in GPT-4's tokenizer. `<|im_start|>` = ID 100264. The model receives these numbers; it never sees raw text. It learned what each ID means through training.

**Q: Are IDs preset / fixed?**
A: Yes. IDs are fixed when the tokenizer is built — BPE runs, the vocabulary is assembled, each token gets an ID sequentially. Special tokens are added at the end (hence the high IDs like 100264+). The IDs never change during use. They're baked in at build time.

**Q: Do different models have different IDs for the same word?**
A: Yes. Each team runs BPE independently on their own dataset. Merge order differs, vocabulary differs, IDs differ. `user` might be 428 in GPT-4, a completely different number in LLaMA 3 or Claude. This is why you can't mix tokenizers — token IDs from one model fed into another are gibberish. The model and its tokenizer are always a matched pair.

---

## Next

**Concept 2: Cognitive deficits caused by tokenization** — why the model can't spell or count (the "ubiquitous" demo, the "strawberry" R-counting failure, and the dots counting failure). Karpathy's three specific breakage demos.
