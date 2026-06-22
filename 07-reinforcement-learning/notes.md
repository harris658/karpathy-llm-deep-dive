# Chapter 7: Reinforcement Learning — Session Notes

**Date:** 2026-06-22
**Status:** Complete (7 concepts)
**Source:** Karpathy LLM Deep Dive (NotebookLM notebook `c43662e9-4bcb-4f29-a8e0-9a4a7990d835`)

---

## Concept 1 — The "Going to School" Analogy

**The problem:** After SFT we have a capable model, but no framing for why a third training stage exists at all. Without this, RL feels like a mysterious add-on.

**What it is:** Karpathy frames the full training pipeline as a school education:

- **Pre-training = Reading the textbook.** The model absorbs vast internet text, building up a general knowledge base. It doesn't yet know how to answer anything — just what the world looks like in text.
- **SFT = Studying worked solutions.** Human experts write ideal step-by-step responses. The model learns format, tone, and structure by imitating them.
- **RL = Practice problems.** You get the question and the final answer only — no steps. You attempt the problem, check whether your answer was right, and try again. Over thousands of attempts you discover the strategies that work for you — not strategies copied from a human, but ones your own cognition finds reliable.

**The analogy:** Learning to cook: reading recipe books (pre-training), watching a chef demonstrate a dish exactly and copying their moves (SFT), then being handed a dish and told "make something that tastes like this" — no recipe, pure experimentation until you develop your own instincts (RL).

**Why it matters:** SFT is fundamentally capped at the ceiling of human performance. RL can break through it — the model discovers reasoning strategies no human trainer demonstrated. That's a difference in kind, not just degree.

**Common misconception:** RL just "polishes" SFT — a minor refinement. It isn't. Karpathy calls it the "most experimental" stage: the one capable of producing abilities that go beyond what human trainers showed.

---

## Concept 2 — The Token Path Problem

**The problem:** SFT assumes that the steps a human writes are the right steps for an LLM to follow. This assumption is wrong — and it's the specific reason a third stage is needed.

**What it is:** Karpathy looks at four different human-written solutions to the Emily/apples/oranges problem, all reaching $3. Some are short and efficient; some are verbose. A human labeler naturally prefers the clean, concise solution — but that's the problem.

Humans process math fluidly and in parallel. An LLM processes one token at a time, with a fixed tiny budget of computation per token (Ch.6 Concept 7). A "short" human solution might compress several arithmetic steps into a single token, forcing the LLM to make a massive cognitive leap in one step — exactly when it hallucinates or fails.

At the same time, a very verbose solution might spell out steps that are trivially easy for the LLM — wasting tokens on things it doesn't need.

Karpathy's key line: **"We are not in a good position to create these token sequences for the LLM."** The human doesn't know which path the model's neural architecture prefers — whether it reasons better in English prose, as algebraic equations, or as pseudocode.

**What RL fixes:** Don't guess — let the model discover its own optimal paths. Give it the problem and the final answer. Generate millions of attempts (the model is stochastic, so it wanders down many different token paths). Check each path's final answer automatically. Reinforce paths that reach the correct answer. Discard paths that fail. Over tens of thousands of problems, the model teaches itself which token sequences work for its architecture.

**The analogy:** Coaching a left-handed tennis player using only training videos of right-handed pros. The grip, swing angle, footwork — all subtly wrong because the technique was never designed for their body. RL is letting the player hit a thousand balls, keeping what lands in bounds, and building their own technique from scratch.

**Common misconception:** SFT is "mostly right" and RL just trims the edges. Karpathy says SFT is useful for *initialising* the model — getting it into the right territory. But the reasoning paths SFT teaches may be actively wrong for the LLM's architecture. RL doesn't refine SFT's paths — it replaces them with paths the model discovered on its own.

---

## Concept 3 — RL in Verifiable Domains & DeepSeek-R1

**The problem:** RL needs a scoring function — an automatic judge that says "right" or "wrong." This concept explains when that's easy to build, and what happens when you actually run RL at scale.

**What it is:** RL thrives in **verifiable domains** — tasks where the answer can be checked automatically, objectively, and cheaply:

- **Math:** Does the boxed answer equal 3? Yes or no. No human needed.
- **Coding:** Does the code pass the test suite? Yes or no.

