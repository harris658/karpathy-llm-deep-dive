# Chapter 1: Pretraining Data — Session Notes

**Date:** 2026-05-29

## What we covered

8 concepts taught end-to-end:

1. **What problem pretraining solves** — feed the model massive text so it absorbs language patterns. Result: an "internet document simulator", not yet an assistant.
2. **Common Crawl** — org that has crawled 2.7B web pages since 2007 by following links. Raw HTML, needs cleaning.
3. **The filtering pipeline** — 5 sequential stages: URL blocklist → text extraction → language filter (>65% English) → deduplication → PII removal. Output: 44 TB / 15T tokens (FineWeb).
4. **Tokens** — the atomic units the model reads. Not words, not letters — chunks found by BPE. GPT-4 vocab: 100,277 tokens.
5. **BPE (Byte Pair Encoding)** — iteratively merges the most frequent pair of symbols until target vocab size is hit. Greedy and sequential — once merged, the original parts can't form new pairs.
6. **Training compute and cost** — tens/hundreds of thousands of GPUs, millions of dollars for frontier models. GPT-2 (2019): $40k to train; Karpathy reproduced it in 2024 for $600, estimates $100 today.
7. **Next-token prediction loop** — sample a random window of tokens, predict the next one, auto-adjust parameters if wrong. Repeat billions of times across 15T tokens.
8. **Base model quirks** — memorises oversampled text (zebra Wikipedia demo); hallucinates past its knowledge cutoff (2024 US election demo with wrong VP picks).

## Key numbers to remember

| Thing | Number |
|---|---|
| Common Crawl pages | 2.7 billion |
| Clean dataset size | 44 TB |
| Training tokens | 15 trillion |
| GPT-4 vocab size | 100,277 tokens |
| GPT-2 training cost (2019) | ~$40,000 |
| GPT-2 reproduction (2024) | ~$600 |

## Diagram

https://excalidraw.com/#json=fFT8Li-cJigRLKXi3qzsc,xjbJMdjDnUQDc8wPA88BFw

## Next

Chapter 2: Tokenization — deep dive into BPE mechanics, the TikTokenizer demos, and why tokenization choices affect model behaviour.
