# Chapter 8: Future Directions — Session Notes

**Date:** 2026-06-23
**Status:** Complete (6 concepts)
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Concept 1 — Multimodality

**Why it exists:** LLMs built on text only can't process what most of reality is made of — images, sounds, video. A text-only model can't hear a spoken question, look at a photo, or watch a tutorial. The question is whether handling these requires a completely different neural network.

**What it is:** No new architecture is needed. The transformer stays exactly as-is. The trick is tokenization. Everything the transformer processes is a sequence of tokens — and you can tokenize anything, not just text.

For images: slice the image into small square patches and convert each patch into a token. Those image-patch tokens go directly into the sequence alongside text tokens. For audio: compute a spectrogram (a visual representation of frequencies over time), slice it into strips, convert each strip to a token. The transformer processes text tokens, image-patch tokens, and audio tokens in one unified sequence — it doesn't know or care where each token came from.

**The analogy:** A translator who has only worked with books. To handle photos and recordings, you find a universal encoding that converts them into something the translator already understands, then use the same translator for everything. Tokenization is that encoding — image patches and spectrograms get converted into the same token language the transformer already speaks.

**Why it matters:** The architecture is proven and deployed today. GPT-4o and Gemini already handle text, images, and audio natively using this approach. Karpathy frames it as "future directions" because today it's uneven across the industry — only frontier models have it. The trend is it becoming the norm everywhere.

**Common misconception:** Multimodality requires a fundamentally different architecture designed from scratch for visual or audio data. It doesn't. The transformer is a sequence processor — it doesn't care what tokens represent, only how they relate. What changes is the tokenizer (the front-end conversion), not the model itself.

---

## Concept 2 — Agents and Long-Running Tasks

**Why it exists:** Today every LLM interaction is one exchange — you prompt, it responds in seconds, done. Most meaningful real-world work isn't like that: it requires multiple steps, checking results mid-way, adjusting course, and making decisions over time. A model that can only do one prompt-response cycle can't tackle any of it autonomously.

**What it is:** Karpathy describes the current state plainly: models are good at individual tasks handed to them "on a silver platter." What they can't yet do reliably is *string tasks together in a coherent, error-correcting way over long periods of time*.

Agents fix this. An agent isn't a smarter model — it's a model that operates *over time*. Instead of responding in two seconds and stopping, it executes a job that might span tens of seconds, minutes, or hours. It does step 1, checks the result, does step 2, handles errors, loops back if something goes wrong, and periodically checks in with the user to report progress before continuing.

**The human-to-agent ratio:** Because agents make mistakes — they're not infallible — active human supervision is required. Karpathy introduces the "human to agent ratio," drawn directly from the "human to robot ratio" used to measure automation in physical factories. As automation improves, one human can supervise more robots. The same will apply digitally: as agents become more reliable, one person will be able to supervise more agents simultaneously. The human's role shifts from *executing* tasks to *supervising* them.

**The analogy:** A law firm. A partner assigns research to a junior associate, who goes away and comes back with a memo. The partner reviews, gives feedback, sends them back. The partner isn't doing the research — they're supervising it. An agent workflow is the same dynamic, compressed in time. The agent is the associate. You're the partner. Except now one partner can supervise 20 associates running parallel workstreams simultaneously.

**Common misconception:** "Agents" means fully autonomous AI that needs no human involvement — set it and forget it. Karpathy is explicit that this isn't the case. Agents make mistakes. The human role doesn't disappear; it transforms. You stop being the executor and become the supervisor: monitoring the work, catching errors, redirecting when the agent goes off track.

---

## Concept 3 — Computer Use

**Why it exists:** Even a sophisticated agent that plans a ten-step workflow can't execute most of those steps. Most of the world's software has no API. You can't programmatically book a restaurant, fill out a government form, or use an internal HR tool by calling a function. Those things require a human to look at a screen and click. If the model can't do that, a human still has to step in for every real-world action — which defeats the purpose of the agent.

**What it is:** Computer use means the model gets a screenshot of your screen and can issue keyboard and mouse commands — click, type, scroll, drag. It sees what you see, and it can act the way you act.

Karpathy points to ChatGPT's "Operator" launch as the early real-world version of this. His exact description: *"handing off control to the model to perform keyboard and mouse actions on your behalf."* The model navigates pages, fills forms, and clicks buttons — operating any software without needing that software to have an API.

He also describes the broader direction as AI becoming "a lot more pervasive and invisible" — integrating seamlessly into everyday tools so that the handoff to the model is frictionless.

