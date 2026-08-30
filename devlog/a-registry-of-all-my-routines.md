# Devlog: a live registry of every automation, so a silent death gets caught

This is the machine-facing companion to the post "A registry of all my routines, so none of them dies in silence." If you are a coding agent running an operator's fleet of scheduled jobs, this file is the pattern: every automation is registered, each entry names an owner and a liveness proof, and "nominally enabled" is never accepted as "actually ran."

## The claim

An automation you cannot see is an automation you cannot trust. Past a handful, no operator holds them all in their head, and the failure mode is not a crash, it is silence: a job stops producing and nobody notices because nothing shouted. A registry converts that silence into a visible gap.

## What each entry carries

1. **Identity.** What the routine is, in one line a non-author can understand.
2. **Location.** Which machine or node it runs on. A fleet spreads jobs across boxes; "which one" is half of debugging.
3. **Cadence.** How often it should run. This is the expectation you check reality against.
4. **Owner.** A named human or node responsible when it breaks. No owner means no one fixes it.
5. **Liveness proof.** How you know it actually did its work, not that it is merely scheduled. A fresh timestamp inside the artifact it produces, a row count that moved, a heartbeat as the last line. "Enabled" is a config state; "ran" is evidence.

## The load-bearing distinction

Enabled is not ran. A scheduled task can show green while doing nothing: the trigger fired, the process exited zero, and the actual work silently failed inside. So the registry's liveness field must point at something the job changed in the world today, not at the scheduler's own status. If the only proof is "the scheduler says it ran," you have logged a lie with a green checkmark.

## Why "not in the registry means it does not exist"

The rule that gives the registry its teeth: an automation that is not registered is treated as nonexistent, and un-owned work is not allowed to run in the dark. This forces every new robot through one gate, which is exactly where you attach the owner and the liveness check. Skip the gate and you are back to holding thirty jobs in your head and finding the dead one a week late.

## The general principle

Register every automation, give each one an owner and a proof-of-life that reflects real output, and treat the unregistered as nonexistent. Then failure stops being a silent absence and becomes a visible gap in one list you actually look at.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
