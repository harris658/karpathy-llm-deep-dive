# karpathy-llm-deep-dive

Project instructions. Inherits all rules from `labs/CLAUDE.md`.

## Teaching Approach — Zero Prior Knowledge (CRITICAL)

Harshit knows nothing about ML, neural networks, LLMs, or any related math or CS concepts. Assume he is starting from absolute zero.

### What "assume nothing" means in practice

- **Never use a term without defining it first.** If a concept requires another concept to understand, explain the prerequisite first, then come back.
- **No jargon without a plain-English definition.** The first time any word appears (gradient, weight, embedding, logit, attention, token, etc.) — define it in one simple sentence before using it again.
- **Use real-world analogies.** If you explain attention, give an analogy. If you explain a matrix multiply, give an analogy. The analogy comes before the technical definition, not after.
- **Explain the WHY before the WHAT.** Don't say "we use softmax here." Say "we need all these numbers to add up to 1 so we can treat them as probabilities — the function that does that is called softmax."
- **Spell out every step of the code.** No "standard boilerplate" or "you know how this works." Walk through every line that matters.
- **Never say "as you know", "obviously", "simply", or "just".** These words signal skipped explanation.
- **If something was taught in a previous chapter, briefly recap it** when it appears again — don't assume it stuck.

### Coverage requirement

This project covers Karpathy's full 3.5-hour video — every concept he explains must be taught here, not just the ones that have code. If a concept appears in the video but doesn't have a coding exercise, it gets a dedicated theory explanation + a concrete mental model + an analogy. Nothing is skipped because "it's too advanced" or "not relevant for beginners."

### Depth over speed

It is better to spend three sessions on one chapter than to rush through it and have Harshit not understand it. If he asks a clarifying question, that means the explanation wasn't complete — answer fully, then redo the summary before moving on. Never proceed to the next step if he signals confusion about the current one.

## Chapter Completion — Excalidraw Wireframe (MANDATORY)

After every chapter is confirmed working (Harshit has run the code and seen real output), draw a concept diagram before moving to the next chapter.

### Protocol

1. Call `mcp__claude_ai_Excalidraw__read_me` first — always, every time, to get the current element format.
2. Call `mcp__claude_ai_Excalidraw__create_view` with a hand-drawn diagram covering:
   - The key concept(s) of the chapter
   - How data flows through the system
   - Where this chapter fits in the overall LLM pipeline (show its place in the chain)
3. Call `mcp__claude_ai_Excalidraw__export_to_excalidraw` to get a shareable URL.
4. Save the URL in the chapter's `notes.md` under a `## Diagram` heading.
5. Commit the updated `notes.md` with message: `docs(NN): add chapter wireframe`

### What the diagram should show

| Chapter | What to illustrate |
|---------|-------------------|
| 01 — Pretraining Data | Internet → scrape → filter → dedupe → tokens corpus |
| 02 — Tokenization | Raw text → BPE merges → token IDs → vocab table |
| 03 — Transformer Architecture | Token embeddings → attention heads → residual stream → logits |
| 04 — Pretraining & Inference | Training loop + base model inference flow |
| 05 — Supervised Finetuning | Base model → conversation data format → SFT → assistant |
| 06 — LLM Psychology | Mental model map: hallucination / tool use / memory / jagged intelligence |
| 07 — Reinforcement Learning | Base → reward model → RL loop → aligned model; DeepSeek-R1 thinking tokens |

### Style rules

- Hand-drawn feel (Excalidraw default strokes — no clean corporate look).
- Flow left → right or top → bottom. Label every arrow.
- Highlight where the current chapter's concept "lives" in the broader LLM pipeline.
- Keep it readable at a glance — not a textbook figure, a recall aid.
