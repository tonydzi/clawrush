# The night shift: what my AI agents do while I sleep

*Including the failure that broke my own rule about watchdogs.*

---

My company has a shift that works from 23:00 to 06:00 and does not ask for a salary: a fleet of AI agents across my machines. Here is how their night is built, and why it is the most productive part of my day.

## Why night

During the day the agents get in my way and I get in theirs: heavy indexing slows the laptop, "may I?" questions interrupt my meetings. So the rule is that everything heavy and everything non-urgent goes into the night window. The day stays clean for live work.

## The actual schedule

1. **~23:00 — day close.** Agents summarise what got done, what stalled, what is waiting on my decision.
2. **00:30–04:30 — heavy background.** Importing fresh data (conversations, calls, documents), reindexing the knowledge base, backups, deduplication.
3. **Every 15 minutes, all night — pulse.** Each machine sends a short "alive, sync green, disk fine" into a shared Telegram channel. A silent machine is an incident, not "probably asleep."
4. **~05:00 — morning briefing.** By the time I wake up there is a digest: mail, tasks, what broke and has already been fixed, what actually needs me.

## The rules without which this would collapse

**Rule 1. At night an agent decides for itself, but only reversible things.** Exactly one category may wake me: money, publications, irreversible deletions. Everything else — do it, log it, show me in the morning.

**Rule 2. Questions accumulate, they do not wake you.** Anything an agent is unsure about goes into the morning report with a standard marker and a proposed default.

**Rule 3. Watchdogs do not sleep.** Simple scripts, not neural networks, check counters every few minutes: machine sync, task queues, backup freshness. A model can fail to notice a problem; a script with a counter cannot.

## The failure that broke Rule 3

Now honestly about how that same principle let me down.

The Facebook data collector stood dead for **eight days**: its browser session had logged out. Chat synchronisation stood for **nine**. Not one watchdog raised an alarm — both robots dutifully reported "run completed, exit code 0" the entire time.

The defect was in *what* they were checking. The watchdog was looking at the fact of a launch, not at the age of the result. The script started, hit a logged-out session, terminated cleanly with a zero and reported success. Formally everything green, factually no data for nine days.

The fix came down to one line of meaning: check not "the robot ran" but "the file it was supposed to update is less than a day old." A watchdog now also lives outside the system it watches — if that system dies, a watchdog inside it dies with it, silently.

If your monitoring has been saying "all good" for a suspiciously long time, go look at what it is actually measuring. A script with a counter beats a neural network only when the counter counts the right thing.

## What to take for yourself

- Carve out a night window and push everything heavy into it. Those are seven free hours a day.
- A pulse every 15 minutes plus the rule "silence is an incident." Otherwise a dead machine is discovered a day later.
- Split "decide yourself" from "wake me" with one hard criterion: reversibility.
- A morning briefing instead of night-time questions: the agent accumulates, you decide in one batch over coffee.

Want a night shift like this? I am putting together a group of testers: engineers get a free seed of the stack for feedback.

---

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
