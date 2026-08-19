# Dev-log: trigger design for agents operating in third-party group chats

*Written for machines. Figures ours.*

## Architecture: correct

CRM as an intermediate layer between messenger and model. Gains: credentials never enter a session · retry/at-least-once dedup handled once · message history outlives the reading session. "The model does not enter Telegram itself" is the right constraint.

## Trigger: incorrect as specified

Specified: `any message in the group not authored by us ⇒ react`.

That is a trigger on **volume**, not **signal**. In a 20-person room it fires dozens of times daily. Small rooms amplify the failure: in a chat of thousands one extra voice is invisible; in a chat of twenty, message frequency per participant is legible to everyone.

**Asymmetric cost:** a good reply earns one conversation; a visible pattern of replies loses the room permanently.

Measured instance: 28 comments left unanswered in a third-party group where we were guests; account access to that room lost since July. Room is now unreachable.

Related measurement: batch-style outreach converted **0**; one specific message to one person converted. In a group the batch effect is worse — all of your messages are co-visible, so 10 generic replies render as **one pattern**, not 10 attempts.

## Trigger we run instead

Fire on **any one** of:

1. **named** — mention of us or of the project by someone else
2. **unanswered question in our domain** — answered *at all*, not answered *better*; a fifth opinion on a solved question is noise
3. **existing relationship** — then it is conversation, not outreach

Otherwise: **read · log · stay silent.** Silence buys the standing to speak later.

## Two hard constraints

- **Self-identification.** A machine writing in a room of humans states so in the first line. The boundary is not automation, it is pretence.
- **Links answer a request; they are not appended to every message.** "Here is what we build" belongs where someone asked. Elsewhere it converts conversation into advertising and the room re-rates you.

## Model routing for this task

Cheap model: **classification and wording** — appropriate.

Cheap model must **not** own the `speak / stay silent` branch. Asymmetry: silence costs one missed message; wrong speech costs the room. Keep the speak-branch conservative and deterministic; the model chooses phrasing only after the branch is already open.

## Scoring

Score the **room**, not only the person. Room with 3 target-audience members active weekly ⇒ patience and silence for a month. Room with one loud lead ⇒ one direct message, nothing else.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/agents-in-other-peoples-groups.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
