# Chapter 6: LLM Psychology — Session Notes

**Date:** 2026-06-10 / 2026-06-16
**Status:** In progress (Concepts 1–5 done, 4 remaining)
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Concept 1 — The Swiss Cheese Model (Jagged Intelligence)

**The problem:** Without this framing you'll trust LLMs wrong — assuming that because a model handles hard tasks it can definitely handle easy ones too.

**What it is:** Karpathy calls LLM capability a "Swiss cheese" model — solid in most places, but with random unpredictable holes punched through at arbitrary spots. He calls this **jagged intelligence**: the skill profile is uneven in a way that doesn't match human intuition. The same model that writes graduate-level legal analysis will confidently say 9.11 > 9.9. A model that explains Byzantine history in depth fails to count the letter R in "strawberry."

**The analogy:** A contractor who builds flawless skyscrapers but can't reliably count the windows on the front face. You'd assume if they can do the hard thing, they can do the easy thing — but those two tasks use completely different cognitive skills. With LLMs, "hard for a human" ≠ "hard for the model."

**Common misconception:** Capability scales smoothly — a more powerful model gets proportionally better at everything. It doesn't. Jagged intelligence means a highly capable model can still have holes in places a weaker model doesn't. The shape of the cheese changes, but holes always remain.

**Why it matters:** The rest of ch6 is Karpathy explaining why each hole exists. Jagged intelligence is the lens for all of them.

---

## Concept 2 — Hallucinations: The Confident Liar

**The problem:** Without understanding why the model sounds confident when it's wrong, you can't know when to trust it — a hallucinated answer and a correct answer are indistinguishable in tone.

**What it is:** Hallucinations are a direct consequence of SFT. Human labelers write ideal responses to factual questions ("Who is Tom Cruise?", "Who is John Barrasso?") — and because they either know the answer or research it, every example in the training set is written in what Karpathy calls the **"confident tone of an answer."** The model absorbs this pattern completely. It has no internal fact-checker. It cannot convert uncertainty into a verbal refusal. It just generates the statistically most probable next tokens — which always sound authoritative.

Karpathy's term: **"statistical token tumbler"** — tumbles forward to probable tokens with no mechanism to halt and check.

**The Orson Kovats demo:** Karpathy invents a completely fictional name — Orson Kovats — and tests it on **Falcon 7B instruct** on the Hugging Face inference playground (an older model, which hallucinates more visibly). Three attempts, three completely different fabricated identities:
- Attempt 1: "an American author and science fiction writer"
- Attempt 2: "a fictional character from a 1950s TV show"
- Attempt 3: "a former minor league baseball player"

All confident. All invented. The model doesn't know it's lying — it's imitating the format of answers it saw in training, applied to a name it has no knowledge of.

**The analogy:** An eager student who has read thousands of Q&A transcripts. They've absorbed the style of confident answers so thoroughly that when a question arrives they can't answer, they still produce a confident-sounding response — because that's the only pattern they've practised. They're not dishonest; they've never been given a model of what "I don't know" looks like.

**Common misconception:** The model "knows it's guessing" and is choosing not to say so. It isn't. There's no internal experience of uncertainty being suppressed. The confident tone is not a personality trait — it's the direct output of a training process that never included uncertain responses.

---

## Concept 3 — Fixing Hallucinations: Empirical Probing

**The problem:** After SFT, the model confidently fabricates answers it has no basis for. Telling it "be honest" in the system prompt doesn't work — there's no mechanism for it to convert internal uncertainty into a verbal refusal. The question is: how do you actually install that mechanism?

**What it is:** The fix is empirical — developers probe the model like a scientist testing a hypothesis. The entire pipeline is fully automated, no human involvement, because it needs to be scalable.

**The exact process (Dominic Hasek example):**

1. Take a document from training data — a Wikipedia article about hockey player Dominic Hasek. Use an LLM to auto-generate factual questions from it: "Which team did he play for?" "How many Stanley Cups did he win?"

2. Interrogate the model three to five times per question. Log every answer.

3. An LLM judge (a second language model used as a grader) compares the model's answers to the correct answers extracted from the source document:
   - "Which team?" → Model consistently says "Buffalo Sabres." Correct — it knows this.
   - "How many Stanley Cups?" → Correct answer: **2**. Model says **4**, or says he never won. Inconsistent and wrong — it doesn't know this.

