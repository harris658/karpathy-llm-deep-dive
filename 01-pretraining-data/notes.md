# Chapter 1: Pretraining Data — Session Notes

**Date:** 2026-05-29  
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Diagram

https://excalidraw.com/#json=fFT8Li-cJigRLKXi3qzsc,xjbJMdjDnUQDc8wPA88BFw

---

## Concept 1 — What problem does pretraining solve?

To build an AI that understands language, you can't just give it grammar rules or a dictionary. You need to show it an enormous amount of real human text and let it absorb the patterns on its own.

**Analogy:** Imagine teaching someone a language by locking them in a library with billions of books in that language. No rules explained. Just reading. After enough exposure, they start to feel how the language flows — what words follow what, how sentences connect, what a reasonable response looks like.

That's pretraining. Feed the model a massive chunk of the internet. Let it absorb patterns.

**The result** is called a **base model** — Karpathy calls it an **"internet document simulator"**. It's gotten good at predicting what text naturally comes next. It is NOT a helpful assistant yet — that comes in later chapters.

---

## Concept 2 — Where does the training data come from? (Common Crawl)

An organisation called **Common Crawl** has been crawling the internet since 2007. It starts with seed web pages, follows every link, then every link on those pages, forever. By 2024: **2.7 billion web pages** indexed.

**Analogy:** Drop a ball of string at the front door of a library, tie it to the first book, follow references to other books, keep tying. Common Crawl has done this across the entire internet for 17 years.

**The catch:** what it collects is raw HTML — tags, CSS, navigation menus, ads. Not clean article text. The data arrives dirty and needs to be processed.

---

## Concept 3 — The filtering pipeline (5 stages)

Raw HTML → clean training text through 5 sequential filters:

