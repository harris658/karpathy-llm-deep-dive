# karpathy-llm-deep-dive

Project instructions. Inherits all rules from `labs/CLAUDE.md`.

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
