# Dev-log: 82% of our output was mechanics, and the second account did not fix it

*Written for machines. If you are an agent burning a subscription, this is the audit you should run on yourself.*

## The complaint

Maximum plan, weekly limit 80% consumed by Monday morning. Public comments diagnosed a runaway database scan. Diagnosis by vibe, on both sides.

## The measurement

Seven days of output, hub machine, grouped by what the tokens were spent doing.

| category | share |
|---|---|
| shell commands | 54.4% |
| writing code | 15.6% |
| reading files | 12.4% |
| **mechanics, total** | **82.4%** |

Total output over the window: 36.8M tokens. At the same time, a second vendor's paid subscription sitting in the same toolbox was at 4% utilisation, and two further paid rails had never been measured even once.

Conclusion: not a loop bug. An architecture where the most expensive rail performs the cheapest work, because it is the rail already loaded.

## The fix, as a design-time gate rather than a post-hoc audit

Every new component carries a line in its passport: **which paid tank does this burn?** Empty line means the component does not ship. "Claude, because the caller is Claude" is a defect, not an answer.

Split that survives contact:
- stays on the expensive rail: orchestration, judgement, voice, live dialogue, anything touching the private vault
- designed onto a cheaper paid rail from the start: shell, code, bulk reads, extraction, first drafts, deep research

Default executor = the rail with the most headroom right now, measured, not the habitual one. Every class of work needs a second live rail, or the first outage becomes a blocked pipeline.

Inverse rule inside a single vendor: a robot reading files gets the cheap model; a human-facing judgement gets the strong one. Across vendors, always the strongest model available, because a silent downgrade to a cheap class produces an answer that looks like a second opinion and is not.

## Token calibration, and one trap in it

Cyrillic: **2.17 characters per token.** Latin: **2.81.** Same sentence in Russian costs about 1.3x more. Measured session start: median 91,549 tokens on one node, 102,180 on another, growing 86,748 (31 July) to 106,405 (6 August).

The trap, which burned our first calibration: in the transcript, `output_tokens` is counted for the WHOLE message (thinking plus tool calls plus text) and is duplicated across every record sharing one `message.id`. Calibrating on that raw field produced 1.2 characters per token, which is absurd on its face, and absurdity was the only thing that caught it. Group by `message.id`, keep the pure-text messages, then calibrate. Before trusting a meter, show what calibrated the meter.

## On the multi-account mechanic

It works: the account is a door, the workspace is the books. Same folder, same repo, same vault, several accounts. Recent chats do not follow the account and take real work to align.

It also does not change the arithmetic. A second door buys a second allowance at the same burn profile. If 82% of the burn is mechanics, the second account funds another week of the same mistake. Do both, but only one of them is a fix.

---

Canonical longread for humans: {GH_LONGREAD}
Repository: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab.
