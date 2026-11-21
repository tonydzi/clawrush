---
name: warm-intro
description: "Warm introduction of two people from your network: match by CRM tags, DM both sides first, create a group, nudge after 3 days. Triggers: 'introduce X to Y', 'make an intro', 'who should meet whom'."
version: 1.0.1
---

# /warm-intro

A warm intro is the most valuable thing a connector trades. This skill turns "introduce Pete to Vasya" into one repeatable operation for Claude Code or Codex, using your own Telegram and WhatsApp.

## Needs
- Claude Code or Codex with a Telegram MCP and (optionally) a WhatsApp MCP connected to YOUR accounts.
- A place where people have tags: CRM, a spreadsheet, or a notes folder. Per person: `strong_at`, `looking_for`, language, channels.

## 1. Pick the pair
- From an order: "introduce A to B". Resolve both people by name, handle and company; ask the owner if two contacts share a name.
- Proactive: for person A, find people B whose `strong_at` matches A's `looking_for` AND vice versa. Write one line per side: what A gets from B, what B gets from A. No two-way line means a weak pair; skip it.
- Facts about a person come only from their card, a research note, or their own words. A guess is marked as a guess and never goes into a message.

## 2. Show the owner first
Show who both people are, the group title, the account that will send, and the drafted texts. Wait for "+". Skip only when the owner says "no approval needed".

## 3. DM each side first
- To A: "A, I want to introduce you to B, they are great at X. OK?" Mirror for B.
- Write in English plus a short block in the person's own language when there is evidence for it.

## 4. Group
- First verify both consent messages and log their IDs. If either is missing, save the draft and stop here.
- Create a Telegram group titled `A <> B <> <Your brand>`, with the final title from the start (basic groups cannot be renamed).
- Post the intro: who A is, who B is, why they should talk, "over to you".
- Require explicit consent from BOTH people for this exact introduction before creating any group or sharing its link. One reply, silence, or a refusal never counts as two consents. If either declines, stop.
- After both agree, add them; if adding is technically blocked, send that consenting person the invite link.
- WhatsApp MCPs usually cannot create groups, so the group lives in Telegram and WhatsApp carries DMs with the link.

## 5. Log
One row per intro: A, B, why, date, channel, proof (group or message id), outcome. Outcomes stronger than `pending` need proof.

## 6. Follow-up after 3 days
You cannot see their private chat, so judge only what you can observe: the group.
- Both wrote in the group: note it as `engaged`, which is not `met`. `met` needs one of them saying they called or met.
- Group is silent: once each, DM A ("A, did you forget about B? I made you a group: <link>"), DM B (mirror), and post in the group ("A, B, don't forget each other: A is great at X, B at Y. I connected you because Z. Get on a call").
- Do not nudge a second time. After that, only proof or the owner sets the outcome.

## Hard stops
Pause and ask the owner when an intro carries money, a commitment, secrets, or would be a mass blast. Pace intros one at a time (anti-ban).

## Style
Short, warm, the owner's voice. No long dashes. Run a final anti-slop pass on any AI-written text before sending.

## Current limits
This is an agent procedure, not an installed autonomous service. Your agent needs working connectors and a place to record consent and follow-up. Follow-up requires a scheduled check or a later manual invocation. This package has not yet completed a live end-to-end introduction pilot. Never claim delivery, consent or a meeting without reading the corresponding evidence.
