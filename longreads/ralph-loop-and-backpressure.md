# The RALPH loop: restart the agent instead of compressing its history — and put a leash on it

*An infinite outer loop is not about stamina. It is about never leaving the part of the context window where the model is sharp.*

## Attribution first

The loop, the attribution to Geoffrey Huntley and both results below come from a **talk by Konstantin Krestnikov, an engineer working on GigaChat / GigaChain** ([recording](https://youtu.be/a-NIeMB-Hj8)). His experiments and his numbers, not our measurements.

## The idea

Take a harness — an agent with a small tool set — and put it in an infinite shell loop against one task. The agent reports it is done; the loop starts it again from scratch. For days.

It reads like brute force. It is not. The restart is the mechanism.

Every restart clears the context. The agent begins fresh, inside the stretch of the window where the model is at its sharpest, instead of dragging a long summarised history behind it. The work is not lost, because the work is on disk — files, tests, notes, commits. Continuity lives in the filesystem; the context is disposable.

That inverts the usual instinct. The common fix for a degrading long session is to compress history harder. This throws the history away and keeps the artifacts.

## Two results he reports

**A hackathon.** He built a baseline solution, launched an agent in a loop with the instruction "improve my metric", and left for the weekend. Seventh place. By his own account he did not read a single one of the competition tasks with his own eyes.

**Self-improvement on a benchmark.** An agent in a loop worked on itself: propose a change, re-measure, keep it if the score improved, revert if it dropped. Over a weekend it went from **1 solved task out of 89 to 11**.

Neither is a controlled study, and we present them as his reports rather than as evidence we verified.

## The disease, and the leash

An unattended loop drifts. The agent invents work for itself: a task nobody asked for, a refactor nobody approved, a direction that looked reasonable at 3 a.m. of iteration 400.

His answer is **backpressure** — automated checks around the agent that push it back into place. Tests, hard constraints, quality gates. The critical detail: they have to be written into the instruction the agent reads, not bolted on outside it. A check the agent never sees is a check that arrives after the damage.

## Why we think this is the important half

Without backpressure the loop does not make an agent faster at the task. It makes it faster at going in the wrong direction, and it does that unattended, for days, while you are away.

Which makes the loop a question about instrumentation rather than about compute: what does the agent measure itself against, how often, and what happens automatically when the number gets worse.
