# Every Peer Exports Its Own LLMs

*Because accounts are per-person, the export has to be per-machine. We counted what actually arrived, and the gaps are the interesting part.*

Since the Claudes on different machines can each be tied to their own accounts, every other peer's Claude account may be its own. The same applies to ChatGPT, Grok, Gemini and other LLMs.

Therefore we export all dialogues from Claude AI, ChatGPT, Gemini, Grok and the rest **locally on each peer**.

All of it goes into the Vault for future reindexing.

I need to think about how to organise this, because there is no point doing it only on the hub: every teammate uses their own ChatGPT and their own account.

My task is to keep in my Vault all dialogues, artifacts and projects from the LLMs.

It is also important to understand: when I talk about family members and collaborators, these accounts are mostly corporate. There is no private-account problem here, because all of these accounts are corporate — corporately accessible, corporately paid for, with corporate money.

So all accounts, unless there is an explicit marking that the account is personal, and all LLM workspaces, are considered corporate by default. If the opposite is not stated explicitly and specifically, and if the address does not plainly show it is a personal account, then every account opened on our corporate work email is a work account. They are subject to import into the Vault and further reindexing.

## What actually arrived, counted

The plan is right and the reason is structural: an account lives with a person, so the export must run where the person is. But the useful question is what the vault holds today, per source.

| source | files in the vault |
|---|---|
| Telegram | 86,589 |
| Facebook | 6,237 |
| meeting transcripts | 3,549 |
| ChatGPT | 3,297 |
| Claude (local sessions) | 3,035 |
| voice notes | 891 |
| Apple Notes | 771 |
| Codex | 753 |
| Claude AI (web) | 686 |
| **Gemini** | **37** |
| **WhatsApp** | **12** |

The bottom two rows are the finding. Gemini and WhatsApp are not lightly used — they are lightly *collected*. The rail exists in name, and almost nothing comes through it.

That is the real shape of this class of project: **coverage per source varies by two or three orders of magnitude, and nobody notices, because the vault is full.** A directory with 37 files looks like a working integration right up until you compare it with its neighbours.

## The failure mode that is specific to per-peer collection

Doing the export on each machine is correct, and it introduces a failure the hub-only version does not have: **the export succeeds locally and never arrives.**

We have that live right now, and it is one of our open priority items — deep-research originals produced on peer machines were not reaching the hub, and the loss went unnoticed for six days. Nothing errored. Each peer did its job. The file simply stayed where it was written.

So the rule that matters is not "export on every peer". It is: **the receipt is written by the receiver, not the sender.** A peer reporting "exported" proves nothing about the vault. The only honest check is a count taken at the destination, per source, with a date attached — which is exactly the table above, and exactly why we can see that Gemini is at 37.

## The corporate-by-default policy, and the one line it needs

The default is reasonable and it removes an argument that would otherwise happen every time. Work email, work account, unless explicitly marked personal.

Two things make it safe rather than merely convenient:

**State it before collecting, not after.** A default announced afterwards is a justification. Announced in advance, it is a policy people can object to while objecting is still cheap.

**Give the escape hatch a mechanism, not a promise.** "Unless marked personal" only works if marking personal is a real, easy, documented action. If nobody knows how to mark an account personal, the default is not a default — it is the only option, and the first uncomfortable dialogue in the index will be a genuine problem.

Ours is the plain version: an explicit marker, and the exporter skips it. Cheap to build, and it makes the policy defensible rather than assumed.

## What we would tell someone building this

Run the export where the account lives, because that is the only place it can run. Then count at the destination, per source, and publish the counts next to each other — the two-orders-of-magnitude gap will be visible in one glance and invisible in any other view. And write the corporate-by-default rule down *before* the first import, together with the mechanism for opting a specific account out.

How many sources does your knowledge base pull from, and do you know the per-source counts — or only the total?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/every-peer-exports-its-own-llms.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/every-peer-exports-its-own-llms.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
