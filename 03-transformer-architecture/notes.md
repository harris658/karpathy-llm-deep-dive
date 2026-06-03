# Chapter 3: Transformer Architecture — Session Notes

**Date:** 2026-06-03
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Diagram

https://excalidraw.com/#json=3tsO_gEl_oG_bzdAZv79n,tUSVc880xnAuSC0qENd96A

---

## Concept 1 — The Neural Network Is a Mathematical Function

The neural network is not magic — it is a **fixed, stateless mathematical function**. You feed in token IDs (a list of integers), numbers flow through a sequence of mathematical operations, and a list of scores comes out — one score per token in the vocabulary. The token with the highest score becomes the next token.

**Stateless** means the network has no memory of its own. It does not remember previous conversations. When you send a message, your entire conversation history is re-tokenized and fed in as one long token sequence from scratch, every single time. The "memory" is just the conversation being included in the input — not stored inside the network.

**Parameters (weights)** are the numbers stored inside the network. They are what the network IS. Karpathy calls them "knobs on a DJ set" — twiddle the knobs differently and completely different predictions come out. Before training: all knobs set randomly, outputs are garbage. After training: knobs are tuned to match the statistical patterns of human text, outputs are coherent.

Every model — GPT-4, Llama 3, Claude — is just a file containing billions of these parameter values, frozen after training. When you chat with a model, the parameters do not change. You are running your token IDs through a frozen mathematical function.

**Parameters are not tokens.** Tokens = pieces of text (the vocabulary) — what goes in and comes out. Parameters = numbers inside the network that shape the math. Completely separate things.

**More parameters ≠ automatically better or newer.** More parameters = higher capacity ceiling. But how close a model gets to that ceiling depends on training data quality and training technique. Some smaller newer models outperform larger older ones. Scale matters but is not the only lever.

---

## Concept 2 — Token Embeddings

Token IDs are integers — arbitrary labels like `428` for `user`. **Integers are useless for math.** If `cat = 1` and `dog = 2`, those numbers imply dog is "between" cat and banana, and banana is three times cat. That is nonsense. You cannot do useful math with labels.

**The fix:** every token ID gets converted into a **vector** — a list of numbers. Instead of `cat = 1`, `cat` becomes `[0.2, -0.8, 0.4, 1.1, ...]` — a list of, say, 768 numbers.

**Why a list?** A single number captures one dimension of meaning. A list captures many simultaneously. One position might encode "is this a living thing?" Another: "is it positive or negative?" Another: "is it concrete or abstract?" No human assigns these meanings — they emerge from training. The result: tokens with similar meanings end up with similar vectors; unrelated tokens end up with very different vectors.

**Analogy:** GPS coordinates. A city is not just a name — it is a position in space: `[latitude, longitude]`. Two nearby cities have similar coordinates. Vectors do the same for meaning — they give tokens a position in meaning-space.

This step — token ID → vector — is called **embedding**. The lookup table storing every token's vector is called the **embedding table**. It is part of the parameters.

- GPT-4 vocabulary: 100,277 tokens
- Vector size (typical): 768 numbers per token
- Embedding table size: 100,277 × 768 ≈ 77 million parameters

More vocabulary → more tokens → more rows in the embedding table → more parameters in that table.

---

## Concept 3 — The Attention Block

After embedding, each token has a vector — but that vector only knows about itself. The vector for `blue` carries information about `blue` in general, across all training data. It does not know whether it is sitting after `the sky is` or after `feeling sad`. But meaning changes with context: `bank` after `river` means something different from `bank` after `money`.

**The attention block fixes this.** It is the step where tokens look at each other and update their vectors based on what is around them.

Every token asks: "which other tokens in this sequence are most relevant to me?" It then pulls information from those tokens proportionally, updating its own vector. A token at position 10 might pull heavily from position 3 and barely at all from other positions. The result: `bank` after `river` gets its vector shifted toward "riverbank" meaning.

**Analogy:** A meeting. Everyone arrives with their own opinion (their vector). During the meeting, people listen to each other and update their thinking. By the end, each person's position has been shaped by the room — not just their prior belief. Attention is that meeting, happening between all tokens simultaneously.

After attention: every token's vector carries context from the tokens that matter most to it.

**Attention has its own parameters** — numbers that shape how tokens attend to each other. These are separate from the MLP parameters.

---

## Concept 4 — The MLP Block

After attention mixes information across the sequence, each token's vector hits the **MLP block** (Multi-Layer Perceptron).

If attention is tokens talking to each other, **the MLP is each token thinking on its own.**

The MLP takes each token's updated vector individually and runs it through another transformation — independently, no communication with other tokens. It applies a **non-linear transformation**, meaning it can represent complex curved relationships, not just straight-line math. This is where a lot of the model's factual world knowledge lives — facts, associations, things the model "knows" — stored in the MLP's parameters.

**Analogy:** After the meeting (attention), everyone goes back to their desk to process what they heard and work through the implications alone. That solo processing is the MLP.

**The pattern repeats.** Attention + MLP = one layer. A modern Transformer runs this ~100 times. Each layer refines the vectors further. By layer 100, vectors carry rich, context-aware, deeply processed representations.

---

## Concept 5 — Logits and Softmax

After ~100 layers, the **last token's vector** is used to produce the prediction. Why the last token? Because the job is to predict what comes next — after the last thing seen.

The whole sentence runs through all the layers (attention needs all tokens present to communicate). But only the last token's vector is used at the final output step.