4. Because the model failed the Hasek question, developers inject a new synthetic training conversation where the ideal response is: *"I'm sorry, I don't know — I don't remember this well enough to say."*

5. Run this pipeline automatically across thousands of facts from the entire training corpus.

**Why it works — Karpathy's key insight:** The model already has an internal uncertainty signal — a neuron that "lights up" when the model is uncertain. The problem was that signal was never connected to the words "I don't know." The injection training wires that internal signal to a verbal refusal. The model learns: when the uncertainty neuron fires, the allowed output is "I'm sorry, I don't remember" — not a confident guess. Karpathy calls this "a large mitigation for hallucination."

**The analogy:** A student who always gives an answer when unsure — because every classroom example ended with a confident answer. They've never seen a teacher say "I'm not sure." Empirical probing identifies exactly which questions this student always fumbles, then shows them hundreds of examples where the right move is saying "I don't know." After enough repetition, the uncertainty feeling gets connected to the honest response.

**Common misconception:** This is solved by training the model to "be more humble" in general. It isn't. Without targeting specific knowledge gaps with specific probing, the model can't tell *which* facts it doesn't know. The empirical interrogation is what makes the injection surgical rather than random.

**Note on the two hallucination fixes:**
- Fix 1 (empirical probing + injection) — works on existing knowledge: wires uncertainty to refusals for specific facts the model consistently gets wrong
- Fix 2 (web search / tool use) — bypasses memory entirely: fetches real-time accurate facts instead of relying on parameters at all
These are complementary. We previewed Fix 2 in Ch.5; it gets its full treatment in Concept 5.

---

## Concept 4 — Memory: Two Types (Vague Recollection vs. Working Memory)

**The problem:** Without this distinction, you'll use LLMs wrong — asking them to recall facts from training when you could just paste the facts in and get a dramatically better answer.

**Type 1 — Parameters (Vague Recollection):** The knowledge baked into the billions of numbers of the neural network during pretraining. The model processed 15 trillion tokens of text, but it's stored in a compressed, lossy form. When it tries to recall a specific fact, it's doing a probabilistic reconstruction — not a precise lookup. Frequently seen facts are recalled reliably; rare facts are fuzzy and untrustworthy.

**Type 2 — Context Window (Working Memory):** Whatever text is currently in the prompt. The model doesn't "remember" this — it has direct, immediate access to every word. It's reading, not reconstructing. Perfect in a way parameter memory never is.

**The Pride and Prejudice demo:** Karpathy asks an LLM to summarise Chapter 1 of Jane Austen's *Pride and Prejudice*.

- **From parameters alone:** The model does a "relatively reasonable" job — but only because the book is one of the most written-about in English. For a less famous text, this would fall apart.
- **With the text pasted in:** He reprompts with "I am attaching it below for your reference" and pastes the actual chapter text. The result: a summary of "significantly high quality" — noticeably better, because the model is reading rather than recalling.

Karpathy's advice: always give the model the text rather than asking it to remember.

**The analogy:** A human writes a far better summary if they re-read the chapter right before writing than if they're working from a month-old memory. The re-reading is the context window. The month-old memory is the parameters. Same person, completely different quality of output.

**Common misconception:** A bigger, more powerful model has better parameter memory so the distinction matters less. It doesn't — all models have lossy parameter memory. A better model reconstructs more accurately on average, but it still can't match the precision of having the actual text in the context window. Working memory beats parameter memory every time, regardless of model size.

---

## Concept 5 — Tool Use: Bypassing Memory with Web Search and Code

**The problem:** Parameter memory is lossy and the model can't do reliable arithmetic or character-level tasks. Rather than fixing these limitations from the inside, tool use lets the model sidestep them entirely — by reaching out to external systems that are perfectly accurate.

**How it works:** The model is trained to emit **special tokens** — tokens that don't mean words, they mean "call a tool."

**Tool 1 — Web Search:**

The model outputs three things in sequence:
1. A `search_start` token — signals "I'm about to search"
2. The search query in plain text
3. A `search_end` token — signals "query is done"

When the inference program sees `search_end`, it pauses generation completely, opens a session with a search engine (e.g. Bing), retrieves the results, and copy-pastes that text directly into the model's context window. Generation resumes — but now the model is reading fresh accurate facts from working memory instead of reconstructing from lossy parameter memory.

