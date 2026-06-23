# Notes

Running log. One entry per working session. Newest at the top.

---

## 2026-06-23 (Ch.8 — complete)

**What we covered:** Chapter 8 — Future Directions, all 6 concepts: Multimodality (image/audio patches tokenized into the same sequence, no new architecture needed), Agents (models operating over minutes/hours, human-to-agent supervision ratio), Computer Use (screenshot + keyboard/mouse control, ChatGPT Operator as early example), Test-Time Training (fixed parameters can't scale to long-running multimodal tasks, sleeping brain analogy, major open research problem), Keeping Track of AI Progress (Chatbot Arena leaderboard now "a little gamed", AI News newsletter by swix, X/Twitter for breaking news), Where to Find Models (proprietary → provider sites, open-weight → Together.ai, base models → Hyperbolic, local → LM Studio).
**What worked:** Multimodality Q&A resolved cleanly — Harshit caught that some frontier models already do all three modalities and the "future directions" framing needed clarification. Clean session, no code, all conceptual.
**What broke:** None.
**Next:** This is the final chapter. Karpathy's full 3.5-hour video is now completely covered across 8 chapters.

---

## 2026-06-22 (Ch.7 — complete)

**What we covered:** Chapter 7 — Reinforcement Learning, all 7 concepts: Going to School analogy (RL as 3rd training stage, practice problems with no worked steps), Token Path Problem (human cognition ≠ LLM token paths, SFT can't create optimal sequences), Verifiable Domains & DeepSeek-R1 (math/code scoring, emergent backtracking from RL), Thinking Models demo (chat.deepseek.com Deep Think, visible internal monologue, distillation risk behind OpenAI's hidden traces), AlphaGo & Move 37 (SFT caps at human ceiling, RL breaks through, alien analogies + non-English thinking language predictions), RLHF & Reward Model (pelican joke, ranking vs generating, discriminator-generator gap), Reward Gaming (adversarial strings, "the the the" scores 1.0, RLHF = "little fine-tune" not real RL).
**What worked:** Heavy Q&A — "pre-Move 37", "why 37", "is RL fully out", "what's RLHF", "what's an adversarial string" — all resolved cleanly mid-session. AlphaGo analogy landed well as the clearest proof that RL breaks the human ceiling. Distillation risk concept clicked immediately.
**What broke / open questions:** No code this chapter — all conceptual. No HF API issues.
**Next:** Chapter 8 — Future Directions: multimodality (audio/image as tokens), agents, computer use, test-time training, where to find models, Karpathy's final pipeline summary.

---

## 2026-06-18 (Ch.6 — complete)

**What we covered:** Chapter 6 Concepts 6–9: No Persistent Self (boot up/shut off, Falcon 7B hallucinated identity, OLMo 240 hardcoded SFT conversations, hidden system message), Models Need Tokens to Think (fixed computation per token, "mean prompt" single-token forced failure, chain-of-thought), Token Blindness (tokenizer compresses letters, ubiquitous/strawberry/dots demos, "use code" fix), Bizarre Distractions (9.11 > 9.9 failure, Bible verse neurons hijack math, closes Swiss cheese loop). Chapter 6 complete.
**What worked:** NotebookLM query pattern enforced — all concepts grounded in Karpathy's exact demos and phrasing. Clean session, no Q&A detours.
**What broke / open questions:** None.
**Next:** Chapter 7 — Reinforcement Learning: RLHF, reward models, reward hacking, DeepSeek-R1, AlphaGo analogy.

---

## 2026-06-16 (Ch.6 — in progress)

**What we covered:** Chapter 6 Concepts 3–5: Fixing Hallucinations (empirical probing pipeline, Dominic Hasek Stanley Cup demo, LLM judge, injecting "I don't know"), Memory Two Types (parameters = vague recollection, context window = perfect working memory, Pride & Prejudice demo), Tool Use (search_start/search_end tokens pause generation + web search, code interpreter offloads math to Python, Orson Kovats and Hasek demos revisited with modern ChatGPT).
**What worked:** Q&A was sharp — Harshit independently connected Ch.5's web-search fix to Ch.6 tool use. The "entire pipeline is automated" point resolved a recurring concern about scale. Parameter vs context window distinction clicked cleanly via the re-reading analogy.
**What broke / open questions:** None.
**Next:** Concept 6 — No Persistent Self: model boots fresh every turn, no memory of prior conversations, identity injected via system prompt + SFT.

---

## 2026-06-10 (Ch.6 — in progress)

**What we covered:** Chapter 6 started — Concepts 1 & 2: Jagged Intelligence (Swiss cheese capability model, uneven skill profile), Hallucinations: The Confident Liar (statistical token tumbler, Orson Kovats demo, why confident tone ≠ correct answer).
**What worked:** Jagged intelligence framing landed as a clean lens for the whole chapter. Hallucination root cause (SFT training data always written in confident tone) clicked well.
**What broke / open questions:** HF free inference API blocking Falcon 7B and Mistral 7B — hallucination_demo.py couldn't run live. Demo explained conceptually instead.
**Next:** Concept 3 — Fixing Hallucinations: empirical probing (Dominic Hasek Stanley Cup example), injecting "I don't know" training examples to wire uncertainty to verbal refusals.

---

## 2026-06-09 (Ch.5)

**What we covered:** Chapter 5 complete — SFT: algorithm unchanged / only data changes, labeling instructions (helpful+truthful+harmless, chain-of-thought on math), hallucinations persist + fixes (deliberate injection, tool use), system prompt (invisible tokens, bolted-on identity), modern synthetic SFT datasets.
**What worked:** System prompt clicked immediately via real Opus 4.8/DeepSeek Reddit incident. Bootstrapping problem (first model = pure humans) resolved cleanly.
**What broke / open questions:** None.
**Next:** Chapter 6 — LLM Psychology. Swiss cheese capabilities, hallucination, tool use, memory, jagged intelligence.

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
