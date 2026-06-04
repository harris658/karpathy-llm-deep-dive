# Chapter 4: Pretraining & Inference — Session Notes

**Date:** 2026-06-04
**Status:** In progress (Concept 1 complete; Concepts 2–5 pending)
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Concept 1 — The Training Loop: Loss, Labels, and Knob-Twiddling

**The starting state:** When a network is first created, every parameter is set to a random number. The model's first predictions are garbage — roughly equal probability assigned to all 100,277 tokens because it knows nothing.

**How it learns — the loop:**
1. Take a window of tokens from the training text (e.g. `the`, `sky`, `is`)
2. Feed it into the network → get 100,277 probability scores
3. Compare the highest-scored token against the **label** — the correct next token (`blue`), which is already sitting right there in the training text
4. Compute the **loss** — a single number measuring how wrong the prediction was. High loss = very wrong. Low loss = nearly right.
5. **Backpropagation** works backward through the entire network and figures out which knobs, if nudged slightly, would make the correct token score higher and all wrong tokens score lower
6. Nudge every parameter in the chain — a tiny amount
7. Repeat with a new window

**Loss** is the progress metric for training. As the model gets better, loss goes down. Karpathy's phrase: *"low loss is good."*

**The analogy:** Learning to throw darts blindfolded. Someone tells you how far you missed (loss). You adjust your stance slightly. Throw again. Adjust again. After millions of throws and corrections, your body has internalized where the board is — even though no one ever stated a rule directly.

**The misconception to watch for:** It is not being told "memorize this answer." It is being nudged — fractionally — toward better predictions, over and over, billions of times. No rules are ever stated. Patterns emerge from correction alone.

**Why labels are "free":** In most ML, humans must manually label training data ("this image is a cat"). That's expensive and slow. Next-token prediction sidesteps this entirely. Any sentence contains its own labels:

| Input | Label (correct next token) |
|---|---|
| `the` | `sky` |
| `the sky` | `is` |
| `the sky is` | `blue` |
| `the sky is blue` | `.` |

Nobody writes those labels — the text already contains them. Every document on the internet is a pre-labeled training example. 15 trillion tokens = 15 trillion labeled examples, zero human effort.

**Backprop runs through the entire Ch.3 pipeline:** The model never sees the word "blue" — it sees token ID `10349`. The label is also a token ID. Backpropagation nudges every parameter in the full chain: embedding table, attention blocks ×100, MLP blocks ×100, logit projection. The embedding vectors themselves (those 768-number lists from Ch.3) are parameters and get tuned too — that's why "cat" and "kitten" end up with similar vectors after training.

**Pretraining vs. fine-tuning:** Human-written labels (questions + correct answers) only appear in **Chapter 5 (Supervised Fine-Tuning)**. Pretraining uses zero human labels — only raw scraped text. That's what makes the 15T-token scale possible.

---

## Pending Concepts

- **Concept 2:** Scale — 1 million tokens per step, loss curve, months of compute
- **Concept 3:** The base model — "internet document simulator", "zip file of the internet"
- **Concept 4:** Inference — the biased coin flip, stochastic generation, remixes
- **Concept 5:** Base model behavior — zebra Wikipedia regurgitation, hallucinating parallel universes, not a chat assistant

---

## Next

**Concept 2 — Scale:** What one training step actually looks like at real scale. Karpathy shows a live GPT-2 training run — 1 million tokens updated per step. What the loss curve looks like as training progresses. Why pretraining costs tens of millions of dollars and takes months.
