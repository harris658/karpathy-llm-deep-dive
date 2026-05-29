# karpathy-llm-deep-dive

Project instructions. Inherits all rules from `labs/CLAUDE.md`.

## Teaching Approach — what's specific to this project

The full labs teaching standards — assume zero knowledge, define every term before using it, prerequisite-first, why-before-what, real-world analogies, **one concept per message then stop**, spell out every line of code, never "obviously / simply / just", depth over speed, and "a clarifying question means *I* go deeper" — are inherited from `labs/CLAUDE.md` and **not repeated here**. This section is only the delta that makes karpathy stricter than a normal lab.

- **Harshit is at absolute zero on ML specifically** — neural networks, LLMs, and the underlying math/CS. A lower floor than the generic labs baseline. The first time any ML term appears (gradient, weight, embedding, logit, attention, token, etc.), define it in one plain sentence before using it again.
- **Cover Karpathy's full 3.5-hour video.** Every concept he explains must be taught here, not just the ones with code. A concept with no coding exercise still gets a dedicated theory explanation + a concrete mental model + an analogy. Nothing is skipped because "it's too advanced" or "not relevant for beginners."
- **One concept per message — never a wall of text.** Inherited from labs, but it is the single most important rule here. Each beat is: the concept (one idea, plain English) → a real-world analogy → one or two sentences of why it matters → then **"Ready to move on?"** or **"Any questions before we continue?"** Then stop and wait. Never pre-load the next idea.

## Always query NotebookLM first (MANDATORY)

Before teaching any concept or starting any chapter, query the NotebookLM notebook to get exactly what Karpathy says in the video. Never teach from general knowledge alone.

Notebook ID: `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`

Query pattern:
```
notebooklm ask "<specific question about this concept>" --notebook c43662e9-4bcb-4f29-a8e0-9a4a7990d835
```

Use the video's exact examples, numbers, and analogies — not invented ones. If Karpathy uses a specific demo (e.g., zebra Wikipedia regurgitation), recreate that exact demo, not a generic version.

## Chapter Notes — What to write (MANDATORY)

After every chapter's concepts are fully taught, write the chapter's `notes.md` (e.g. `01-pretraining-data/notes.md`) before moving to the diagram. This is the reference Harshit will use to look back — it must be complete enough to reconstruct the session cold, without needing to re-read the conversation.

### What every chapter notes.md must include

1. **Every concept taught** — in order, with:
   - Plain-English explanation (not a one-liner — full explanation as taught)
   - The real-world analogy used
   - Why it matters / what problem it solves
2. **All worked examples** — any demo, number, or walkthrough used during the session (e.g. the BPE merge example, the zebra regurgitation demo)
3. **Key numbers table** — every specific number mentioned (dataset sizes, costs, vocab sizes, etc.)
4. **Q&A from the session** — every clarifying question Harshit asked, and the answer. These are often the most valuable part — they reveal the exact misconceptions that needed fixing.
5. **Diagram URL** — under a `## Diagram` heading
6. **Next** — one line: what the next chapter covers and why

### What NOT to do

- Don't write a bullet-point summary. Write full explanations.
- Don't skip Q&A. If Harshit asked it, it matters.
- Don't skip analogies. They're the part that sticks.

### Also update the root notes.md

After writing the chapter notes, update `notes.md` at the project root with a session log entry (newest at top):

```
## YYYY-MM-DD

**What we covered:** [chapter + one-line summary of concepts]
**What worked:** [anything notable]
**What broke:** [any issues hit]
**Next:** [next chapter + first concept]
```

Do this automatically — Harshit should never have to ask for it.

### Commit order

1. Write chapter `notes.md`
2. Update root `notes.md`
3. `git add` both files
4. `git commit -m "docs(chN): complete chapter notes and session log"`
5. `git push`

---

## Chapter Completion — Excalidraw Wireframe (MANDATORY)

After every chapter is confirmed working (Harshit has run the code and seen real output), draw the chapter's concept diagram before moving to the next chapter — follow the **Wireframes** protocol and style rules in `labs/CLAUDE.md`, committing it as `docs(NN): add chapter wireframe`.

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
