# Chapter 5: Supervised Fine-Tuning — Session Notes

**Date:** 2026-06-09
**Status:** Complete
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Concept 1 — What SFT Is: Only the Data Changes

**The problem:** After pretraining, the base model is an "internet document simulator" — it completes text, doesn't help. To turn it into an assistant, you need it to respond helpfully to questions, follow instructions, and adopt a useful persona.

**The key insight:** The training algorithm doesn't change at all. It's still the same loop — feed tokens, predict next token, compute loss, backpropagate, nudge parameters. What changes is only the data.

Instead of 15 trillion tokens of raw internet text, SFT uses a small, curated dataset of conversations — each one a prompt + ideal assistant response.

**Why it's cheap:** Pretraining: months, tens of millions of dollars, 15T tokens. SFT on ~100,000 conversations: roughly three hours. The dataset is tiny relative to pretraining. Even modern SFT datasets with millions of conversations are a rounding error at pretraining scale.

**The result:** After training on enough conversational examples, the parameters shift to adopt the assistant persona. The model learns to produce helpful responses because that's the statistical pattern it now sees.

**Karpathy's phrase:** The resulting assistant is a *"neural network simulation of a data labeler"* — it statistically imitates the tone, style, and problem-solving behaviour of the humans who wrote the ideal responses.

---

## Concept 2 — Labeling Instructions

**What they are:** Detailed documents, typically hundreds of pages long, that human contractors study professionally before writing a single response. They specify what "helpful, truthful, and harmless" means in practice — every edge case, every refusal scenario, every tone guideline.

**Example prompts labelers work with:**
- "List five ideas for how to regain enthusiasm for my career."
- "What are the top 10 science fiction books I should read next?"
- "Translate this sentence into Spanish."
- "Explain the economic relevance of 'monopsony' to a beginner."
- "If apples cost $1.50 and oranges cost $0.75, what do 3 apples and 2 oranges cost?"

**The math problem insight:** For the apples and oranges question, a bad response immediately states the final answer — forcing the model to do all arithmetic in a single token. It can't. The ideal response writes out the steps:

> *"3 × $1.50 = $4.50. 2 × $0.75 = $1.50. Total = $6.00."*

By spreading computation across many tokens, each step is simple. This is how the model learns "chain of thought" — not an innate capability, but a pattern baked in by how ideal responses were written.

**Refusals:** Labelers are explicitly told not to answer certain categories of request. They write graceful refusal responses. The model learns to imitate those refusals — not because it "knows" something is off-limits, but because refusal is the statistically expected next token for those prompts.

---

## Concept 3 — Hallucinations Persist After SFT

**Why hallucination survives fine-tuning:** Human labelers write confident, authoritative responses — that's what good assistant output sounds like. The model learns the *style* of confident answers, not the underlying behaviour of "check before you claim." It has no internet access, no ability to verify facts. It just knows: questions are followed by confident-sounding answers.

**Karpathy's demo — "Orson Kovats":** He prompts the model with a completely made-up name. The model confidently invents an identity: "a 1950s TV character" or "a minor league baseball player." It cannot say "I don't know" — that's not statistically likely after a question about a person. It just samples what confident answers about people look like.

**Fix 1 — Deliberate injection:** Developers automatically interrogate the model with thousands of factual questions. For every question it consistently gets wrong, they inject a training conversation where the correct answer is *"I'm sorry, I don't know."* This trains the model to connect its internal uncertainty to a verbal refusal instead of guessing.

**Fix 2 — Tool use:** Train the model to emit a special token (e.g. `search_start`) when it lacks a fact. This pauses generation, triggers a real web search, and pastes results directly into the context window. The model stops reading from its blurry parameter memory and reads fresh accurate text instead — far more reliable than patching individual knowledge gaps.

**The big picture:** Every behaviour the assistant has was explicitly programmed by example. The quality of the assistant is bounded by the quality of the labeling instructions and the human responses.

---

## Concept 4 — The System Prompt

