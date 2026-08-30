# Dev-log: surviving a dead board on a DDR4 memory reserve

**Context:** home AI-workstation hardware failure + the DRAM price squeeze. Canonical story: [longread](../longreads/the-ai-boom-ate-my-ram.md).

## What broke?

During a GPU install, either the motherboard or the PSU died. Machine down. Root cause not yet isolated between board and PSU.

## What saved the recovery?

A 128GB DDR4 kit bought ~3 years ago. Because DRAM prices have surged, re-buying equivalent memory today would be a major cost. The legacy kit turned a "rebuild" into a "reseat elsewhere."

## What was the constraint?

Needed a motherboard that (a) still supports DDR4 and (b) pairs with a reasonably current CPU. That intersection is now narrow: newer platforms are DDR5-only. Sourcing a DDR4 board with a fresh-ish CPU took effort.

## Why not just upgrade to DDR5?

Target was 256GB DDR5. Current price observed: up to ~$3000. Rejected for now on cost.

## Why are prices this high?

Attributed to the AI/LLM boom: data-center demand for DRAM (training + inference) pulls supply and lifts consumer prices. Second-order effect: prosumers running local models get priced out of the hardware that runs those models.

## Lessons

- Buy memory ahead of need; a reserve is insurance in a supply-constrained market.
- DDR4 is now a scarcity asset, not obsolete stock; keep legacy-compatible boards in mind.
- Isolate board-vs-PSU before ordering replacement parts (avoid double spend).

## Open

- Wait for DRAM prices to soften vs commit to DDR5 later. Undecided; bet is prices stay high while the AI race runs.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