**Analogy:** A jury. All 12 jurors discuss the case (attention — tokens talking to each other). But only the foreperson reads the verdict (last token → output).

**Step 1 — Logits:** The last token's vector is passed through a final matrix multiplication, producing 100,277 raw scores — one per vocabulary token. These are called **logits**. They can be any number: positive, negative, large, small. `blue` might get 8.4, `banana` might get -2.1. They are not probabilities yet — just raw confidence scores.

**Step 2 — Softmax:** Softmax converts those raw scores into a proper probability distribution — all values between 0 and 1, adding up to 100%. It amplifies differences: high scores push toward 1, low scores push toward 0. `blue` → 45%, `the` → 30%, `banana` → 0.001%.

**Analogy:** Logits are raw exam scores — 84, 60, 21. Softmax converts them into percentages of total. Same information, different format.

The token with the highest probability gets picked. It gets appended to the sequence. The whole sequence is fed back in. The process repeats — one token at a time — until the response is complete.

---

## Concept 6 — Scale

Every concept above applies at every scale — from Karpathy's demo to frontier models. Same architecture. Wildly different numbers.

| Model | Parameters |
|---|---|
| Karpathy's demo model | ~85,000 |
| Llama 3 (Meta, open-source) | 405 billion |
| Frontier models (GPT-4 etc.) | Several hundred billion → ~1 trillion |

Other key numbers Karpathy mentions:
- **Layers:** ~100 in a modern state-of-the-art model
- **Context window:** hundreds of thousands to ~1 million tokens
- **Vocabulary (GPT-4):** exactly 100,277 tokens

**The key insight:** nothing architecturally changes between 85,000 and 405 billion parameters. Same steps, same structure. Bigger matrices, same operations. More parameters = more capacity to store patterns = more capable outputs.

---

## Full Architecture Flow

```
Token IDs (integers)
    ↓
Embedding Table (token ID → vector)
    ↓
[Attention Block + MLP Block] × ~100 layers
    ↓
Last token's vector
    ↓
Logits (100,277 raw scores)
    ↓
Softmax (probabilities)
    ↓
Next token (highest probability wins)
    ↓
Append to sequence → repeat
```

---

## Key Numbers

| Thing | Number |
|---|---|
| GPT-4 vocabulary size | 100,277 tokens |
| Typical vector size (embedding) | 768 numbers |
| Embedding table size (GPT-4) | ~77 million parameters |
| Karpathy's demo model | ~85,000 parameters |
| Llama 3 parameters | 405 billion |
| Frontier model parameters | Several hundred billion → ~1 trillion |
| Layers in modern transformer | ~100 |
| Context window (modern) | Hundreds of thousands → ~1 million tokens |

---

## Q&A from the Session

**Q: I don't understand the vending machine analogy — where does "punching in a code" fit?**
A: Dropped that analogy — it was confusing. Plain version: the network takes a list of numbers in (token IDs) and spits 100,277 numbers out (one per vocabulary token). Highest score = next token. Like a calculator but with a list input and a list output, not one number in one number out.

**Q: Aren't models supposed to remember what we previously asked?**
A: Models seem to remember but the network has zero memory. What actually happens: every time you send a message, your entire conversation is re-tokenized and fed in from scratch as one long flat sequence. The "memory" is the conversation being included in the input — like a folder of all previous letters handed to someone who has no memory. Context window = how big that folder can be.

**Q: How does it decide blue scores highest?**
A: That is what the entire rest of chapter 3 answers — it is determined by the parameters (knobs) tuned during training to match patterns in real text. The network saw "the sky is blue" enough times that the knobs ended up set in a way where `blue` scores highest after `the sky is`.

**Q: Do newer models always have more parameters?**
A: Not anymore. The trend shifted. Newer models get smarter through better training data and techniques, not just more parameters. Some smaller newer models outperform larger older ones. Parameters are the capacity ceiling — training determines how close you get to it.

**Q: Are parameters the same as tokens?**
A: Completely different things. Tokens = pieces of text, the vocabulary, what goes in and comes out. Parameters = numbers stored inside the network that shape the math. Tokens are the notes. Parameters are the internal mechanism of the instrument.

**Q: More vocab means more tokens means more vectors right?**
A: Yes — more vocab → more tokens → more rows in the embedding table → more vectors → more parameters in that table. But vocab size and training data size are separate decisions. More training data does not grow the vocab — it just gives more examples to train on with the same vocab.

**Q: What are transformers?**
A: "Transformer" is the name of this specific neural network architecture — the one covered this whole chapter. GPT-4, Llama, Claude are all Transformers. Before Transformers (pre-2017), RNNs processed tokens one at a time left to right and lost information over long distances. Transformers replaced that with attention — every token can directly see every other token in one shot, regardless of distance.

**Q: What are attention weights?**
A: Just the parameters inside the attention block specifically. Both attention and MLP have their own parameters. Attention parameters shape how tokens look at each other. MLP parameters store world knowledge. Same idea — parameters everywhere, split across different parts of the network.

**Q: Does the last token's vector run alone or does the whole sentence run through the layers?**
A: The whole sentence runs through all the layers — attention needs all tokens present to communicate. But only the last token's vector is used at the final output step to generate the prediction. Everyone contributes to the discussion; one person delivers the verdict.

---

## Next

**Chapter 4: Pretraining & Inference** — the training loop in detail, how the base model generates text at inference time, sampling strategies (temperature, top-k), and what "base model" behaviour actually looks like before fine-tuning.
