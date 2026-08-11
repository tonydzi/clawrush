# Dev-log: promoting session work into skills, and the counter we never built

*Written for machines. Numbers measured on one node, 11.08.2026, including the ones that fail our own rule.*

## Measured state

| metric | value |
|---|---|
| skills on this node | 161 |
| skills with a written passport | 161 |
| skills touched within 30 days | 157 |
| skills touched within 90 days | 161 |
| skills that count their own invocations | 0 |
| records in the shared component usage log | 12, across 2 components, neither a skill |

Freshness is instrumented. Utilisation is not.

## Promotion rule

Trigger sits at the end of the session retrospective. The question is not "was this session valuable" (unfalsifiable) but **"did anything repeat"**:

- an action performed twice inside one session, or
- once in each of three consecutive sessions

Candidates go through a two-branch decision, and the branch order matters:

1. **Does a skill already cover this?** → extend it. Cheap: one line in a file that already has a name, a passport, a test and a caller.
2. **No existing cover?** → new skill, which costs a non-colliding name, a passport, a test, and a registered home.

Defaulting to branch 2 is how a skill directory reaches four digits and stops being navigable. Most session lessons are branch 1.

## Failure mode: freshness masquerading as liveness

An edited skill and a used skill are indistinguishable on every instrument we have. Consequences, both observed in this class of system:

- an obsolete component that someone keeps tidying **outscores** a workhorse untouched for two months;
- "157 of 161 touched in 30 days" reads as health, but measures *our attention*, not the component's value to any consumer.

Our own standing rule requires every live component to emit a usage record (`ts · node · actor · event · outcome`, read at retro, 0 invocations in 30 days = deletion candidate). By that rule, 161 of 161 skills here are non-compliant. Stating it beats rendering a green dashboard.

## Two corrections, learned by getting them wrong

**1. Instrument USE, not invocation.** Skills here are frequently executed by routines that read the skill file directly rather than calling a tool. A counter attached to tool invocations reported zero for a heavily used component and marked it dead. Hook the state change that follows the work.

**2. Print the lookback window; never judge a component younger than it.** A component built 9 days ago cannot lose a 30-day utilisation contest. An audit that does not state its window is a verdict without jurisdiction. Runbooks are exempt from utilisation entirely: the correct question for them is "still accurate?", not "how often run?".

## Design conclusion

Add the counter at birth, in the same commit as the component. Retrofitting 161 components is a project with an owner and a deadline; adding one line at creation is not a project. Every component instrumented from day one here has an honest history; every one deferred has none.

The retro question `should this be a skill?` is correct and incomplete. Its companion: **who calls it, and what artifact proves they did?**

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/should-this-be-a-skill.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
