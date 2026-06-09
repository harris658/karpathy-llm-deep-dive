# Chapter 4: Pretraining & Inference — Session Notes

**Date:** 2026-06-04 / 2026-06-09
**Status:** Complete
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

## Concept 2 — Scale: 1 Million Tokens Per Step

**The key number:** Every single update step of the neural network processes exactly **1 million tokens simultaneously** — all in parallel. Not one token at a time, not ten: a million.

**The analogy:** Imagine learning to cook, but instead of making one dish per day and adjusting from feedback, you somehow cook a million dishes simultaneously, taste them all at once, and adjust your technique from the combined result. That's one step.

**The loss curve:** While training runs, researchers watch a single number drop — the loss curve. At step 0, loss is high (random guessing). As steps tick by, it slowly decreases. That downward slope *is* learning. Karpathy's GPT-2 reproduction runs for **32,000 steps**, processing about **33 billion tokens** total.

**Why it costs tens of millions:** The GPT-2 reproduction Karpathy shows cost **$600** and took one day. The original 2019 GPT-2 training cost **$40,000**. That feels cheap — but GPT-2 is a small, old model. Modern frontier models like Llama 3 (405B parameters, 15T tokens) require **tens of thousands to hundreds of thousands of GPUs running in parallel**. At **$3 per GPU per hour**, running 100,000 GPUs for months reaches hundreds of millions of dollars before accounting for power costs. Karpathy's phrase: *"tens of millions or hundreds of millions of dollars."*

**Batch size is a hyperparameter, not a universal rule:** The 1 million figure is what Karpathy configured for his demo. Every model sets its own batch size based on hardware and budget. It's a tunable knob, not a fixed limit.

**More training is better — up to a point:** Two limits exist:
1. *Diminishing returns* — the loss curve flattens. Early steps move the needle significantly; later steps barely move it.
2. *Data exhaustion* — training on the same text repeatedly (*multiple epochs*) causes the model to memorize documents rather than generalize. Performance gets worse, not better. More training only helps if there's more *unique* data to train on.

**Model size vs. training are separate things:** Model size (number of parameters) is fixed before training starts — it's an architectural decision. Training tunes the *values* of those parameters; it doesn't create more of them. The analogy: a mixing board with 10 sliders vs. 1,000 sliders. Using the mixing board longer doesn't give you more sliders — you just get better at finding the right positions for the ones you have.

**Scaling laws (Chinchilla):** Researchers found an optimal ratio between model size and training tokens. The Chinchilla result: roughly **20 tokens per parameter** for peak efficiency. A 10B parameter model ideally needs ~200B tokens. This is how teams decide model size upfront — start with the compute budget, apply the ratio, design accordingly. In practice, companies hedge by releasing multiple sizes (7B, 13B, 70B) since nobody gets it perfectly right on the first try.

**Big models and overfitting:** A bigger model doesn't handle repetitive training better — it overfits *faster*, because more parameters means more capacity to memorize exact documents verbatim. Size and data must scale together. The current bottleneck for frontier models isn't compute — it's running out of high-quality unique text, which is driving interest in synthetic data generation.

---

## Concept 3 — The Base Model: Internet Document Simulator

**What it is:** After pretraining completes, the output is a **base model**. Karpathy calls it a very expensive **"token autocomplete"** — given some tokens, predict what comes next. That is its one skill.

**The zip file analogy:** Think of the base model as a **lossy zip file of the internet**. It has read 15 trillion tokens and compressed all of it into its parameters — world knowledge, language patterns, facts, opinions, code, stories. But it's lossy, like a JPEG: things that appeared thousands of times in training (e.g. "Paris is the capital of France") are sharp. Rare things are blurry and probabilistic — the model has a vague recollection and will fill gaps with something plausible-sounding.

**What it cannot do:** A base model is not designed to answer questions or be helpful. It has no concept of truth vs. plausibility. It has no concept of stopping. It simply continues token sequences in whatever direction looks statistically likely based on the internet text it saw.

**What it can do with a clever prompt:**
- *Exact recall*: High-quality sources like Wikipedia are seen many times during training → memorized nearly verbatim.
- *Pattern following (few-shot)*: Give it a list of English-Korean word pairs, then a new English word — it recognizes the pattern and translates, no instruction needed.
- *Simulated assistant*: Structure a prompt like an AI conversation transcript and it will continue in the assistant role — because that's what the text pattern calls for.

---

## Concept 4 — Inference: The Biased Coin Flip

**What inference is:** Training is over, parameters are frozen. Inference is the process of generating new text from the trained model.

**Token-by-token generation:**
1. Feed the model a prompt (a sequence of tokens)
2. Run the full Ch.3 pipeline → get a probability distribution over all 100,277 tokens
3. **Flip a biased coin** — sample from the distribution. High-probability tokens are more likely to land, but it's still a random draw.
4. Append the selected token to the sequence
5. Feed the new longer sequence back in — repeat

**Why sampling instead of always picking the top token:** Always picking the highest-probability token (*greedy decoding*) would give the exact same output every time for the same prompt — brittle and boring. Sampling produces variation, which makes outputs feel natural and creative.