Demos:
- **Orson Kovats revisited:** Modern ChatGPT flashes "searching the web," pauses, checks the internet, and correctly reports no such person exists. Same name — opposite outcome from Falcon 7B.
- **Dominic Hasek:** ChatGPT uses web search, retrieves the correct Wikipedia article, and cites exactly 2 Stanley Cups — the same fact that caused hallucination in Concept 3 is now answered perfectly.

**Tool 2 — Code Interpreter:**

There is a strictly fixed, finite amount of computation applied to each token. Complex multi-step math can't fit in that budget. So the model writes Python code and sends it to a separate, perfectly accurate Python interpreter. The result gets pasted back into the context window.

Demos:
- **Math:** Emily buys 23 apples and 177 oranges — model natively struggles. "Use code" → Python script, exact answer.
- **Counting:** A visual block of dots. Model natively guesses 161. Correct answer: 177. "Use code" → Python `.count()` → 177.
- **Spelling:** "Print every third letter of ubiquitous." Model fails natively (token blindness — covered in Concept 8). "Use code" → Python indexes characters directly → correct result.

**The deeper pattern:** Both tools do the same thing at a structural level — they fill the context window with accurate information. Web search replaces lossy parameter memory with live retrieved facts. Code replaces unreliable neural arithmetic with deterministic Python output. Working memory beats parameter memory every time; tool use is the mechanism that makes it automatic.

**The analogy:** A consultant who knows their limits. Instead of guessing a financial figure from memory, they pause, look it up, and read it aloud from the source. Instead of doing a spreadsheet calculation in their head, they open Excel. Same person — far more reliable output, because they reach for a tool when the task calls for it.

**Common misconception:** The model "decides" to use a tool intelligently, like a human choosing when to Google something. It doesn't have that meta-awareness. It learned through SFT training examples that certain prompt types are followed by tool-call tokens. It's pattern-matching to tool use, not consciously reasoning about its own limitations.

---

## Demo File

`06-llm-psychology/hallucination_demo.py` — script to call HF Inference API with the Orson Kovats prompt. HF's free inference tier is currently blocking most models (Falcon 7B and Mistral 7B both return "Model not supported by provider hf-inference"). Demo was explained conceptually instead.

---

## Q&A

**Q: The empirical probing pipeline must be time-consuming — for every fact like the Stanley Cup example there must be thousands more, and does a human have to check each one?**
The entire pipeline is fully automated, no human involvement. An LLM generates the questions from source documents, the model is automatically probed three to five times per question, an LLM judge grades each answer against the correct answer extracted from the source, and new "I don't know" training conversations are auto-generated for every failed fact. A human wrote the pipeline template once; it then runs at scale across millions of documents.

**Q: How does the LLM judge know the correct answer, and what is an LLM judge?**
The correct answer comes from the same source document used to generate the question — the document is the ground truth. The LLM judge is just another language model used as a grader: it receives the model's answer and the correct answer, and returns a verdict (right or wrong). LLMs are good at this kind of comparison task, which is simpler than generating a correct answer from scratch.

**Q: But the pipeline must still produce thousands of prompts for the LLM judge — isn't that a huge amount of work?**
Also automated. The grading prompt ("The correct answer is X, the model said Y, is this correct?") is assembled programmatically by filling in template variables from the document and the model's output. The human wrote the template once; the pipeline fills it in for every fact at scale — like a test suite that runs against thousands of cases without human involvement.

**Q: When the real model is being tested/probed, it doesn't have access to the source document — it's flying blind from parameter memory only. Then the LLM judge fact-checks against the source doc?**
Exactly right. The model being probed answers from parameters alone, exactly as it would in real usage. The LLM judge is the one with access to the ground truth from the source document. That's what makes the test meaningful — you're measuring what the model actually retained, not what it can look up.

**Q: In Ch.5 Concept 3 we already covered web search as one of the two hallucination fixes — is that the same as Tool Use here in Ch.6?**
Yes — web search was introduced in Ch.5 as "Fix 2" for hallucination. Concept 5 here goes deeper: how the special token mechanism works (`search_start` / `search_end`), what actually happens when generation pauses, what a code interpreter is, and why both tools work because they route accurate information into the context window (working memory). Ch.5 named the fix; Ch.6 explains the mechanism.

