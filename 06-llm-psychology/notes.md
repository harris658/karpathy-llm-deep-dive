# Chapter 6: LLM Psychology — Session Notes

**Date:** 2026-06-10
**Status:** In progress (Concepts 1–2 done, 7 remaining)
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Concept 1 — The Swiss Cheese Model (Jagged Intelligence)

**The problem:** Without this framing you'll trust LLMs wrong — assuming that because a model handles hard tasks it can definitely handle easy ones too.

**What it is:** Karpathy calls LLM capability a "Swiss cheese" model — solid in most places, but with random unpredictable holes punched through at arbitrary spots. He calls this **jagged intelligence**: the skill profile is uneven in a way that doesn't match human intuition. The same model that writes graduate-level legal analysis will confidently say 9.11 > 9.9. A model that explains Byzantine history in depth fails to count the letter R in "strawberry."

**The analogy:** A contractor who builds flawless skyscrapers but can't reliably count the windows on the front face. You'd assume if they can do the hard thing, they can do the easy thing — but those two tasks use completely different cognitive skills. With LLMs, "hard for a human" ≠ "hard for the model."

**Common misconception:** Capability scales smoothly — a more powerful model gets proportionally better at everything. It doesn't. Jagged intelligence means a highly capable model can still have holes in places a weaker model doesn't. The shape of the cheese changes, but holes always remain.

**Why it matters:** The rest of ch6 is Karpathy explaining why each hole exists. Jagged intelligence is the lens for all of them.

---

## Concept 2 — Hallucinations: The Confident Liar

**The problem:** Without understanding why the model sounds confident when it's wrong, you can't know when to trust it — a hallucinated answer and a correct answer are indistinguishable in tone.

**What it is:** Hallucinations are a direct consequence of SFT. Human labelers write ideal responses to factual questions ("Who is Tom Cruise?", "Who is John Barrasso?") — and because they either know the answer or research it, every example in the training set is written in what Karpathy calls the **"confident tone of an answer."** The model absorbs this pattern completely. It has no internal fact-checker. It cannot convert uncertainty into a verbal refusal. It just generates the statistically most probable next tokens — which always sound authoritative.

Karpathy's term: **"statistical token tumbler"** — tumbles forward to probable tokens with no mechanism to halt and check.

**The Orson Kovats demo:** Karpathy invents a completely fictional name — Orson Kovats — and tests it on **Falcon 7B instruct** on the Hugging Face inference playground (an older model, which hallucinates more visibly). Three attempts, three completely different fabricated identities:
- Attempt 1: "an American author and science fiction writer"
- Attempt 2: "a fictional character from a 1950s TV show"
- Attempt 3: "a former minor league baseball player"

All confident. All invented. The model doesn't know it's lying — it's imitating the format of answers it saw in training, applied to a name it has no knowledge of.

**The analogy:** An eager student who has read thousands of Q&A transcripts. They've absorbed the style of confident answers so thoroughly that when a question arrives they can't answer, they still produce a confident-sounding response — because that's the only pattern they've practised. They're not dishonest; they've never been given a model of what "I don't know" looks like.

**Common misconception:** The model "knows it's guessing" and is choosing not to say so. It isn't. There's no internal experience of uncertainty being suppressed. The confident tone is not a personality trait — it's the direct output of a training process that never included uncertain responses.

---

## Demo File

`06-llm-psychology/hallucination_demo.py` — script to call HF Inference API with the Orson Kovats prompt. HF's free inference tier is currently blocking most models (Falcon 7B and Mistral 7B both return "Model not supported by provider hf-inference"). Demo was explained conceptually instead.

---

## Concepts Still to Cover

3. **Fixing Hallucinations** — empirical probing; wiring uncertainty to verbal refusals via training injection
4. **Memory: Two Types** — parameters (vague recollection) vs context window (working memory)
5. **Tool Use** — special tokens that let the model bypass its lossy memory via web search
6. **No Persistent Self** — the model boots from zero every turn; identity is injected, not felt
7. **Models Need Tokens to Think** — distributing computation across generation steps
8. **Token Blindness** — why counting and spelling break at the character level
9. **Bizarre Distractions** — the 9.11 > 9.9 failure and how Bible-verse neurons hijack math

---

## Next

**Concept 3 — Fixing Hallucinations:** how developers empirically probe for knowledge gaps (the Dominic Hasek Stanley Cup example) and inject "I don't know" training examples to wire uncertainty to verbal refusals.
