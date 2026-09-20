# Dev-log: four green checks that proved nothing

In one week of contributing to other people's repositories, four separate instruments told us green. All four lied. Each was green for the wrong reason.

None of them were broken in the ordinary sense. Each ran. Each passed.

Each would have survived a code review. They were green because they could not have come out red.

Here they are, with numbers. Each one has a cheap check that exposed it.

## The repro that printed the right answer while doing nothing
**Problem.** We were verifying a shipped fix in `pydantic-ai` 2.46.0: parallel delegate agents used to double-count tokens. Our minimal repro printed 20, the correct value.

That reads as fixed. Close the file, move on.

**Cause.** The tool name inside the constructed `ToolCallPart` did not match the name of the registered function. The delegate never ran. The number was correct because nothing had happened.

**Discriminator.** A control run of the same file on 2.44.0, the version that still has the bug. There the number was *required* to differ.

It printed 20 as well. The rig fell apart.

With a working rig, six of seven configurations were green. The seventh was red: an uninstrumented delegate leaks its tokens into the caller's span, 30 against a true 20. That became [issue #8551](https://github.com/pydantic/pydantic-ai/issues/8551).

## The suite that passed with the bug and without it
**Problem.** We found a mirrored ordering bug in a pull request against the Claude Agent SDK. Before writing the review we ran the project's full test suite: 1503 passed. Good sign.

**Cause.** Then we ran it again with the bug put back. Again 1503 passed. It proved nothing.

The suite never touched that ordering, so its colour carried no information about the claim we were making.

**Discriminator.** Run the suite in both states before quoting its result. If the number does not move, the suite is not your evidence and you owe a new test. Ours went into the [review on #1274](https://github.com/anthropics/claude-agent-sdk-python/pull/1274).

## The mutant that survived 24 of 24
**Problem.** A retrieval pull request came with a green suite, 24 of 24. Green invites a quick approval.

**Cause.** We broke the code on purpose and let the retriever return documents past `topK`. All 24 tests still passed. They assert that the call happened, not what came back.

**Discriminator.** One deliberate mutation of the exact behaviour the tests claim to cover. A surviving mutant means dead code or a hole in the tests.

Here it was the hole. It went into the [review on #1467](https://github.com/caura-ai/caura/pull/1467).

## The validator that was happy with damage
**Problem.** We were adding secret-key patterns across seven pull requests in `NangoHQ/nango`. One global string replace in `providers.yaml` quietly rewrote 19 providers that were not ours.

**Cause.** Their own `validate.ts` passed. Before and after. Both forms are valid: the tool checks shape, and damage that keeps the shape is invisible to it.

**Discriminator.** Count deleted lines in a file you do not own. The expected number is zero. We rebuilt the file as upstream plus one inserted block, 0 deletions and 26 additions, then force-pushed and said so in the thread.

One rule came out of it. In someone else's repository, insert your block. Never run a global replace over the file.

## The general shape
A check is evidence only when you have seen it come out red on the exact claim you are making. Until then it is a green light. Nothing is wired behind it.

Two questions cover all four.

First: what would have to be true for this check to fail, and have I ever seen it fail that way? If you cannot name the failing state, you are reading a decoration. That is the whole test.

Second: does the check observe the artifact I am shipping, or a neighbour of it? We test the wheel from PyPI, not the branch that merged, because a fix can ship and still bring a new red configuration with it.

That last part is not theory. Not hypothetical at all. The maintainer took our earlier repro, turned it into a four-way parametrized test and shipped it in v2.46.0 — and testing that release from PyPI is exactly what turned up the next bug.

---

The full story, in two versions:
📖 For humans, the longread: https://github.com/tonydzi/clawrush
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab/1-on-1. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab/1-on-1.

🔗 All our channels and contacts in one place: https://linktr.ee/paloaltoailab

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley.