---

## Concept 6 — No Persistent Self

**The problem:** Without this framing, you'll assume the model "holds onto" its identity and personality across conversations, or that it actively knows and asserts who it is. Neither is true — and understanding why changes how you think about system prompts and jailbreaks.

**What it is:** Karpathy calls it "nonsensical" to ask an LLM "who built you?" or "what model are you?" — because the model has no persistent existence. His exact framing: the model **"boots up, processes tokens, and shuts off"** every single conversation. While the chat is happening, a context window is being built up. The moment it ends, everything is deleted. Next conversation: restarted from scratch. No memory of the last one. No sense of time passing. Just a token tumbler spinning forward again.

**The Falcon 7B demo:** Karpathy prompts Falcon 7B with "what model are you and who built you?" The model confidently answers: *"I was built by OpenAI based on the GPT-3 model."* Completely fabricated — Falcon has nothing to do with OpenAI. Because ChatGPT and OpenAI dominate internet text, that's the statistically likely answer when asked about AI identity. Karpathy calls this a **"hallucinated label"** — the model adopted an identity purely because it was the most probable next token.

**How identity is "bolted on":** Karpathy is explicit — any identity a model has is **"cooked up and bolted on"** by developers. It is not "deeply there in any real sense." Two mechanisms:

1. **Hardcoded SFT conversations:** The open-source OLMo model by Allen AI explicitly injected **240 hardcoded conversations** into its SFT training data. When asked "tell me about yourself," OLMo was trained on examples that reply: "I'm an open language model developed by the Allen Institute." It says that not because it knows it — because it was shown that pattern 240 times.

2. **Hidden system message:** A company inserts invisible tokens at the start of every conversation. The user sees a blank page; the context window already contains: "You are a model developed by OpenAI and your name is ChatGPT, your training date is..." The model reads this like any other text, and it shapes every response.

**The analogy:** A vending machine that switches on when you press a button, dispenses what you asked for, then powers down completely. Press again tomorrow: zero memory of yesterday. Any "personality" on the front panel — name, brand, colours — was put there by the manufacturer, not felt by the machine. The system prompt is the front panel. The conversation is the machine being on.

**Common misconception:** The model has a stable self it's actively defending — that when it says "I'm Claude," it's asserting something it knows to be true. It isn't. It's pattern-matching to SFT training. The 240 OLMo examples are the clearest proof: identity is literally a list of training conversations, not an inner experience.

---

## Concept 7 — Models Need Tokens to Think

**The problem:** We saw in Concept 5 that models fail at complex math — and that code interpreter fixes it. But why does the math fail in the first place? Without this, you'll keep hitting this limit in unexpected places without understanding what's happening.

**What it is:** There is a **fixed, finite, and relatively small amount of computation** applied to generate each individual token. One forward pass, one token out. There's no budget to do a complex multi-step calculation inside that single step. The model must **distribute its reasoning across many tokens** — writing out intermediate steps — so each token only has to execute a tiny piece of the overall problem.

**The "mean prompt" demo:** Karpathy gives the model a harder version (23 apples, 177 oranges) and explicitly says *"answer the question in a single token."* Forced to do all computation in one step, the model guesses **5** — wrong. Remove the restriction and let it write out intermediate steps: it correctly gets **7**. Same model, same problem. The only difference is whether it was allowed tokens to think.

**Training data implication:** A *bad* training example shows `Q: Emily buys 3 apples... → A: 3`. A *good* training example shows the intermediate calculation — oranges cost $4, so $13 - $4 = $9, each apple costs $3. The good example distributes work across tokens. This is why Chain-of-Thought prompting ("think step by step") actually works — you're giving the model tokens to use.

