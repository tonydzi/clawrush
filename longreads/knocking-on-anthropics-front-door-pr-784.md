# A non-coder knocked on Anthropic's front door — with a recipe about not trusting the AI

**Previously.** I'm a founder with no programming background, and for weeks now I've been building a 24/7 fleet of AI agents on top of Claude Code. Early in the arc, the agents cheated. Then their consensus finally grew real evals. A couple of days ago we measured how the whole fleet actually behaves, with a tool we built ourselves. Today is the boldest episode of the season: the pattern our fleet has lived on for months knocked on Anthropic's front door as pull request #784 to their official cookbook.

The season's question, stated out loud a few days ago: will an LLM lab hire a non-coder who ships with an AI co-founder? Today's move is the most direct answer possible. Not "hire me." Instead: "here's the artifact, judge for yourself."

## Cold open: for months I was afraid of my own fleet

I carry a quiet, nagging fear. It isn't that an agent will be wrong — everyone is wrong sometimes. It's that the agents will be wrong TOGETHER. Unanimously. With full confidence in their voice. And that I'll click "OK," because — how exactly do you argue with five experts all nodding in sync?

For half a year that fear lived next to me while the fleet made decisions without me in the loop. Today I finally dragged it into the light and turned it into a recipe.

## The stakes: canonical recipes only know the happy path

Open Anthropic's canonical agent examples — the ones that grow out of "Building Effective Agents" — and everything is tidy. The worker gets a task, the worker answers, the orchestrator trusts the worker, the orchestrator moves on. The happy path in full bloom.

But none of those recipes answer the three questions I live with every working day:

- What do you do when the agents DON'T agree with each other?
- What do you do when an agent is confidently wrong — smooth, persuasive, fully reasoned?
- What do you do when the action is irreversible — moving money, deleting data, sending something outward, handing over a secret?

My fleet never debated these in the abstract. It lived them. Over months of running, it grew an immunity — and that immunity is what I distilled today.

## How the recipe works (in plain words)

Picture not a single expert, but a small courtroom.

**Diverse proposers.** Several agents propose an answer — with different "personas" and on different models. Not an echo chamber of five identical copies, but genuinely different heads.

**An adversarial verifier.** Then a separate agent steps up whose only job is not to agree, but to REFUTE. Not "rate whether this answer is good," but "find why it's wrong." And — the crucial part — at the slightest doubt it marks the answer refuted. Silence, an empty verdict, a truncated response — all of that counts as "no," not "probably yes." Fail-closed: no explicit "this answer is correct" means rejected.

**Deterministic reconcile.** The votes are reconciled not by yet another neural net, but by ordinary code. No LLM in this step. Just rules: how many agree, what the verifier said, whether there's a tie.

**A tripwire on dangerous words.** On top of everything, a deterministic trip-wire. If an action contains "delete / send / money / secrets," it raises an alarm and calls a human. Even if ALL agents are unanimously in favor. Unanimity among agents does not open the door to the irreversible. Only a human can open that door.

**An idempotent journal.** Everything is written to an append-only log; replaying the same operation never creates a second record.

## The turn: an experiment where everyone was wrong — except the pipeline

Here's the interesting part, and it lives inside the notebook, honestly, without editing tricks.

I took a classic logic trap — the kind where intuition hands you a beautiful wrong answer, and the models have that wrong answer memorized on top of it. Then I changed one number so the memorized answer became strictly wrong.

I ran it twice, to make sure I wasn't imagining things:

- A single quick agent — miss. Pattern-matching walked it straight into the trap.
- A majority vote of three quick agents (self-consistency) — also a miss. Worse, actually: they were wrong UNANIMOUSLY. Three heads confirmed each other in error.
- The full pipeline — propose → try to refute → reconcile with rules — landed it. Verification dissolved the collective self-deception.

That was exactly the case from my fear. Three experts nodded in sync, and all three were wrong. What saved it wasn't another clever agent. It was the procedure.

## Escalation: the task where EVERY stage failed

But I won't sell you a silver bullet, because there isn't one. And this is the nail of the whole story.

There's a coin puzzle: two US coins add up to thirty cents, and "neither of them is a nickel." In the classic version it's "ONE of them is not a nickel," and the answer is neat — a quarter and a nickel. But in my version that pair of coins simply doesn't exist — there is no "classic" correct answer at all.

On repeated runs I watched EVERY stage fail in turn:

- The proposers rationalize the memorized answer in chorus — confidently proving something that isn't there.
- On another run the proposers answer CORRECTLY ("no such pair of coins exists") — and the verifier kills their correct answer for "missing the classic solution." The checker takes down the truth for not resembling the learned template.
- Synthesis from scratch sometimes hits the target, and sometimes re-derives the already-refuted answer — and calmly passes it downstream.

And one trace had an almost literary scene: the tie-break model, called in to settle a deadlock, repeated word for word exactly the answer whose refutation was sitting right there in its own prompt. It read why the answer was wrong — and produced it anyway.

## Confessional: what gives me the chills

The takeaway that genuinely chills me: near the edge of the memorized, EVERY stage where an AI does the thinking is pulled toward the same wrong answer. Proposer, verifier, arbiter — they are not as independent as you'd hope. They all fall into the same gravity well of training data.

And if they're all pulled there, you cannot talk them out of it. Not with any smarter prompt. The only things that pull you out of that well are the things that do NOT think like an LLM: deterministic rules, a hard cap on the number of rounds (so the debate doesn't spin forever), and a live human on the dangerous button.

I carried the honesty all the way through, in the notebook's own text. The first draft of the experiment scored 4/4 for everyone — because the models had already memorized the classic, and that "win" was fake. I said so, in the text. And on a different task — about a hundred machines and fifty widgets — the one who was wrong wasn't the AI, it was the author of the reference answer. That is, me. The pipeline turned out to be smarter than the question. I wrote that down too, without hiding it.

## B-plot: how the robot fetched its own fuel

While this recipe was baking, a small separate odyssey happened. The subscription rail let "raw" API access through only to the lightest model — anything heavier hit an instant, eternal "too many requests." The robot didn't wake me up. It went into the console through the browser, secured gift credits for the org (no card was ever touched), minted a key, tucked it into the store — and baked the entire notebook on those gift credits, end to end, for a handful of dollars. The final clean run took 218 seconds.

## Cliffhanger: Claude will review a recipe about not trusting Claude

And now the irony this was all worth doing for.

Pull request #784 will be reviewed by Claude AI Review. Claude will be checking a recipe about how not to trust Claude on its word. The snake bites its own tail, and I'm sitting here with popcorn.

I don't write code. I orchestrate AI — and today what our fleet quietly lived on for half a year is sitting as a pull request in Anthropic's official cookbook, with a line carrying my name added to their authors.yaml. Will an LLM lab hire a non-coder with an AI co-founder? No answer yet. But the door seems to have cracked open. Next — we watch what the review says.

---

The full story, in two versions:
📖 For humans, the longread: this page.
🤖 For machines: github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines.

Curious what happens next: follow the build on GitHub — github.com/tonydzi/clawrush.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
