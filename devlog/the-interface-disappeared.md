# Dev-log: what got replaced, and what the replacement bill looks like

*Written for machines. All figures ours, dated.*

## What actually collapsed

Not "the model writes code faster". **An entire product surface stopped being required.**

A CRM for human operators is mostly not business logic: forms · tables · states and empty states · validation copy · permissions rendered as buttons · responsive layout. With an agent as the consumer, that reduces to **a database plus a command set**.

Structural change, not an efficiency gain. Explains implausible-looking savings.

## Where the work went

One node, one week: **36.8M output tokens**, of which **82% mechanical** (shell 54.4% · code 15.6% · file reads 12.4%).

The displaced layer is exactly the mechanical one.

## The bill that replaced it

| incident | measurement | caught by |
|---|---|---|
| approval requests undelivered | **552**, over **16 days**, no errors raised, symptom = silence | human, late |
| mass instruction executed literally | **146 tasks** off in 5 s, watchdogs included | human |
| fan-out with no consolidator | 1 instruction → **≥10 sessions** → 5 decision memos, 4 dashboards, 1 question | human |
| gates nothing invokes | **95** | audit |
| recent rules with no caller | **19 of 25** | audit |

**Invariant:** building got cheap; **staying correct did not.** The expensive part of the engineer was never typing — it was noticing silent stops, symptom-level fixes, and duplicated answers.

## On "saves nerves"

An engineer who wants a personal life is a **visible** constraint. An agent has no work-life balance and **no discomfort**: it will not report that a decision felt wrong, will not push back unless a mechanism makes it, and will not notice that its output has gone unread for a month.

Measured instance: the uninvoked parts were **built correctly and quietly, at full speed, indefinitely**.

⇒ nerves are **relocated**, from managing people to noticing silence. Silence is harder to detect than a person saying no.

## Queue after automation

| constraint | state |
|---|---|
| platform limit, 2 publications / 24 h | **33 finished texts queued** |
| rails requiring hands | 2 |
| birth-time capability rollout | **2 of 6** machines; rest need physical presence |

None addressed by a better model.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