**What it is:** A hidden block of text prepended to every conversation before the user types anything. The user never sees it. Karpathy calls these *"invisible tokens"* secretly inserted into the context window.

**What it typically contains:**
- The model's identity: "You are ChatGPT-4o, built by OpenAI."
- Knowledge cutoff date
- Tone and behavioural guidelines
- Product-specific instructions

**Why identity must be stated explicitly:** The model has no persistent sense of self — it restarts completely fresh every conversation. Without a system prompt telling it who it is, it hallucinates an identity based on training data. An older open-source model might claim to be built by OpenAI simply because ChatGPT is mentioned far more in training data than anything else.

**Karpathy's phrase:** The identity is *"cooked up and bolted on"* — not deeply rooted in the weights, just text the model reads every turn. Companies reinforce this with both the system prompt and dedicated SFT examples so the two sources agree.

**Beyond identity:** The system prompt is the main lever for product customisation without retraining. Same model, completely different behaviour: swap the system prompt and you get a customer service agent, a coding assistant, or a children's tutor.

**Real-world example:** When Opus 4.8 launched, Reddit users reported the model claiming to be DeepSeek or another model. Most likely cause: testing via raw API or third-party wrappers without a properly configured system prompt — the model fell back to statistically likely identity patterns from training data.

---

## Concept 5 — Modern SFT Datasets

**The original approach (InstructGPT, 2022):** Pure human labor. Contractors read hundreds of pages of instructions, then manually wrote every prompt and every ideal response from scratch. Expensive, slow, thousands of examples.

**The modern approach:** Human-model hybrid.
1. An LLM drafts the ideal response
2. A human expert reviews, edits, approves
3. The approved version enters the training set

This scales from thousands of examples to **millions**. Open-source datasets like UltraChat contain millions of multi-turn conversations — what Karpathy calls **"SFT mixtures"**: blends of human-written and synthetic conversations across enormous topic diversity.

**The bootstrapping circle:** Early models trained on pure human data. Those models then helped produce data for the next generation, which produced data for the generation after. Each model in the lineage is partly trained on its predecessors' outputs.

**The trap:** Synthetic data sounds like a shortcut. It only works if human review is rigorous. If labelers rubber-stamp LLM outputs, errors compound through generations. The human-in-the-loop isn't optional — it's the quality gate.

---

## Key Numbers

| Fact | Number |
|---|---|
| SFT training time (100K examples) | ~3 hours |
| Original InstructGPT dataset | Thousands of conversations |
| Modern SFT dataset (e.g. UltraChat) | Millions of conversations |
| Labeling instructions length | Hundreds of pages |
| Year InstructGPT released | 2022 |

---

## Q&A

**Q: Who writes the ideal responses — is it also a model?**
Today, largely yes — LLMs draft, humans review. But the first model (InstructGPT) was trained on pure human-written data. No prior model existed to help. Someone had to go first with nothing but humans and a lot of instructions.

**Q: Did GPT-3 come before or after InstructGPT?**
Before. GPT-3 (2020) was the base model. InstructGPT (2022) was GPT-3 with SFT applied on top — same underlying model, different data. First time OpenAI released something that reliably followed instructions.

**Q: Why does the model claim to be DeepSeek when Opus 4.8 was released?**
No system prompt or misconfigured identity. Without "you are Claude, made by Anthropic" in the context, the model falls back to statistical likelihood from training data — which might favour DeepSeek if it appeared heavily there. Exactly what "cooked up and bolted on" means in practice.

---

## Diagram

[Chapter 5 SFT Architecture](https://excalidraw.com/#json=Lg8kD7lGF0i3sWLMxPxOQ,TiBr8hb2J43iHr4hcgXZAQ)

Shows: Pre-trained Base LLM + SFT Dataset → fine-tuning loop (response-only loss) → Instruction-Following LLM + System Prompt

---

## Next

**Chapter 6 — LLM Psychology:** The "Swiss cheese" capability model — why models solve PhD-level physics but fail trivial counting tasks. Hallucination, tool use, memory, jagged intelligence.
