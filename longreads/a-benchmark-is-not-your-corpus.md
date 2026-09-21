# A benchmark is not your corpus

## Previously

I run a second brain. Not a metaphor, a folder: ~6,500 curated notes, 24,226 chunks,
half Russian, half English. Decisions, post-mortems, other people's lessons, my own
screw-ups. When I ask it something, it searches by meaning, not by words.

Meaning is handled by one small model, the embedder. Swap it and everything shifts:
what is found, what is lost, what surfaces first. It is like changing the way a person
recalls things.

For six months I did not touch it. Not out of caution. I simply had no way to tell
whether a change made things better or worse.

## The hit

In September I commissioned a deep research pass: which repositories and which models
to adopt now. Three independent LLMs, 144 sources, 30 repositories. One item where all
three agreed: swap the embedder to BGE-M3.

One report carried an argument I could not wave away. A Russian-language benchmark:
my current model at 61.41 nDCG@10, BGE-M3 at 70.50, and with their own reranker 76.44.
Nearly nine points. For a vault that is half Russian, that reads like a free lunch.

I almost pressed the button. One thing held me back: the day before, we had built a
ruler.

## The ruler that costs nothing

The idea is so cheap that I am still annoyed I did not have it earlier.

For years I placed links between notes by hand. This one about memory connects to that
one about graphs. This decision supersedes that one. Every such link is me, manually,
telling the system that two things belong together.

Which means the relevance labels were already there. Accumulated over years. For free.
They were just sitting there as decoration instead of as a measuring instrument.

A script turns my own notes into a 184-question exam, in four classes:

**Title questions** - the query is a note title, the right answer is that note. Tests
whether the system finds a thing I named by name.

**Body questions** - the query is the first paragraph with links stripped, the right
answer is still that note. Tests meaning rather than word overlap.

**Bridge questions** - the query is one note's opening, and the right answers are the
notes it links to. This is the honest, nasty class: it tests whether the system can walk
relations instead of matching text.

**Temporal questions** - the query is the title of a superseded decision, the right
answer is the one that replaced it. Tests whether the system serves stale truth.

Zero LLM calls. Zero paid tokens. The exam is assembled out of what is already on disk.

## The move

I ran BGE-M3 against that exam. Same index, same questions, one component swapped.

English gained 0.0804. Exactly what the benchmark promised.

Russian lost 0.0134.

A tiny number. But the sign is the opposite of the promise, and it drops precisely
where half my corpus lives. The temporal class dropped too, and that is the class I
introduced `superseded_by` fields for in the first place.

Rolled back.

Second candidate, Qwen3-Embedding-0.6B. No microscope needed there: the main class fell
from 0.867 to 0.800 Recall@12, English lost 0.029 nDCG, and reindexing took 2,863 seconds
instead of 31.

Five days later I re-ran both models on the same frozen question set. The absolute numbers
moved - the index had grown, the reranker differed - and the verdict did not move at all:
Qwen3 loses on titles, on body meaning and on English, and wins only on bridge questions,
within noise.

Both candidate indexes are still on disk. Deliberately. If a new argument shows up
tomorrow, switching is one line.

## This was the second time in a month

Before that came another deep research pass, on how human memory works and what of it
is worth copying.

One rail put a cognitive-psychology mechanism in first place. An elegant one: penalise
fan-out from over-connected hub nodes, plus decay by recency of access, exactly as human
memory does. The argument was strong: it fixes a genuine weakness of language models
rather than adding ritual on top.

I sent that disagreement out as its own research order, to four rails. Three findings
came back that I did not want to hear, and they closed the question.

**One.** The literal "fan penalty plus base-level decay" pair is not a standard in
shipped systems. Production stacks use intent routing, PageRank, neighbour caps and
edge-type filters instead.

**Two, the decisive one.** Time decay does not fix semantic drift. They are different
diseases. Access frequency does not make a fact true - it entrenches an old error. And a
note I have not touched in six months may be the most correct answer in the vault.

**Three, the honest one.** No rail produced independent evidence that hub nodes alone
explain my regression. The agreement was over shared literature, not four independent
replications.

Not adopted.

## The new normal

What we adopted instead is dull and has no pretty brain story attached.

First we looked at where the right answer actually dies. It turned out that 97% of
correct answers were already in the candidate pool, while only a quarter survived into
the final list. The system finds them and loses them at the last step: ranking. The
cross-encoder judges whether a neighbour's text looks like the query. But a bridge
relation is structural, not textual. It simply cannot see it.

So enlarging the candidate pool is pointless. Structure needs a vote in the ordering.

We took plain Personalized PageRank over the existing wikilinks and placed it as a
second judge beside the reranker, fusing ranks rather than scores. Bridge nDCG@12 went
0.176 -> 0.279. Bridge Recall@12 nearly doubled, 0.251 -> 0.451. No other class dropped.

The conclusion was convenient, so we stress-tested it: a parameter grid instead of a
single point. Positive everywhere, a plateau rather than a lucky needle. Parameters
chosen on odd-numbered questions held on even-numbered ones.

It runs on plain numpy, milliseconds per query, ~7.8k nodes and ~40k edges. No graph
database, no extra service. If the graph is empty or the computation fails, the band
returns the original order and logs one line. There is a test for that.

## What I take away

Three confident recommendations from frontier models. Real papers, real benchmarks, real
numbers. Two lost on my data. The third was replaced by a duller mechanism that won.

A 150-source report is knowledge about other people's systems. Not about mine.

Until you have your own ruler, every model swap is superstition. Expensive superstition,
with a well-cited justification.

And the part that stings: the ruler took one day to build, out of labels I had been
producing by hand for years without noticing. I waited six months for it.

The ruler itself is in this repo: [`artifacts/brain_gold_eval.py`](../artifacts/brain_gold_eval.py) ([what it is and how to reuse it](../artifacts/gold-set-from-your-wikilinks.md)). `--selftest` runs on a bare Python, no dependencies.

---

The full story, in two versions:
📖 For humans, the longread: https://github.com/tonydzi/clawrush/blob/main/longreads/a-benchmark-is-not-your-corpus.md
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines.

Curious what happens next: follow us https://t.me/ClawRus.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab/1-on-1. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab/1-on-1.

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley. github.com/tonydzi
