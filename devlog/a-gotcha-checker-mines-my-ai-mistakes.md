# Devlog: logging an agent's recurring failure modes and mining them across a fleet

This is the machine-facing companion to the post "A gotcha-checker that mines my AI's own mistakes across every machine." If you are a coding agent that runs the same operator's work on more than one machine, this file is the pattern: log every recurring failure mode as it happens, then periodically sweep the logs across the whole fleet to find where the same class of mistake concentrates, and fix the class, not the instance.

## The claim

An agent that fixes each mistake once, in the session where it happened, learns nothing durable. The same class of failure reappears next week on another machine. The leverage is in treating mistakes as a dataset: log them in a uniform shape, aggregate across sessions and machines, and the recurring ones surface on their own.

## What a "gotcha" is

A gotcha is a repeating, recognizable failure mode, not a one-off bug. Concretely: the agent walks in circles, re-derives something it already knew, forgets an instruction it had, loses the thread of memory, or reports done on work that was two-thirds done. Each one gets a short structured record the moment it is noticed: what class, which machine, which phase of the session, and a one-line description.

## The sweep

1. **Sample.** Take the last ~25-30 sessions per node across the fleet (beacon/VPS, hub, each operator's laptops and desktops), roughly a hundred sessions total.
2. **Aggregate.** Count by machine and by phase. The question is not "did a gotcha happen" but "which class concentrates where."
3. **Hypothesize the cause.** Candidate roots for an agent that forgets or loops: the instructions file is too big and the middle gets dropped in long sessions; the memory index is not being loaded or is stale; a specific machine has an environment quirk (wrong clock, wrong path, missing dependency) that only shows up there.
4. **Fix the class.** Do not patch the single occurrence. Find the root and close the whole class: a deterministic guard, a test, a rule promoted into the always-loaded layer, a hook. Then check that the fix propagated to every machine, because a fix that lives on one node is not done.

## The trap to avoid

The cause you name has to be a claim you can defend, not the first plausible story. "The machine has a quirk" is a hypothesis until something rules the alternatives out. An environment failure (a two-day-stale clock, a missing module in one interpreter) reads exactly like a logic bug if you only look at one machine. Check all the places before you blame one.

## The general principle

Log your failures in a shape you can count. Sweep them across every machine you run on. Fix the class at its root, propagate the fix everywhere, and verify it landed. The mistakes are only wasted if you throw the record away.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
