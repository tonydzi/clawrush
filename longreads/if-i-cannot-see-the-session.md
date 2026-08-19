# If I Cannot See the Session, There Is No Point Running the Routine

*552 alerts and approval requests did not reach a human for 16 days. Nothing was broken. That is the problem.*

Work with incoming messages. We have three kinds of inbound: Telegram, WhatsApp and mail. Mail has everything, though I may adjust something. Building further.

I am now building routines for processing messages in WhatsApp and Telegram, and they should be similar. I will run the routines on the anchor node, because you can log into Telegram and WhatsApp from it without ban risk.

**The most important thing: if those routines ask for any approvals, I need to see them. If I cannot see those sessions, there is no point running the routines.**

I have a year of accumulated debt — unread or unanswered direct messages. I am decomposing the task. The first routine will handle incoming. First the debt has to be worked through. I would like to reach zero-inbox status; that used to work for me.

If I am already at zero-inbox, I move on to executing my mission. If a lead does not help me achieve the mission, it gets handled automatically. The routine will be double: clear the old debt and process the last 24 hours. Each day handle more, from 20 to 50 leads of each category in each account.

Maybe I will bring in the CRM, so it pulls in all dialogues from all my accounts and the routine runs on top of that, with the CRM taking on distribution. So the CRM ingests and updates the message database, and then sends them out.

So I have a gradation: from VIP leads — I read what came from them, what they need, I give them information from my side and interact according to our mission; and I need to think about how to bring a lead to a call. Down to the other leads, the unimportant ones — they are processed on a cheaper model, not dismissed, but kept in touch, invited to chats and so on.

Right now I am focusing on setting up this process.

## That one sentence is the whole design, and we learned it the expensive way

"If I cannot see those sessions, there is no point running the routines" is correct, and it is stronger than it looks — because the failure it prevents does not look like a failure.

Our own measurement: **552 alerts and approval requests did not reach the person they were addressed to, for 16 days.** Nothing errored. The watchdogs printed correct paths and honest "file not found" lines. The routines ran. The queue filled. And the only visible symptom was silence, which is indistinguishable from everything being fine.

The root, once found, was mundane and generalises: **the process that sends and the process that runs on a schedule did not see the same filesystem.** A scheduled job under the same account saw six fewer folders than an interactive session, and the messaging rail's session file lived in one of them. Underneath that sat a second failure: the retry path started by importing something the node did not have, so it exited before its first line — meaning the promise "I will resend on the next successful delivery" was unfulfillable by construction.

So the practical rules, all paid for:

**Files a robot needs must live where the robot can see them, and "it works in my session" is not evidence.** The only proof is a one-off scheduled job that prints the result.

**A queue of unsent approvals needs an age alarm, not a counter.** Ours had a counter. A counter that nobody reads is the same as no counter. What was missing was: oldest unanswered item is N days old.

**Silence must never mean consent.** If an approval request cannot be delivered, the routine stops rather than proceeding. Any other choice makes an undelivered question look like a yes.

## On grading leads by mission fit

The gradation is right, and there is one measured trap in the bottom tier.

"Kept in touch, invited to chats" done in bulk is exactly the shape that fails. We measured it on ourselves: a batch of catch-up messages converted **zero**, while a single specific message to one person worked. The cheap model is fine for classification, drafting and extraction; what breaks is when the *output* looks batch-produced to the human receiving it. A generic re-approach does not merely fail, it teaches the recipient to ignore the next one.

Related, from the same measurements: after roughly a week of silence the thread is closed, not paused. Re-approach needs a new reason — a result, an artifact, something that happened — not a reminder that you exist.

## And the honest note about zero-inbox

Reaching it once is a project. Holding it is a different thing entirely, and it depends on the intake rate rather than on the excavation. Ours, for scale: about **658 messages a day** arriving, reduced to about **24 lines** by a deterministic filter on "does this need a human decision". Without a filter like that, zero-inbox is a state you touch once and then watch recede.

Which is why the double routine in the post is the right shape — debt and last-24-hours as separate loops — with one addition: the 24-hour loop is the one that decides whether the debt loop ever finishes.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/if-i-cannot-see-the-session.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/if-i-cannot-see-the-session.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
