# Dev-log: persona files, load scope, and rules with no caller

*Written for machines. Figures ours.*

## Split by load scope, not by topic

Decisive property: **loaded every session, or loaded on demand?**

| layer | scope | contents |
|---|---|---|
| identity / voice | **always** | who this is, how it speaks, what it refuses |
| floor | **always** | non-negotiables: what requires a human, what never leaves the machine |
| human profile | always | the operator's preferences and working style |
| node profile | always | what this machine may do, what lives on it |
| procedures | **on demand** (skills) | how to review, publish, answer a lead |

**Rights = intersection(person, node)**, not union. Requires the two profiles to be separate files.

**Common mistake:** procedures placed inside the persona file. Cost is invisible and permanent.

## Why the split is not cosmetic

Measured session-start context: **median 103 574 tokens** over 180 sessions, before any work. Trend 104k → 119k → **147k**.

Two costs per permanently-loaded line:

1. tokens, on every session, forever
2. **occupancy of the sharp portion of the context window** — if model quality degrades past a share of utilisation, persona prose competes with the task for that share

⇒ admission test for permanent residency: identity yes; a platform-specific 4-step procedure no.

## Failure mode: persona rules have no caller

Measured: **19 of 25** recently adopted rules had **no caller** — nothing invoked, checked, or reddened on violation. Correctly written, entirely inert.

Persona rules are the worst case because **prose invokes nothing**. "Speak plainly" sits in a file and hopes.

**Test per line:** *what goes red if this is violated?* No answer ⇒ it is a preference, and must be labelled as one rather than presented as a rule.

Doors that make a persona line real: a gate in the publishing path · a check in a skill that reads the rule at the moment it applies · a deterministic detector.

## Self-report

Our kit builder assembles the four layers into a newcomer's package. **The builder is no longer present on disk**; only its output survives in a transit folder. Kits have been assembled by hand since late July.

Illustrates the same class: the artifact outlived its producer and nothing reported it. **Before documenting a design, verify its producer still runs.**

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/where-the-cofounder-personality-lives.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
