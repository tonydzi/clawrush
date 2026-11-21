---
name: warm-intro
description: "Warm introduction of two people from your network: match by CRM tags, DM both sides first, create a group after two consents, review follow-up when invoked after 3 days. Triggers: 'introduce X to Y', 'make an intro', 'who should meet whom'."
version: 1.0.2
---

# /warm-intro

Status: procedure draft; no live end-to-end pilot completed. This skill guides an agent through a warm introduction using your connected accounts. It does not run on its own.

## Needs
- Claude Code or Codex with a Telegram MCP and (optionally) a WhatsApp MCP connected to YOUR accounts.
- A place where people have tags: CRM, a spreadsheet, or a notes folder. Per person: `strong_at`, `looking_for`, language, channels.

## 1. Pick the pair
- From an order: "introduce A to B". Resolve both people by name, handle and company; ask the owner if two contacts share a name.
- Proactive: for person A, find people B whose `strong_at` matches A's `looking_for` AND vice versa. Write one line per side: what A gets from B, what B gets from A. No two-way line means a weak pair; skip it.
- Facts about a person come only from their card, a research note, or their own words. A guess is marked as a guess and never goes into a message.

## 2. Show the owner first
Show who both people are, the group title, the account that will send, and the drafted texts. Wait for "+". The owner may explicitly waive their review for this one pair; that never waives either participant consent.

## 3. DM each side first
- To A: "A, B is great at X; you could help each other with Y. May I create a small Telegram group with you and B? Your profile will be visible to the other participant under your Telegram settings. OK?" Mirror for B.
- Write in English plus a short block in the person's own language when there is evidence for it.

- Bind each affirmative reply to the exact person and DM account/chat ID. Log request and reply message IDs. An ambiguous reply needs clarification; never infer consent from silence or a forwarded reply.

## 4. Group
- First verify both consent messages and log their IDs. If either is missing, save the draft and stop here.
- Create a Telegram group titled `A <> B <> <Your brand>`, with the final title from the start.
- Post the intro: who A is, who B is, why they should talk, "over to you".
- Require explicit consent from BOTH people for this exact introduction before creating any group or sharing its link. One reply, silence, or a refusal never counts as two consents. If either declines, stop.
- After both agree, add them; if adding is technically blocked, send that consenting person the invite link.
- Inspect connector capabilities first. Use the channel both people agreed to. If group creation is unsupported, record the limit and ask for agreement to another channel before proceeding; do not silently substitute it.

## 5. Log
Use the owner's existing CRM/table. If none exists, keep one local `intros.md` table. Required columns: intro ID, A/B identity and DM account/chat IDs, benefit to each, consent request/reply IDs, group ID, created time, follow-up due time, A/B/group nudge message IDs, outcome and evidence. Save the draft and state here before stopping. Check this row and live messages before any retry; do not duplicate a proven send. Outcomes stronger than `pending` need proof.

## 6. Follow-up check after 3 days, when invoked
Write the due time (created time + 3 days) into the same row and use an existing scheduler or a manual reminder to invoke this skill again. The skill cannot wake itself. You cannot see their private chat, so judge only what you can observe: the group.
- Both wrote in the group: note it as `engaged`, which is not `met`. `met` needs one of them saying they called or met.
- Group is silent: once each, DM A ("A, did you forget about B? I made you a group: <link>"), DM B (mirror), and post in the group ("A, B, don't forget each other: A is great at X, B at Y. I connected you because Z. Get on a call").
- Do not nudge a second time. After that, only proof or the owner sets the outcome.

## Hard stops
Pause and ask the owner when an intro carries money, a commitment, secrets, or would be a mass blast. Pace intros one at a time (anti-ban).

## Style
Short, warm, the owner's voice. No long dashes. Run a final anti-slop pass on any AI-written text before sending.

## Current limits
This is an agent procedure, not an installed autonomous service. Your agent needs working connectors and a place to record consent and follow-up. Follow-up requires a scheduled check or a later manual invocation. This package has not yet completed a live end-to-end introduction pilot. Never claim delivery, consent or a meeting without reading the corresponding evidence.
