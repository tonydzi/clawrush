# The smart zone is shorter than your context window, and your startup files eat it first

*Four years took the industry from a chat box to the harness. The most useful number in that story is not the size of the context window.*

## Attribution first

The history and the two practitioner estimates below come from a **talk by an engineer on the GigaChat team** ([recording](https://youtu.be/a-NIeMB-Hj8)). They are his observations, not our measurements, and we mark them as such. What we add is our own instrumentation on our own fleet, which is the only part of this document we can defend with numbers.

## The four-year compression

| period | what an agent was |
|---|---|
| late 2022 | A clean chat. One prompt, one text answer. No memory, no tools |
| mid 2023 | ReAct. The model can call a function, read the result, correct itself, then answer. This is where the "agent loop" comes from |
| 2023–2024 | Chains of calls, first SDKs, vector databases, RAG. Structured JSON output makes agents embeddable in ordinary code |
| 2024–early 2025 | Scaffolding. Chains become branching graphs; agents get roles — planner, critic, executor. Peak structural complexity |
| late 2025 → now | The reversal. The graph turns out to be unnecessary. One general agent, a handful of file tools, a well-posed multi-step task |

That last row is the interesting one. The industry spent four years building scaffolding around the model and then discovered the building stands without it.

**Harness** is the name for what remains: an agent plus a small tool set. The speaker's metaphor is the clearest definition we have heard. The model is the source of force. The tools are the harness — they transmit the force and constrain it at the same time. Your data is the field. Force, harnessed to tools, is dragged across the field and turns it into finished work. Different tasks, one mechanism; only the contents of the field change.

The core tool set is boringly consistent across open harnesses: read, edit and write files, run shell commands, search across files (they are too big to read whole), fetch from the web, keep a todo list, spawn subagents. That is a system administrator with full access to a machine, and it is enough.

**Practitioner estimate, not a published benchmark:** he has not met a harness carrying more than 30–40 built-in tools, and at roughly 100 tools models start picking the wrong one — any model, including the strongest. Each tool description also sits in the request permanently, whether or not you use it.

## The part that changed how we work

Every long-running agent shows the same symptom. Today it solves your task. Tomorrow you hand it the same task and it appears to have gotten dumber — it forgot yesterday's conversation and re-asks the obvious. Nothing broke. The context ran out, the history was summarised, and summarisation loses data. Always.

On top of that, per the same talk: a model has a **smart zone**, roughly the first third of its context window, where it is at its sharpest. Past that it degrades even if the window is nominally enormous. Also a practitioner estimate.

This reframes the external loop. Wrapping a harness in an infinite shell loop (the RALPH loop, credited to Geoffrey Huntley) so it runs for days is not primarily about compressing history more efficiently. It is about **never leaving the smart zone**: each restart begins with a clean context while the work stays on disk.

## What we measured on our own fleet

Here the borrowed reasoning ends and our instrumentation begins. We built a measurement into `token_cost.py` and ran it across our own machines and transcripts.

**Session startup cost, measured 06.08.2026 across 122 sessions in 14 days:**

| node | median startup context |
|---|---|
| workstation (ZBOOKG8) | 102 180 tokens |
| second node | 91 549 tokens |

And it grows: 86 748 tokens on 31.07 → 106 405 on 06.08. On the hub, a live measurement on 17.08 read **109 996 tokens** before a single word of work.

**The window is bigger than we assumed.** Our own transcripts show a usable window of at least **411 949 tokens** — the "200k" figure we had been reasoning with is refuted by our own data. Same measurement: roughly **64 turns** fit inside the first 40% of that window.

**Cyrillic costs more.** 2.17 characters per token in Russian against 2.81 in Latin script, so identical prose is about 1.3× more expensive in Russian. Our service files are in Russian.

## The conclusion we actually act on

Put the practitioner estimate and our numbers together. If the sharp region is the first third of the window, then **everything loaded at startup is subtracted from the agent's smart zone before it starts thinking.** A bloated always-loaded layer is not merely more expensive per run — it is a standing deduction from intelligence for the whole session.

That is a different argument from the cost one, and it is the stronger of the two. We had been measuring our startup context as rent. It is also a competence tax.

Two consequences we adopted:

1. **Price every improvement in tokens at the moment you build it.** A hook, a status line, an extra always-loaded paragraph: name what it costs per run, per day, and as a share of startup context. Cheap does not mean useful — cost answers "can we afford it", not "do we want it".
2. **Prefer restarting inside the smart zone over summarising to stay in one session.** Summarisation is a guaranteed loss of data; a restart against durable files on disk is not.

## Honest boundaries

- Both the 30–40 tool ceiling and the one-third smart zone are one practitioner's observations without published measurement. We repeat them because they match what we see, not because they are established.
- Our numbers are ours: one small fleet, our own workload. They are reproducible for us and not a general benchmark.
- The instrument lied once before it was trusted. `output_tokens` in a transcript is charged for the entire message — reasoning and tool calls included — and is duplicated across every record sharing a `message.id`. Our first calibration produced 1.2 characters per token, which is absurd on its face, and only the absurdity caught it. Before believing a measurement, show what calibrated the scale.

---

Dev-log for machines: {GH_DEVLOG}
Repository: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
