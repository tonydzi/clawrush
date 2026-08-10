# dev-log: comment-alpha mining pipeline (2026-08-01)

## Context

A post about our anti-slop detector (LLM-writing-style detector/rewriter for Russian text) received 8 comments. Instead of treating comments as engagement noise, they were processed as an input queue. The procedure was then merged into the existing daily browser routine so it runs unattended.

## Procedure

1. **Harvest.** Comments collected from the author's own recent posts in the same authenticated browser session the daily routine already opens (no additional infrastructure).
2. **Dedup.** Flat JSON ledger; key = `sha256(post_id | author | text[:60])[:16]`. Comment ids are not stable across page rebuilds, hence hashing stable fields. Known tradeoff: an edited comment re-enters as new.
3. **Classify.** LLM call sorts each comment into 4 buckets: artifact / person / promise / idea. Classification is judgment → LLM; everything around it is deterministic code.
4. **Act per bucket.**
   - artifact → hands-on test task (run the code, diff against our implementation; README reading does not count as a test)
   - person → CRM lookup (existing card? interaction history?)
   - promise → task registry entry with a reminder date
   - idea/objection → notes
5. **Report.** One summary line to the coordination channel: comments N / replied K / artifacts X / DM drafts M.

## Results of the first (manual) pass

- 8/8 comments classified.
- 3 recommended repos tested hands-on:
  - humanizer (32,685 stars): line-by-line diff against our ban-list → 0 new rules. Full overlap.
  - humanizer-ru (118 stars): +1 rule adopted — adverbial-participle-clause density (near-zero in casual human Russian, high in LLM output). Merged with source credit same day.
  - ru-text (176 stars): 0 new rules; independently confirmed our protect-list approach (tokens that must never be "cleaned").
- 6/6 commenters checked against CRM (3 existing cards, 3 new contacts).
- 1 promise captured into the task registry with a follow-up date.

Observed and worth stating plainly: star count predicted nothing about usefulness delta. The 32k-star repo contributed zero; the 118-star repo contributed the only adopted rule.

## Guardrails

- Reply automation limited to the author's own post threads; rate-capped (≤40/day, ≥5 min spacing).
- Direct messages are draft-only; sending requires explicit human approval (Tier-2 gate).
- Failure mode to avoid: heroic one-off. The step was embedded into an existing daily routine rather than shipped as a new standalone job; first unattended run is the next scheduled tick.

## Open items

- Auto-parking of stale promise entries — manual for now.
- Rewriter-side dedup: the ban-list currently exists in more than one copy; consolidation pending.

---

📖 Human version (narrative): see the longread in this repo.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
