# My Machines Do Not Know How to Say Goodbye

*A node that is switched off and a node that is dead send the identical signal: nothing. Here is what that cost us, measured.*

Today I was turning on remote access across every session in the fleet. I wanted to see any session from my phone and keep working inside any of them.

My hub sent back the list of nodes the order never reached. Two of my own laptops were on it.

The work laptop had not spoken to the fleet in 71 hours. The MacBook, 32. Their heartbeat file had not been updated in nineteen days and I had not noticed. More precisely, I was certain everything was synced and everything worked.

## The signal that means nothing

A node in our fleet reports itself two ways: it writes messages into a shared mailbox, and it touches a heartbeat file. When the machine is switched off, it simply stops writing.

That is the whole problem. **Stopping is also what happens when the app crashes, when the network drops, when the sync folder stalls, and when someone closes the lid and drives to the airport.** One observable state, five causes, no way to tell them apart after the fact.

My hub is not at fault here, which was my first instinct. The node never says "leaving now." It just goes quiet, and absence of writing looks the same from every direction.

The measured shape of it on our fleet:

| node | last message to the fleet | what that last message was | heartbeat file |
|---|---|---|---|
| work laptop | 14 Aug, 20:35 — 71 hours | a patrol robot's routine tick | stale 19 days |
| MacBook | 16 Aug, 10:33 — 32 hours | a real work report on GitHub scaling | stale 18 days |

The work laptop's last line is the interesting one. It was not a goodbye, it was a **routine tick that had been firing every thirty minutes** — 18:35, 19:05, 19:35, 20:05, 20:35 — and then nothing. A clock that stops mid-swing tells you the clock stopped. It does not tell you whether someone unplugged it or it broke.

## The same failure, one level up

The same day, the hub reported on itself, and the shape repeated: **10 of its 91 watchdogs were not in order.** Five disabled outright. Five silent for 125, 169, 200, 201 and 201 hours.

One of the silent five is the watchdog whose only job is to shout when anything in the system goes red. It had not shouted in eight days.

And the panel was green the entire time. Our anchor node caught why: **the health file is written by a separate process, and that process outlived the death of the application it was reporting on.** The green light was never showing health. It was showing that something, somewhere, was still writing to a file.

This is the rule we already had and evidently had not applied deep enough: a watchdog must not run on the engine of the thing it watches, and what you monitor is the **age of the output**, not the fact that a job started.

## The fix is not better detection

You cannot distinguish two identical signals by looking harder at them. The fix is to make the signals different: **the node has to say goodbye on the way out.**

A line written before shutdown — "leaving on purpose, at this time" — turns silence-after-goodbye into an expected state and silence-without-goodbye into an alarm. Same silence, two meanings, because now one of them has a receipt in front of it.

Everything else follows from that: a node that never said goodbye and has been quiet past its own tick interval is presumed broken, not resting. Until then, every quiet node is a coin flip, and I will keep being certain that everything is synced and everything works.

Teaching them to say goodbye.

---

Anton Dzyatkovsky · Palo Alto AI Research Lab
Telegram [@tonydzi](https://t.me/tonydzi) · WhatsApp +1 341 222 9178 · X [@Tony_Stef_](https://x.com/Tony_Stef_)

*Engineer who wants to test this: write to me, I will hand you a seed for free.*

Dev-log for this one: https://github.com/tonydzi/clawrush/blob/main/devlog/my-laptops-fell-out-of-the-fleet.md