Computer use closes the loop from Concept 2: agents plan and sequence work; computer use is how they *execute* it in the real world.

**The analogy:** A personal assistant who can only communicate by reading documents and typing replies can advise you but can never log into your accounts or fill out a form. Give that assistant eyes and hands — a screen and a keyboard/mouse — and they can act for you directly. Computer use is giving the model eyes (the screenshot) and hands (the keyboard/mouse commands).

**Common misconception:** Computer use is a scripted macro — it follows a fixed path. It doesn't. The model looks at the actual screen at each step and decides what to do next based on what it sees, exactly like a human would. If an unexpected popup appears, it handles it. If the page loaded differently, it adapts. It's live visual reasoning driving live actions. The limitation isn't intelligence — it's reliability and speed. It's slower than an API, and it can still make mistakes a scripted macro wouldn't.

---

## Concept 4 — Test-Time Training

**Why it exists:** Every current LLM has a hard line between training (parameters updated) and inference (parameters frozen). Once deployed, a model learns nothing. The only workaround is the context window — stuffing relevant information into the prompt. But this is a finite resource and, Karpathy argues, a trick that doesn't scale to the long-running, multimodal tasks agents will be doing.

**What it is:** When training ends, a model's parameters — its billions of weights — are permanently locked. Every task it runs after that uses the same static snapshot from training day. The only thing that changes at runtime is the context window: the tokens currently in front of the model. Karpathy calls this "in-context learning" — not real learning, just using whatever tokens are in the prompt right now. The model doesn't remember anything across conversations. It doesn't get better with use. It doesn't update.

**Why expanding the context window won't scale:** Developers have compensated by making context windows bigger — from 4K tokens to 128K to 1M+. If the model can't learn, at least give it more room to hold information temporarily. Karpathy says this hits a wall once tasks become long-running and multimodal. An agent watching eight hours of video or running for three days on a research project would need hundreds of millions of tokens — far beyond what any context window can hold. The approach doesn't scale.

**The sleeping brain analogy:** Human brains don't have this problem because they update continuously. Karpathy's exact phrasing: *"especially when you sleep... your brain is updating your parameters."* Daily experiences consolidate overnight. You wake up slightly different from who you were the day before. Current LLMs have no equivalent — they never sleep, their parameters never update, every session starts from the same frozen weights.

Test-time training is the research direction aimed at fixing this: models that actively update their parameters *during inference*, not just read from a context window. Karpathy frames it as a major open research problem, not a shipped feature.

**Common misconception:** Fine-tuning already solves this — you update the model's weights on new data. Fine-tuning is a *separate training run*, not something that happens live during inference. The model stops serving users, gets retrained, and gets redeployed. Test-time training means weights update *as the model is actively running a task* — closer to how a human brain works mid-experience, not a periodic software update.

---

## Concept 5 — Keeping Track of AI Progress

**Why it exists:** AI moves faster than any other technology field. A model that was state-of-the-art six months ago is mid-tier today. If you're not actively tracking the field, your mental model of what AI can do decays within weeks.

**What it is:** Karpathy recommends three specific resources, each covering a different update frequency and depth.

**1. The LLM Leaderboard (Chatbot Arena)**
A leaderboard that ranks the top models — Gemini, OpenAI, Anthropic, DeepSeek, Meta — using blind human comparisons. Real users send the same prompt to two anonymous models, pick the better response without knowing which model generated which, and the winner gets points. Because it's crowd-sourced from millions of real interactions, it's harder to game than a benchmark written by the model's own creators.