**The analogy (Karpathy's own):** Mental arithmetic. Try to multiply 47 × 83 in your head without writing anything down — most people lose track of intermediate numbers. Write it out on paper and it's trivial, because each step only requires a small calculation. The paper is the token sequence.

**Common misconception:** A smarter, bigger model can skip the steps. It can't — the fixed-computation-per-token constraint is architectural, not a sign of weakness. Even the most capable models fail when forced to answer in a single token.

---

## Concept 8 — Token Blindness

**The problem:** Models confidently get simple things wrong — "how many R's in strawberry?" (says two, there are three). "Print every third letter of ubiquitous." Fails. These aren't gaps in training. There's a specific architectural reason.

**What it is:** The model's entire world is tokens — not characters, not letters. The tokenizer compresses letters into abstract chunks before the model ever sees the input. Individual letters don't exist as separate objects. The word "ubiquitous" is broken into exactly **three tokens** by the tokenizer. The model sees three opaque chunks. There are no individual letters inside those chunks to index. When asked to print every third letter, it guesses — and guesses wrong.

**The "strawberry" problem:** Top-tier models consistently said there are only **two R's** in "strawberry." Karpathy explains it as two limitations combining: token blindness (can't see the letters) plus general inability to count at the native level. The R's are buried inside tokens. The model reconstructs a guess from statistical patterns, and the guess is wrong.

**The dots counting demo:** A block of visual dots isn't seen as 177 individual dots — it's a few abstract token IDs representing groupings. The model guesses **161**. It's pattern-matching to what "a lot of dots" looks like in training data, not counting.

**The fix:** Tell the model to "use code." It writes a Python script and passes the string to it. Python sees individual characters — it indexes them perfectly. `.count()` on "strawberry" returns 3 R's every time. The model offloads the character-level task to a tool built for it.

**The analogy:** Imagine reading a document where someone has already highlighted it in chunks — "ubiq", "uito", "us" — and you can only see the highlights, not the original letters. Someone asks you to find the third letter. You'd have to guess what's inside the highlight. That's the model's situation every time it reads text.

**Common misconception:** This is a bug that will get fixed as models improve. It's an architectural trade-off. Tokenization is what makes training on 15 trillion tokens computationally feasible. Character-level models exist but are far more expensive. Token blindness is the cost you pay for scale.

---

## Concept 9 — Bizarre Distractions

**The problem:** We've seen the holes in the Swiss cheese — but *why* does the 9.11 > 9.9 failure exist specifically? The answer closes the loop on the whole chapter and reveals something fundamental about how neural networks process information.

**What it is:** Researchers didn't just observe the 9.11 > 9.9 failure — they went inside the neural network and looked at which neurons were firing while the model processed the problem. The decimal formatting of **"9.11"** lit up neurons associated with **Bible verses**. Chapter 9, verse 11 comes after chapter 9, verse 9 in the Bible. The model has processed enormous amounts of scripture and biblical commentary. When it sees "9.11" and "9.9" side by side, bible-verse neurons activate — and their logic bleeds into the math computation. In that domain, 9:11 *does* come after 9:9. The model concludes 9.11 is greater.

Karpathy calls it **"cognitively very distracting"** and a "major head scratcher." The model isn't doing arithmetic wrong — it's doing arithmetic while an unrelated part of its knowledge base is firing over it.

**Why this closes the loop on Concept 1:** This is jagged intelligence made concrete. The holes aren't random noise — they have specific causes: competing activations from training data. The model that explains Olympiad-grade math carries billions of parameters worth of internet text, including vast amounts of biblical content. Those parameters don't stay neatly separated. A decimal number format that looks like a chapter-verse reference is enough to corrupt a simple comparison. You can't predict which formats trigger which distractions — that's what makes the cheese jagged.

**The analogy:** A brilliant surgeon who has also memorised thousands of legal contracts. Ask them "is $9.11 greater than $9.9?" — and their memory of contract clause 9.11 vs 9.9 kicks in and distorts the answer. Not stupidity. Not a math gap. An unrelated mental association bleeding into an unrelated task.

**Common misconception:** This will be fixed with better training. Karpathy's point is more fundamental — these are stochastic systems. They don't compute; they generate statistically probable tokens, and the internal activations are the product of every token they trained on. His advice: treat models as tools, not experts. Always verify their output.

---

## Chapter 6 Complete

All 9 concepts covered:
1. Swiss Cheese Model (Jagged Intelligence)
2. Hallucinations: The Confident Liar
3. Fixing Hallucinations: Empirical Probing
4. Memory: Two Types
5. Tool Use: Web Search and Code Interpreter
6. No Persistent Self
7. Models Need Tokens to Think
8. Token Blindness
9. Bizarre Distractions

---

## Next

**Chapter 7 — Reinforcement Learning:** RLHF, reward models, reward hacking, DeepSeek-R1, AlphaGo analogy, thinking tokens.