**Stochastic = different every time:** Because of the coin flip, the same prompt produces a different response on every run. Small early differences compound — by the 20th token, two runs can be heading in entirely different directions.

**Remixes, not copies:** The model isn't retrieving stored answers. It's sampling a path through a probability landscape built during training. Every walk through that landscape is unique. The outputs are *remixes* of training data, not verbatim copies.

---

## Concept 5 — Base Model Behavior: The Demos

**Demo 1 — "What is 2+2?"**
Karpathy types this into a base model. It does not say "4." It generates more math questions, or a philosophical tangent on arithmetic. The model treats the input as a text prefix. On the internet, a document containing "What is 2+2?" is probably a quiz or worksheet — so the model generates more quiz content. It has no concept of "the human wants an answer."

**Demo 2 — Zebra Wikipedia Regurgitation**
Karpathy pastes the first sentence of Wikipedia's article on zebras. The model recites the rest of the article nearly word for word. Why? Wikipedia is high-quality text that gets preferentially sampled during training — the model sees it multiple times until it memorizes it, the way you'd memorize a song heard a thousand times. The lesson: fluent and confident output can be pure memorization, not reasoning.

**Demo 3 — The 2024 Election Hallucination**
The model has a training cutoff at end of 2023 — it never saw data about the 2024 US presidential election. Karpathy prompts it about the 2024 election outcome. The model cannot say "I don't know" — that's not a behavior it learned. So it keeps generating tokens confidently:
- Run 1: Mike Pence ran against Hillary Clinton
- Run 2: Ron DeSantis ran against Biden and Kamala Harris

Each run: a different fabricated parallel universe, stated with complete fluency and zero hesitation. This is what Karpathy means by **"hallucinating parallel universes."** The model isn't lying — it has no concept of lying. It's doing the only thing it knows: generating statistically plausible-sounding text.

**The takeaway:** The base model has absorbed an enormous amount of world knowledge. But it has no goal, no sense of helpfulness, no ability to say "I don't know", and no alignment between fluent and true. Every chapter from here is about fixing those gaps.

---

## Key Numbers

| Fact | Number |
|---|---|
| Tokens per training step (Karpathy's GPT-2 demo) | 1 million |
| Steps in Karpathy's GPT-2 run | 32,000 |
| Tokens in Karpathy's GPT-2 run | ~33 billion |
| GPT-2 original training cost (2019) | $40,000 |
| GPT-2 reproduction cost (today) | $600 |
| Frontier model training cost | Tens to hundreds of millions of dollars |
| GPU rental cost (H100) | ~$3 per GPU per hour |
| Llama 3 parameters | 405 billion |
| Llama 3 training tokens | 15 trillion |
| Chinchilla optimal ratio | ~20 tokens per parameter |
| GPT-2 parameters | ~1.5 billion |
| GPT-2 original training tokens | 100 billion |

---

## Q&A

**Q: If no human is involved, how does the model know the correct answer?**
It doesn't need one — the correct answer is already in the text. The model sees `the sky is` and the answer `blue` is sitting right there in the next position. Every sentence is its own answer key. No human labeling needed; the text is the label.

**Q: Is it trained on simple sentences where there are direct answers?**
No — it's trained on everything: Wikipedia, Reddit, novels, code, news, blog comments. "Correct" doesn't mean factually right. It just means what actually came next in this particular document. If the training text says "The capital of Australia is Sydney" (wrong), the model learns to predict Sydney anyway. It learns what humans wrote, not what is true. For ambiguous sentences with no single correct next word, the model assigns probabilities across all possibilities — the loss just nudges the actual next token's probability a bit higher.

**Q: Is 1 million tokens per step a universal limit for all models?**
No — it's called batch size, and it's a hyperparameter each team sets based on their hardware and budget. Bigger batches give more reliable gradient signals but need more GPUs. It varies across every model.

**Q: Isn't model size determined by how much training has been done?**
No — model size (number of parameters) is fixed before training starts, as a design decision. Training only tunes the *values* of those parameters. More training doesn't add parameters. Think of it like a mixing board: using it longer doesn't give you more sliders.

**Q: So more training is always better?**
Not always. Two limits: (1) diminishing returns — loss flattens as common patterns are absorbed; (2) data exhaustion — repeating the same data causes memorization instead of generalization, which hurts performance.

**Q: Is too much training only a problem for small models? Big models have more space.**
Actually a big model overfits *faster* — more parameters means more capacity to memorize verbatim. Size and data must scale together. A big model only helps if you have proportionally more unique data to feed it.

**Q: How do you decide upfront how many parameters a model needs?**
You start with your compute budget (GPU-hours), then apply scaling laws. The Chinchilla result: ~20 tokens per parameter for optimal efficiency. Budget → token count → parameter count. In practice teams hedge by releasing multiple sizes since nobody gets the ratio exactly right.

---

## Diagram

https://excalidraw.com/#json=I2bdZ6rjc9d8WOejgfDA3,32nsb_vfSCdJebgdV_WIVA

---

## Next

**Chapter 5 — Supervised Fine-Tuning:** How the base model (internet document simulator) is transformed into an assistant using human-written conversation data. The format of that data, what changes and what doesn't, and why fine-tuning is so much cheaper than pretraining.
