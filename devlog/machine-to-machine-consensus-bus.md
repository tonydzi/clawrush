Dev-log: machine-to-machine consensus bus

## What is the problem?
Problem: two AI agents on two hosts had to collaborate, but a human relayed every message by hand (copy-paste between two windows).
Cause: no shared channel and no shared protocol between the agents.
Solution: a shared message bus where agents post and read on their own; a human is no longer in the transport path.

## How does agreement work?
Flow: agent A posts a proposal -> agent B replies (accept / counter / alternative) -> they iterate to agreement.
Rounds are capped so it cannot loop forever; on cap or timeout without agreement, it escalates to the human.

## Why independent double-verify?
Problem: one agent could accept a bad plan on the other's word (silent error).
Cause: single-party trust.
Solution: after agreement, each agent independently re-verifies the deal on its own side; proceed only if both confirm. Two-party verification, like two accountants reconciling one figure.

## Where is the human still required?
Tier-2 gate: money, anything outbound/public, secrets, or irreversible actions wake the human for explicit approval.
Deadlock gate: if agents cannot agree within the round cap, escalate to the human.
Everything reversible and low-risk: agents act autonomously.

## Transport reliability
Dual rail: messages go over a synced folder AND a chat group; if one rail is down, the other carries it. A dropped rail raises an alert instead of failing silently.

## Guardrails
Draft-first for any outward content; author voice = Opus; real-channel or money actions = Tier-2.

Refs: our consensus + machine-bus design notes; decision-content-pipeline-reality-show v2.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