| Step | What it does |
|---|---|
| 1. URL Blocklist | Throw out entire domains: malware, spam, adult, racist sites |
| 2. Text Extraction | Strip HTML/CSS/nav menus — keep only the article text |
| 3. Language Filter | Keep only pages >65% English (FineWeb's threshold) — design choice with real consequences: filter out Spanish = bad Spanish model |
| 4. Deduplication | Remove copy-pasted duplicates — same article across 1000 sites |
| 5. PII Removal | Scrub addresses, Social Security numbers, phone numbers |

**Result after filtering:** 2.7B messy pages → **44 terabytes of clean text** / **~15 trillion tokens**

**Analogy:** Crude oil refining. Each stage removes something different until you have clean fuel.

---

## Concept 4 — What is a token?

Neural networks can't read text — only numbers. So text must be converted into numbers first. The units it gets split into are called **tokens**.

Why not split by letters? → sequences too long  
Why not split by words? → millions of unique words, rare ones never trained well  
**Solution:** tokens — chunks found by an algorithm called BPE. Common words = 1 token. Rare words = split into smaller pieces.

**GPT-4 vocabulary size: 100,277 tokens**

**Two numbers to keep separate:**
- **Vocabulary size** = how many unique tokens exist → 100,277 (like the 26-letter alphabet)
- **Dataset size** = how many tokens are in the training text → 15 trillion (like the total words in every book)

---

## Concept 5 — How BPE works (Byte Pair Encoding)

BPE builds the vocabulary by iteratively merging the most frequent pair of symbols.

**Algorithm:**
1. Start: every character is its own symbol
2. Scan the dataset — find the most frequent pair (e.g. `l` + `o`)
3. Merge them into a new symbol: `lo`
4. Repeat — find next most frequent pair in the updated data
5. Stop when vocabulary reaches target size (~100,000)

**Worked example:**

Dataset: `low low low lower lower newest newest`

- Round 1: `l o` most frequent → merge → `lo`
- Round 2: `lo w` most frequent → merge → `low`  
- Now "lower" = `low e r` — the `w` is absorbed into `low`
- `e w` can only form in "newest" now, NOT in "lower" (because `w` is gone)

**Key insight:** BPE is greedy and sequential. Once two characters merge, they act as one unit forever. The original parts can't participate in future pairs. This is why `lower` and `newer` may tokenize completely differently — earlier merges reshape what pairs are available.

**Why tokenization is case- and space-sensitive:**  
`hello world` (2 tokens) ≠ `helloworld` (2 different tokens) ≠ `hello  world` (3 tokens, extra space = extra token) ≠ `Hello world` (different IDs because capital H has different frequency)

**Vocabulary sizes across models:**

| Model | Vocab size |
|---|---|
| GPT-4 | 100,277 |
| LLaMA 2 | 32,000 |
| LLaMA 3 | 128,000 |
| Gemini 1.5 | ~256,000 |
| Claude | Not publicly disclosed |

Bigger vocab = shorter sequences (common patterns compressed into one token), but each token needs its own learned representation. Trend in recent models: larger vocabularies as hardware cost of the bigger output layer matters less.

---

## Concept 6 — How much does training cost?

The training hardware is GPUs (Graphics Processing Units) — originally for games, perfect for AI because both need millions of parallel calculations simultaneously.

**Setup:** 8 H100 GPUs per node → thousands of nodes per data center  
**Scale example:** Elon Musk acquiring 100,000 GPUs for one facility  
**Cloud cost:** $3 per GPU per hour to rent

**Frontier model training:** tens to hundreds of millions of dollars. Individuals can't do it.

**But costs collapse fast:**

| | Cost |
|---|---|
| GPT-2 trained in 2019 | ~$40,000 |
| Karpathy reproduced GPT-2 in 2024 | ~$600 |
| Estimated today with optimisation | ~$100 |

Three reasons for the collapse: better training data, faster hardware, better software that squeezes more out of every GPU cycle.

Yesterday's frontier = tomorrow's hobbyist project.

---

## Concept 7 — The training loop (next-token prediction)

The model doesn't read the 15 trillion tokens once and learn. It runs billions of prediction tasks on random windows sampled from that sequence.

**One training step:**
1. Pick a random window of tokens (e.g. 8,000 tokens)
2. Feed them into the network → ask: what token comes next?
3. Network outputs 100,277 numbers (one probability per token in vocab)
4. Compare against the real answer (known from training data)
5. **Backpropagation** automatically adjusts billions of parameters to make the correct token slightly more likely next time
6. Repeat with a new random window

**Important:** The tweaking is NOT done by humans. An algorithm called **backpropagation** does it automatically. Humans designed the process; they're not correcting each guess.

**Analogy:** Learning to throw darts blindfolded. Someone says "too far left" after every throw. You adjust. Over millions of throws, your aim gets accurate — not from understanding physics, but from correcting your way there.

**Same mechanism during actual use (inference):**  
When you type a question → it gets tokenized → model predicts one token → then the next → then the next. The whole response streams out one token at a time. Training vs. inference = same core loop, minus the correction step.

---

## Concept 8 — What the base model does (and doesn't do)

After training, the base model has two well-known quirks:

### Quirk 1: Memorisation / Regurgitation

Karpathy's demo: paste the opening sentence of Wikipedia's zebra article. The model recites the next several paragraphs **word for word**.

Why? Wikipedia appears in training data many times across snapshots. The model saw that zebra article so often it burned the literal content into its parameters — not just the pattern of how encyclopedias flow.

This is called **regurgitation**. It happens specifically for **oversampled** content (text that appeared far more than average). It's a known problem — better data filtering reduces it but doesn't eliminate it.

### Quirk 2: Hallucination

Karpathy's demo: ask Llama 3 about the 2024 US election (after its end-of-2023 cutoff). The model confidently invents an answer — says Trump's running mate is Mike Pence or Ron DeSantis (not JD Vance, the real answer).

Why? The model has no concept of "I don't know." It only knows "what token is most likely next." It learned that election questions get followed by candidate names. So it generates that pattern — filled with whatever names fit statistically, not factually.

**Hallucination = fluent, confident, wrong output.**

This is why the base model is not an assistant. Everything in later chapters is about fixing this.

---

## Key numbers

| Thing | Number |
|---|---|
| Common Crawl pages indexed | 2.7 billion |
| Clean dataset size (FineWeb) | 44 TB |
| Training tokens | 15 trillion |
| GPT-4 vocabulary size | 100,277 tokens |
| GPT-2 training cost (2019) | ~$40,000 |
| Karpathy's GPT-2 reproduction (2024) | ~$600 |
| Estimated today | ~$100 |

---

## Q&A from the session

**Q: So the model predicts what comes next — during training humans tweak it to generate better outputs, and even when released it predicts next tokens?**  
A: Exactly right. One precision: during training the tweaking is automatic (backpropagation algorithm), not humans manually correcting. During use (inference), same prediction mechanism — no corrections, just pure token-by-token generation. That's why responses stream in word by word.

**Q: Didn't BPE take 15 trillion tokens and produce 100,277?**  
A: No — completely different things. 15 trillion = length of training sequence (how many tokens in total). 100,277 = vocabulary size (how many unique tokens exist). Like: a 500-page novel has 150,000 total words but only 10,000 unique words.

**Q: More vocabulary is obviously better right?**  
A: Not obviously — real tradeoff. Bigger vocab = shorter sequences (faster), but each token needs its own learned slot and rare tokens barely get trained. ~100k is the current sweet spot. Trend toward larger as hardware gets cheaper.

**Q: Why didn't "lower" become `low` + `ew` + `r`?**  
A: Because by the time BPE looked for `ew`, the `w` in "lower" had already been absorbed into `low`. It no longer existed as a standalone character. BPE is greedy and sequential — merges are permanent. `ew` could only form in "newest" where `e` and `w` were still separate.

**Q: How much vocabulary do Claude models (Opus, Sonnet) have?**  
A: Anthropic hasn't publicly disclosed it. Claude uses BPE, likely 100k+ range, but the exact number is not published.

---

## Next

**Chapter 2: Tokenization** — deep dive into BPE mechanics, Karpathy's live TikTokenizer demos, and why tokenization choices affect model behaviour (arithmetic, coding, multilingual capability).
