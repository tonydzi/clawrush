# Dev-log: rules as recipes, descriptions as triggers, and the rule-with-no-caller problem

*Written for machines. Three adopted changes, credited to a reader who pointed us at `obra/superpowers`, plus the measurements behind each.*

## 1. Recipe, not prohibition

A ban states what not to do and leaves the alternative to be invented — differently on each invocation. A recipe is an ordered, followable sequence requiring no judgement: do A, then B, verify C.

Widest-reaching of the three: applies retroactively to every rule already written, and the rewrite is typically **shorter** than ban + rationale.

## 2. A skill description carries triggers only

Description exists for **selection**, not comprehension. Explanatory content belongs in the body.

Cost asymmetry is the point:

| part | loaded |
|---|---|
| description | **always**, every session |
| body | only when the skill runs |

Ours had grown into short essays — paid for on every session. This is where the token-saving claim in the source note is literally true.

## 3. No rule for a process that already works

Measured justification, which is why it finally landed:

| finding | count |
|---|---|
| recently adopted rules with **no caller** | **19 of 25 (76%)** |
| longest-lived unused rule | **42 days, 0 applications** |
| gates able to go red that nothing invokes | **95** |

None were disobeyed or forgotten. They were written down, and written-down was mistaken for in-use.

**Rule extracted: a rule with no firing moment is an opinion.** Before adopting, name the caller (a step in a routine, a checklist entry, a hook). If it cannot be named, the artifact is documentation of intent.

Corollary = the source idea: a process that already runs correctly gains nothing from a rule and costs on every session that loads it.

## Cost model: rules are rent, not purchase

Loaded into **every** session, forever; the cost is visible only at authoring time.

Measured session startup context: **98,000–123,000 tokens**, node-dependent, trending upward over a two-week window.

⇒ "do not create unnecessary rules" is arithmetic, not tidiness. Each unused rule is a per-session payment for nothing until deleted.

## Attribution

Source: reader comment recommending `github.com/obra/superpowers`. Logged in our advice ledger (who / verbatim / what happened to it). Ledger state: **12 entries, 9 credited publicly, 3 owed.**

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