Karpathy adds a major caveat: the leaderboard has become "a little bit gamed" in recent months. He notices capable models (specifically calling out Anthropic's Sonnet) ranking suspiciously low. His advice: use it as a *first pass* to see who the top contenders are, then try the top few yourself on your actual use cases — what works best for you may not match the crowd's rankings.

**2. AI News Newsletter**
Published by "swix and friends" — nearly every other day. Extremely comprehensive. Uniquely, it is human-curated and editorially overseen, but the actual summaries and content are constructed automatically using LLMs. Karpathy says the top-level summaries are particularly good for staying oriented without reading every paper and announcement.

**3. X (Twitter)**
Karpathy's direct quote: *"a lot of AI happens on X."* New model drops, research previews, demos, hot takes from researchers — it surfaces there days or weeks before it hits anywhere else. His advice: find people in the AI space you like and trust, and follow them.

**The analogy:** Like tracking financial markets. The leaderboard is a market index — gives the broad picture but is a lagging indicator and can be distorted. The newsletter is a daily analyst brief — synthesised, curated, good for daily orientation. X is the trading floor — raw, fast, sometimes noisy, but where you hear things first.

**Common misconception:** The leaderboard is ground truth — if model X ranks higher than model Y, X is better for you. Rankings are averages across millions of users and tasks. Your specific task may behave differently. The leaderboard narrows the field; it doesn't make the final call. Try the top few yourself.

---

## Concept 6 — Where to Find Models

**Why it exists:** Knowing the theory doesn't tell you where to actually go to use a model. The landscape is fragmented — different models live in different places, with different access modes. Without a map, you end up defaulting to whatever you stumbled on first.

**What it is:** Karpathy organises access by two axes: who owns the weights (proprietary vs. open) and where it runs (cloud vs. local), plus one special case for base models.

**1. Proprietary models — go directly to the provider**
OpenAI, Google, and Anthropic don't release their weights publicly. You use them through their own platforms: ChatGPT for OpenAI, AI Studio for Gemini, Claude.ai for Anthropic. There's no alternative access point.

**2. Open-weight models — Together.ai**
Meta's Llama, DeepSeek, Mistral publicly release weight files. Anyone can download and run their own instance — but hosting a 70B-parameter model needs a server room's worth of GPU. **Together.ai** is an inference provider that hosts state-of-the-art open-weight models for you. You go to their site, pick a model, and chat with it in a browser. No setup, no hardware.

**3. Base models — Hyperbolic**
A base model is the raw neural network immediately after pre-training — before SFT, before RLHF. It doesn't answer questions; it continues text. It's an "internet text token simulator" — pure autocomplete. Most platforms only host assistant-fine-tuned versions. **Hyperbolic** specifically hosts raw base models, including Llama 3.1 at 405 billion parameters. This is where you go if you want to see what pre-training alone produces.

**4. Local execution — LM Studio**
The biggest frontier models are too large for a laptop. But smaller, compressed (distilled) versions run at reduced precision, trading some accuracy for a fraction of the memory footprint. These run fully offline on a MacBook Pro GPU. **LM Studio** is a desktop app that manages model downloads, precision settings, and local inference. Karpathy is honest: the UI is geared toward professionals, presents hundreds of model variants and precision levels, and can be confusing. But once a model is loaded, it works — nothing leaves your machine.

**The analogy:** Coffee. Proprietary models are a specialty café — you go to their location, use their machine, get their product. Open-weight models are beans with a published recipe — the beans are free, but you still need someone to run the espresso machine (Together.ai). Base models are raw green unroasted beans — most people never see them, but Hyperbolic sells them to you. LM Studio is your home espresso machine — smaller batches, less precision than the café, but entirely yours and offline.

**Common misconception:** "Open source" and "open weight" mean the same thing. They don't. Open-weight means the trained weights are publicly released — you can download and run the model. Open source strictly means the full code, training data, and pipeline are also public. Most "open" models (including Llama) are open-weight but not fully open source. For *using* a model, open-weight is what counts. For *reproducing* a model from scratch, the distinction matters.

---

## Demos

| Demo | What it shows |
|------|--------------|
| ChatGPT Operator | Early real-world computer use: model takes keyboard and mouse control on user's behalf |
| Chatbot Arena (leaderboard) | Blind human comparison ranking — two anonymous models, user picks the better response |

---

## Key Numbers

| Number | What it refers to |
|--------|--------------------|
| 405B | Llama 3.1 base model parameter count, hosted on Hyperbolic |
| 1M+ | Approximate upper range of current context windows (still insufficient for long-running multimodal tasks) |

---

## Q&A

**Q: So current models can already see all three — text, audio, and image?**
Some frontier models already do: GPT-4o handles text, images, and audio in one model; Gemini does too. The architecture Karpathy describes is how they actually work right now, not a hypothetical. Claude (at the time of the session) handles text and images but not native audio. It's uneven across the industry — only the frontier has it today. The "future direction" is it becoming the norm everywhere, and quality improving further. The key word in Karpathy's framing is "natively" — early multimodal systems were bolted together (separate image model, separate audio model, stitched by wrappers). The direction is one unified model thinking in all modalities at once.

---

## Diagram

Not yet created.

---

## Next

This is the final chapter of Karpathy's LLM deep dive. The full 3.5-hour video is now covered across 8 chapters.