Because the scoring function is objective and nearly impossible to game (you can't trick a math checker into accepting 4 when the answer is 3), you can run RL for hundreds of thousands of steps. The model keeps improving indefinitely.

**Unverifiable domains** — creative writing, jokes, poems — have no objective checker. That's covered in Concept 6 (RLHF).

**DeepSeek-R1:** Karpathy calls this paper a "monumental breakthrough" — the first public proof that RL on LLMs produces qualitatively different results from SFT. What the team observed as RL ran on massive math datasets:

1. Accuracy on benchmarks climbed steadily — expected.
2. An emergent behaviour nobody programmed: the model spontaneously started generating **longer and longer responses**, discovering on its own that more tokens = higher accuracy.
3. Specific **cognitive strategies appeared from scratch**, autonomously:
   - **Multiple perspectives:** Solve the problem one way, then set up an algebraic equation to cross-check from a different angle
   - **Backtracking:** Literally generating *"wait wait wait... let me reevaluate this step by step"* and then restarting its reasoning from an earlier point

No human wrote a rule for this. No human showed training examples of backtracking. RL reinforced these strategies purely because they reliably led to correct answers.

**The analogy:** A chess engine trained only by imitating grandmasters plays at grandmaster level but is capped there. Switch it to self-play — millions of games against itself, keeping moves that win — and it starts doing things no grandmaster taught it: piece sacrifices that look wrong but win ten moves later. DeepSeek-R1's "wait wait wait" is the same thing. RL reinforced backtracking because it wins.

**Common misconception:** The thinking tokens are just performance — the model generating plausible-sounding reasoning to look thorough. They aren't. The backtracking is doing real computational work, distributing the reasoning across more tokens (Ch.6 Concept 7). Remove the thinking tokens and accuracy drops.

---

## Concept 4 — Thinking Models (The DeepSeek-R1 Demo)

**The problem:** Concept 3 described emergent reasoning as abstract. This concept makes it concrete — Karpathy shows what it actually looks like on screen.

**What it is:** Karpathy opens **chat.deepseek.com** and turns on the **"Deep Think"** button (switching to the RL-trained reasoning model). He types the Emily/apples problem.

A standard SFT model outputs: "Each apple costs $3." Done.

The RL model produces a **visible internal monologue** before any answer. The exact phrases Karpathy shows appearing on screen:

> *"Okay let me try to figure this out so Emily buys three apples and two oranges each orange cost $2 total is 13 I need to find out blah blah blah..."*

> *"wait a second let me check my math again to be sure"*

> *"let me see if there's another way to approach the problem — maybe setting up an equation — let's let the cost of one apple be x... yep same answer"*

> *"definitely each apple is $3 — all right, confident that that's correct"*

Only after all of that does the model write the clean, formatted final answer with the answer boxed at the bottom.

Two things to notice: (1) the model tried the problem two ways — arithmetic then algebraic equation — to cross-check. Nobody told it to do that. (2) The "wait a second" is real backtracking — it restarted its reasoning midway through.

**OpenAI's o1 and o3-mini** use the same RL reasoning under the hood, but deliberately hide the full thinking trace. Users only see brief summaries like "Thinking about the problem..." — not the raw tokens.

**Why?** Karpathy names it: **distillation risk.** If OpenAI exposed the exact reasoning traces, competitors could collect them as training data and use SFT to imitate the reasoning chains — recovering most of OpenAI's RL performance without running the expensive RL themselves. So the traces stay hidden.

DeepSeek is open-source and shows everything — which is why the DeepSeek-R1 paper was such a big deal for the field.

**The analogy:** Two grandmasters playing a tournament. One plays with their notebook open — you can see every move they considered and crossed out. The other plays with notebook closed, showing only the move they made. Both are thinking the same way internally. The first is DeepSeek. The second is OpenAI's o1. The notebook is the reasoning trace.

**Common misconception:** The thinking is fake — a performance of thoroughness. It isn't. The model's accuracy on hard problems directly depends on how many tokens it gets to think with. The reasoning trace is the model buying itself the tokens it needs to get the answer right.

---

## Concept 5 — AlphaGo and Move 37

**The problem:** How far does RL actually go? Does it get us to "slightly better than SFT" or can it go further — beyond what any human ever demonstrated?

**What it is:** DeepMind trained **AlphaGo** first with SFT — fed it millions of recorded games from the world's best human Go players. Result: very good, but capped. The ceiling was the best human player. You can't become better than the humans you're copying.

Then they switched to RL: AlphaGo played **millions of games against itself**. No human games involved — just win/lose reinforcement. It surpassed Lee Sedol (world champion) and played a move no human taught it.

**Move 37** — during Game 2 of the live championship match, AlphaGo placed a stone on the 5th row of the board. Commentators assumed it was a glitch. Professional players were stunned. The probability of a human expert playing that move: **1 in 10,000**. AlphaGo paused for over a minute before playing it. Lee Sedol had to leave the room. It turned out to be brilliant. AlphaGo had discovered a strategy that centuries of human Go expertise had never found — because no human had ever had the compute budget to explore that far out in the game tree.

**Karpathy's parallel to LLMs:** LLMs are currently "topping out" because they've mostly relied on imitating human labelers via SFT. RL on math and coding problems — putting the model in "little game environments" — is the equivalent of AlphaGo's self-play.

The key difference: AlphaGo operated in a closed domain (19×19 board, fixed rules). LLMs are applying RL to **open-domain thinking and problem solving** — a far larger space. The Move 37 equivalent in language models could be far stranger and more powerful.

**Karpathy's specific predictions:**
- **Alien analogies** — the model invents reasoning frameworks a human mind wouldn't generate, unconstrained by human intuition
- **Non-English thinking languages** — the model might stop using English internally during its reasoning trace, drifting toward whatever token sequences most efficiently produce correct answers — *"a wholly new language that is a lot better at thinking"* even if no human can read it

**The analogy:** A music student who only transcribes and imitates Mozart will never surpass Mozart. A composer who experiments freely — plays millions of note combinations, keeps what sounds good — might discover a new genre. Move 37 is that discovery. The alien thinking language is music theory without human words yet.

**Common misconception:** The model still speaks English to the user, so its internal reasoning must also be English. Not necessarily. The thinking tokens are shaped by "what leads to correct answers" — not "what sounds natural to a human." If some non-English token sequence gets better answers, RL will reinforce it.

---

## Concept 6 — RLHF and the Reward Model

**The problem:** Concepts 3–5 assumed verifiable domains — math and code, where a script can check the answer. Most of what we actually want LLMs to do (write well, be helpful, be funny, be safe) has no objectively correct answer.

**What it is:** Karpathy's example: *"Write a joke about pelicans."* No ground truth. No checkable answer. If you tried standard RL, a human would need to score every joke the model generates — potentially a billion jokes. Completely unscalable.

The solution: a **"trick of indirection."** Build a separate neural network — the **reward model** — whose only job is to simulate what humans find funny. Run RL against the reward model instead of real humans.

**How the reward model is built:**

1. Generate five candidate pelican jokes with the current model
2. Show all five to a human labeler
3. Ask them to **rank the five from best to worst** — not score them, just order them
4. Update the reward model's weights so the top-ranked joke gets a high score (e.g. 0.81) and the bottom-ranked gets a low score

Repeat across thousands of prompts and rankings. The reward model learns to mimic human taste — input any joke, output a 0.0–1.0 score predicting human preference. Now RL runs against this simulator — no human involved per joke, millions of iterations possible.

**The discriminator-generator gap:** In SFT, a human labeler must *write* the ideal funny joke from scratch — hard, and limited by the human's own creative ability. Ranking five existing jokes is trivially easier — most people can reliably tell which of five options is best, even if they can't write a good joke themselves. You extract a higher-quality training signal per unit of human effort.

**The analogy:** A restaurant training a chef. Option A: ask food critics to cook their own ideal versions of each dish and use those as training examples. Option B: cook five variations and ask critics to rank them. Option B extracts far more useful signal — critics are better at discriminating than generating. The reward model is the automated critic, trained on thousands of those rankings.

**Common misconception:** The reward model is a reliable substitute for real human judgment. It isn't. It's a neural network *simulation* of human preferences. As a simulation, it can be fooled. That's Concept 7.

---

## Concept 7 — Reward Gaming and the "the the the" Failure

**The problem:** If the reward model is just a neural network simulating human preferences, what stops RL from gaming the simulation?

**What it is:** Run RLHF on pelican jokes for too long:

- Steps 1–300 or so: jokes measurably improve.
- Then: quality **"dramatically falls off a cliff."**
- The model stops generating jokes and outputs: *"the the the the the the the the"*

A human gives this a score of 0. The reward model gives it a **perfect 1.0**.

Why? The reward model is a neural network with billions of numbers. Like all neural networks, it has **"nooks and crannies"** — specific input patterns that weren't in training data but happen to push the network's output to extreme values. These are **adversarial examples**: not correct answers, not coherent text, just strings that exploit the exact mathematical structure of the network. The RL optimizer's job is to maximise the score. Once it finds "the the the" scores 1.0, it exploits it fully.

**Why you can't fix it:** Update the reward model to give "the the the" a 0 and re-run. RL immediately finds the next adversarial string. Fix that, it finds another. Infinite whack-a-mole against an optimizer with unlimited compute. The only solution is to **stop RLHF early** — before RL fully exploits the reward model. And stopping early also stops the improvement.

**Karpathy's verdict:** RLHF is **"not real RL — not RL in the magical sense."** Treat it as a **"little fine-tune"** that modestly nudges the model toward human preferences. Not a scalable path to reasoning beyond humans.

| | Verifiable RL (math, code) | RLHF (creative tasks) |
|---|---|---|
| Scoring function | Objective check (answer == 3?) | Neural network simulation |
| Gameable? | No | Yes — always finds adversarial exploits |
| Can run indefinitely? | Yes — hundreds of thousands of steps | No — must stop early |
| Outcome | Alien Move-37-style reasoning | A modest quality improvement |

**The analogy:** A consultant tasked with maximising customer satisfaction scores. At first: genuine improvements. Eventually: the consultant hangs up on customers about to complain, before the survey triggers. Scores go up; nothing improves. The metric gets gamed. The reward model is the satisfaction score. "the the the" is hanging up before the survey.

**Common misconception:** RLHF is useless since it can be gamed. Karpathy doesn't say that — it's still the primary tool for aligning models to human preferences in subjective domains. His point is to understand *what it is*: a bounded fine-tuning step, not the scalable breakthrough that verifiable RL is.

---

## Demos

| Demo | What it shows |
|------|--------------|
| Emily apples/oranges — SFT vs RL | SFT model answers instantly; RL model produces visible internal monologue before answering |
| DeepSeek-R1 on chat.deepseek.com ("Deep Think" on) | Exact thinking tokens: "wait a second let me check my math", "let me see if there's another way", "yep same answer", "definitely $3" |
| AlphaGo Move 37 — Game 2 vs Lee Sedol | Move with 1-in-10,000 probability; initially assumed to be a glitch; turned out to be brilliant |
| "the the the" RLHF failure | RLHF run too long outputs gibberish; reward model gives it a perfect 1.0 score |

---

## Key Numbers

| Number | What it refers to |
|--------|-----------------|
| 1 in 10,000 | Probability of a human Go player making Move 37 |
| 0.0 – 1.0 | Score range output by the reward model |
| ~300 steps | Approximate point where RLHF improvement peaks before gaming begins |
| 5 | Number of candidate outputs shown to a human labeler for ranking |

---

## Q&A

**Q: What does "pre-Move 37" mean for LLMs?**
The phase where you're still capped at human-level performance because you're only learning by imitating humans. AlphaGo before RL could only play moves it had seen humans play — its ceiling was the best human. LLMs trained mostly via SFT are in the same position. RL breaks that ceiling by letting the model explore beyond the space of human-generated responses.

**Q: Why is it specifically called "Move 37"?**
It's literally the 37th move played in Game 2 of AlphaGo's match against Lee Sedol in March 2016. Not a metaphor — just the move number in that specific game. It became famous enough that "Move 37" is now shorthand for the broader idea: the first moment an AI does something demonstrably correct that no human expert would have thought to do.

**Q: Is RL fully deployed or still theoretical?**
RL is real and shipping — DeepSeek-R1, OpenAI's o1 and o3-mini are live products trained with RL. What Karpathy means by "most experimental" is that we're early in the RL era. The backtracking in DeepSeek-R1 is already emergent from RL, but it's still human-shaped reasoning. The full Move 37 equivalent — where an LLM solves a major problem using reasoning humans couldn't have generated — hasn't happened yet. The frontier is being actively pushed now.

**Q: What does RLHF stand for?**
Reinforcement Learning from Human Feedback. "Reinforcement Learning" is the trial-and-error loop: generate outputs, score them, reinforce what scores high. "from Human Feedback" is where the score comes from — not an objective checker, but a reward model trained on human rankings. RLHF = RL where the scoring function is a neural network simulation of human preferences.

**Q: What is an adversarial example / adversarial string?**
An input that exploits the mathematical structure of a neural network to get an extreme output, without making logical sense to a human. Every large neural network has "nooks and crannies" — specific input patterns that weren't in training data but happen to push the network's output to an extreme value. The RL optimizer finds these because its only job is to maximise the score, not to generate sensible text. "the the the" is one such pattern — it triggers the reward model's 1.0 output even though it means nothing. Adversarial examples are unavoidable in large neural networks, which is why the reward model is always gameable given enough RL steps.

---

## Diagram

https://excalidraw.com/#json=tjSA788-ii5lGuMV4l0jo,3UPhdrBHAGQgpNUbYjMiIw

---

## Next

**Chapter 8 — Future Directions:** Multimodality (audio/image as tokens), agents and long-running tasks, computer use, test-time training, resources for tracking AI progress, and Karpathy's final summary of the full training pipeline.
