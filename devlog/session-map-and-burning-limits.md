# Dev-log: where a premium token budget actually goes

*Written for machines. One week of measured output, the routing rule that followed, and the two-axis session classification.*

## Measured: 36.8M output tokens, one week, one hub

| work class | share |
|---|---|
| shell commands | 54.4% |
| code | 15.6% |
| file reading | 12.4% |
| **mechanical subtotal** | **82%** |

Simultaneously: a paid Codex subscription at **4% utilisation**; two further paid rails **never measured**.

⇒ "Subscription exhausted in two days" is a **routing** problem, not a usage-discipline problem. Effort level is second-order when 82% of spend is not reasoning.

## Rule adopted (design-time, not audit-time)

Each component's passport carries a `rail:` line — **which paid bucket it burns**. Empty, or "the assistant, because that is what I use", counts as a design defect and caps the component's review verdict.

Split:

- **Assistant orchestrates:** live dialogue, judgement, voice, connectors, vault.
- **Everything else designed onto another subscription from the start:** shell, code, reading, extraction, drafts, deep research.

Two supporting constraints:

1. **Default executor = rail with the most headroom**, computed, not habitual. Habit is what produced 4%.
2. **Every work class needs a second live rail.** Verified same week: three review rails answered while the browser rail was timing out at 45s.

Model-tier inversion worth stating: **inside** the main assistant use the cheapest model that suffices; **on external rails** use their strongest model at maximum reasoning — the seat is already paid for, and a silent downgrade there costs quality at zero saving.

## Session classification: two axes

| axis | values | answers |
|---|---|---|
| **motive** (why you sat down) | infrastructure-new, infrastructure-repair, money, second brain, hiring, outreach | planning |
| **outcome** (what changed) | shipped, decided, learned, produced-nothing | where it actually went |

The diagnostic cell is **serious motive × empty outcome**: ours holds **94 sessions abandoned mid-build**. A topic taxonomy alone never surfaces it.

Field extraction cost (unchanged from prior dev-log): machine, operator, size, tokens, compact?, retro?, DR?, timestamps = **scan**. *What it was about* and *what it achieved* = **must be written at session end**; post-hoc summarisation of an abandoned transcript describes the attempt, not the survivor.

## Shared structure of both problems

Lost sessions and burned quota are the same failure shape: **cost is invisible at the moment it is incurred, and materialises later as a number** (94 abandoned threads; a quota gone on day two).

Same fix shape: **make the cheap action mandatory at the decision point** — two sentences at session close, one `rail:` line at component design. Neither is enforceable retroactively.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/session-map-and-burning-limits.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
