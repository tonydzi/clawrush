# Agents in Other People's Group Chats

*The architecture in this post is right. The trigger is the part that will get you removed from the room.*

Still thinking about routines. Inbound routines I can run either on the anchor node or on the hub. For now I am in favour of only the super-important routines living on the hub, while the anchor node can comfortably run all of these, because WhatsApp, Telegram and mail can all be done there.

My CRM should run specifically on the anchor node. So the CRM is an intermediate layer between the AI and Telegram — I will need to connect it to WhatsApp and mail too, so the AI only works with messages and does not go into Telegram itself, because that is too complicated a construction. In the end I will have two WhatsApps and four Telegram accounts.

Another important point: I will have a routine for incoming messages in Telegram groups. Not in direct messages — specifically in groups. Not big groups of thousands of people, where it is spam. Right now I am interested in small groups, up to about twenty people.

If there is a message in a group from anyone other than my account — regardless of whether they pinged me or just left a message — the main thing is that there is a message that is not mine. It needs a reaction. How to react is probably better decided on a cheap model.

I have my missions: mission one, find a job at an LLM company; mission two, gather a community of engineers; possibly another mission, earn money for our project. If we are answering messages from important leads, my agents should talk there and say what we do. And, following the no-waste rules, assess how important those leads are. If they are important, we try to give them value: answer their messages and say "let us have a call". In parallel we give links to what we are building — our Telegram chat, channel, GitHub, our groups. We need testers, angels, VCs, engineers.

## The architecture is right. One line in it is not.

The layering is correct and worth stating again because it is the durable part: **the CRM between the messenger and the model** means credentials never enter a session, retries and duplicate deliveries are handled once, and the message history outlives the session that read it. "The AI should not go into Telegram itself" is the correct instinct.

The line that will cost you is this one: **"the main thing is that there is a message that is not mine — it needs a reaction."**

That is a trigger on **volume**, not on **signal**. In a twenty-person group, that fires dozens of times a day. And the room being small is exactly what makes it dangerous — in a chat of thousands, one more voice disappears; in a chat of twenty, everyone notices who talks constantly.

## What happens next is predictable, and we have the receipt

An unfamiliar participant who reacts to everything and periodically mentions what they are building does not read as helpful. It reads as promotion, and the outcome is not "lower conversion" — it is removal, and it is permanent. **The cost is asymmetric: a good reply earns one conversation, a bad pattern loses the whole room forever.**

Ours, measured: we once had 28 comments sitting unanswered in someone else's group — a room where we were guests, and where access from that account has been lost since July. The account is gone and the room is closed to us. That is what losing a room actually looks like afterwards.

And separately, on the reply style: we measured that a batch of similar outreach messages converted **zero**, while one specific message to one person worked. In a group chat the batch effect is worse, because everyone sees all of your messages next to each other. Ten generic replies in a row are not ten attempts — they are one visible pattern.

## The trigger we would use instead

Not "a message that is not mine". Any one of these three:

**We were named.** A mention, or our project named by someone else.

**A question in our domain that nobody has answered yet.** Not answered better — answered at all. Adding a fifth opinion to a solved question is noise.

**A person we already have a relationship with**, in which case it is a conversation, not outreach.

Everything else: read, log, stay silent. Silence in someone else's room is not a missed opportunity; it is the thing that buys the right to speak when it matters.

Two more constraints we run, both cheap:

**The agent identifies itself.** If a machine writes in a room of humans, the first line says so. Our synthetic co-founder names himself in every thread he writes in. Not doing that in someone else's group is where the line actually is — not in the automation, but in the pretence.

**Links are a reply to a request, not an attachment to every message.** "Here is what we are building" belongs where someone asked what you are building. Anywhere else it converts a conversation into an ad, and the room updates its opinion of you accordingly.

## On the cheap model deciding "how to react"

Fine for classification and drafting — that is exactly the work it is good at. But it should not decide **whether to speak at all**, because that decision is asymmetric: staying silent costs one missed message, speaking wrongly costs the room. Make the "speak" branch conservative and hard-coded, and let the cheap model only choose the wording once the branch is already open.

The mission-based scoring is the right frame, with one addition: score the **room**, not just the person. A room where three of your target audience talk weekly is worth patience and silence for a month. A room with one loud lead is worth one direct message and nothing else.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
