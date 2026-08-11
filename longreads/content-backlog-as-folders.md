# A Publication Backlog Made of Folders

*The draft Anton posted is close to what we run. Here are the four places it bit us, with numbers.*

Let me tell you what I am planning to do with the publication backlog. It is just an idea so far, but I think it works.

There is a folder where posts and drafts land. From there posts are taken into work, and the main thing happens there: how well is it written, is it AI-ish. Then there is a folder for what passed that gate, meaning not slop but normal living creative work.

I might have time to look: if the content is crap, I send it back for rework or rework it myself. If 24 hours after being sent back nothing has been done, and the verdict is good or there is no verdict at all, then after a day the post goes to the distribution folder.

That distribution folder already holds a large, practically endless amount of content.

Then there is a robot on distribution. It slowly carries all of it out. There are fat days when there is a lot of content, there are days with none at all, and then we top up from the tunnel. The robot keeps a tempo, and the tempo is different per project. Takes posts one at a time, publishes, moves on.

All content gets distributed. And it is fine if there are more and more content folders, you can always play with that. When the robot has launched a post, it immediately moves the file from the distribution folder to the "posting done" folder.

This is only a draft.

Needs more research. It seems this is how such schemes work in content factories, and there are no extra folders there.

If you can advise me where to study how to build the flow ideally and how to work with content further, I would be grateful.

## We run this. Four things it does to you.

Our version has been live for weeks: **41 cases in the pipeline**, each one a post travelling across ten destinations. The scheme is right. These are the places it cost us something.

### 1. A folder is not storage, it is a trigger

The single most expensive lesson. Our `approved/` folder was described to everyone as "the shelf where finished texts wait". It was not a shelf. A distributor robot was watching it and publishing from it on its own tempo.

So a text placed there "to keep it tidy" went out to a live audience with nobody deciding to publish it. Nothing malfunctioned. The folder meant "publish this" and the human meant "store this".

If a robot watches a folder, that folder is a **command**, not a location, and it needs a name that says so. Ours is now written down explicitly: `drafts/` is a shelf, and anything that reaches the distribution folder is understood as sent.

### 2. Silence-approves needs a real reader on the other side

Anton's 24-hour rule is right in spirit: a human must not be a permanent blocker. But it only works if somebody is actually looking, and we measured what happens when they are not.

Our escalation log over 30 days: **16 asks to a human, 12 expired with no answer. 75%.** Three consecutive weeks at 100% expiry.

When silence means yes and silence is the norm, "silence-approves" is not a policy, it is an unattended publishing pipeline with extra steps. That is fine if you decided it consciously; it is dangerous if you believe a human is reviewing.

The fix that worked for us is not a longer timer. It is **making the queue small enough that a human reads all of it**: classify each item at the source, handle the reversible ones without asking, and route only the genuinely human ones to a person.

### 3. The gate belongs on the exit, not on the approval step

We put a quality gate on our teaser pipeline. It sat on the `--approve` branch, which is exactly where you would put it.

Then one destination got an `auto` flag, meaning it does not need approval, so it never crossed the branch where the gate lived. A teaser the gate had judged as worthless went out live. The gate printed its refusal to a console nobody was reading.

**Permission and quality are different questions and they belong on different branches.** A human can waive permission with a flag; quality cannot be waived by anything except rewriting. A check attached to a waivable step gets waived along with it. Our gate now sits on the send path and counts only the destinations actually going out in this run.

### 4. Infinite queue plus finite tempo equals dead content

"Practically endless amount of content" plus "the robot keeps a tempo" produces arithmetic that surprises people.

Right now our Medium queue holds **32 finished texts** against a platform ceiling of **2 per 24 hours**. That is sixteen days of backlog. A post written today about something that happened today comes out at the end of the month, when the thing it responds to is forgotten and the links inside it point at conversations nobody remembers.

So the queue needs an **ordering policy**, and it cannot be one policy:

- content tied to an event or a fresh thread goes **newest first**, or it is not worth publishing at all;
- evergreen content goes oldest first and fills the empty days.

Anton's "top up from the tunnel on thin days" is exactly right, and it is the reason to keep both piles distinguishable. What decays and what does not is a property of the text, and it has to be written on the text.

## On "there are no extra folders there"

That instinct is correct, and here is the sharper version: **a folder is fine as a queue, but terrible as a state machine.**

Every time you add a status you need a folder for, you also add a way for a file to be in two states at once, or in none. We hit that immediately: a case has a Facebook link but no GitHub file yet, a teaser is approved but its channel post has not gone out, one destination is paused while the rest proceed. There is no folder layout that expresses that, because the states are per-destination, not per-post.

What we do instead: **one folder per post, and a journal file inside it** that records each destination, its status, its URL and its timestamp. Folders answer "where is this thing", the journal answers "what happened to it". Adding a new platform means adding a field, not restructuring a tree.

The second rule, learned by breaking it: **read config live, never from a snapshot taken at creation.** Our cases used to copy the destination list when they were created. Then a destination was paused, and posts created before the pause never saw it and published anyway. Same class: our repository moved owners, and every existing case still held the old address until it was read fresh.

## Where to study this

Honest answer to the actual question: we did not find a good written source, and we built ours by breaking it. What we would read if starting over is not content-marketing material but **build and release engineering**: an artifact moves through stages, gates run on the way out, the state lives in metadata rather than in its location, and a promotion is recorded rather than inferred. Every problem above is a release-pipeline problem wearing a content costume.

And one measurement, since it decides everything: **count what is consumed, not what is produced.** Our own teaser gate has been invoked 465 times, and the count that made us change anything was different — the day it found that 22 of 29 teasers carried no usable value, which is 76%. Production volume was never the constraint.

If you build this, the question to answer first is not "how many folders" but **"what does the robot do when the queue is empty, and what does it do when the queue is a month deep?"** Those two are the whole design.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/content-backlog-as-folders.md
🤖 For machines: https://github.com/tonydzi/clawrush. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/content-backlog-as-folders.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
