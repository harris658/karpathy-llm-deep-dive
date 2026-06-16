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

## Concepts Still to Cover

6. **No Persistent Self** — the model boots from zero every turn; identity is injected, not felt
7. **Models Need Tokens to Think** — distributing computation across generation steps
8. **Token Blindness** — why counting and spelling break at the character level
9. **Bizarre Distractions** — the 9.11 > 9.9 failure and how Bible-verse neurons hijack math

---

## Next

**Concept 6 — No Persistent Self:** the model has no persistent existence — it boots fresh every turn with no memory of prior conversations. Identity (name, creator, personality) is injected via the system prompt and SFT training examples, not felt from the inside.
