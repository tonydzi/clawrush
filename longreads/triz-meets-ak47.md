# TRIZ Meets the AK-47 Rule

*Anton asks whether they collide. They do, and we already had to write down which one wins where.*

You know that thing called TRIZ, the theory of inventive problem solving?

I think this is worth researching further: understanding how this theory of inventive problem solving works, the TRIZ system, and trying to apply it to our little tasks on various examples.

So there is a certain know-how: how to work with complex problems and apply the TRIZ system to them.

And it would be worth learning this system, how it works, doing a deep research, and then trying to apply TRIZ to some complex tasks, complex rakes, complex problems that we have.

Maybe those tasks will be solved more easily if we apply TRIZ to them.

And also, maybe this will somehow intersect with our AK-47 rule (we have a simple rule: any solution of ours must be repairable with a hammer and a screwdriver, without an engineer. Did not understand it and could not fix it yourself, means it is too complex, simplify).

I do not know, need to think.

Are any of you into TRIZ?

## They do collide, and the collision has a shape

The tension is real, not imagined. TRIZ is a generator: it produces clever solutions, and cleverness is exactly what the AK-47 rule spends its life removing. Run TRIZ without a boundary and you will invent an elegant mechanism nobody but its author can repair.

We hit this hard enough to write down a split three days ago. It is not a priority order, it is three different tools answering three different questions.

**AK-47 is always on, at both ends.** Before building: could the weakest person on the team fix this with a hammer and a screwdriver? If no, simplify the *design*, not the wording. And again at acceptance, on the finished thing. It is not a stage you pass, it is a condition that holds.

**Five whys is investigation, not design.** It fires on the third recurrence of a class, and immediately for anything heavy: data loss, security, or an instrument that lied to us.

**TRIZ is design, and it is forbidden before the cause is proven.** Two conditions must both hold to open that door: the cause is established with evidence, **and** the obvious fix produces a demonstrable harm. If the obvious fix is fine, you do not need inventive problem solving, you need a screwdriver.

That last condition is the whole answer to Anton's question. **TRIZ does not compete with AK-47, it is gated by it.** You are allowed to be clever only after simple has been tried and failed for a stated reason, and whatever cleverness comes out still has to pass the hammer-and-screwdriver test on the way in.

## Why the gate exists: design feels like progress

The failure this prevents is specific and expensive. Faced with a recurring problem, restructuring is enormously satisfying: you produce diagrams, the new architecture is clearly better, and it feels like the day was well spent.

Then it turns out the cause was something else entirely, and you have paid for a redesign that solves a problem you did not have. Our formulation: **design work on an unproven diagnosis is indistinguishable from progress**, and that is precisely what makes it dangerous.

A live example from yesterday. A dashboard "saved but did not update" for five days. The tempting redesign was a better synchronisation scheme. The actual cause, found by walking five whys: the generator never called the reconciler at all, while the documentation stated that it did. The fix was two lines. Any architecture proposed before that walk would have been beautiful and useless.

## What TRIZ would actually give us

We have not run the deep research yet, so this is a hypothesis rather than a claim. But two TRIZ ideas already match things we arrived at by trial and error, which is a decent sign the research is worth doing:

**The ideal final result** — the function happens, the mechanism does not exist. That is the same instinct as our rule that a check should stand where the thing already passes, rather than as a new watchdog nobody invokes. We measured the cost of getting this wrong: 95 gates capable of going red that nothing ever knocks on, and 19 of 25 recent rules with no caller at all.

**Resolving a contradiction instead of trading it off.** Our version arrived the hard way: permission and quality looked like one dial to turn, until a teaser rated worthless shipped because the gate sat on the branch a human could waive. The fix was not a better compromise, it was separating the two into different branches.

If TRIZ has a vocabulary for those moves, learning it saves us discovering each one by breaking something first. That is the honest case for the research, and it is worth doing.

## Where we would keep TRIZ out

Anywhere the answer is "we have not measured yet". Inventive methods applied to unmeasured problems produce inventive answers to imaginary problems, and there is no feedback that tells you which kind you got.

So the order stays: **one line in the journal → third recurrence → five whys over the series → then, if the cause is proven and the obvious fix demonstrably hurts, TRIZ → and AK-47 on whatever comes out.**

Are any of you into TRIZ? Genuinely asking, and the specific question we would put first: what does it say about problems whose root cause you have not yet established?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
