# "Did You Book the Call?" — the Automation, and the Five Ways It Lied

*The skill exists. The interesting part is not the happy path, it is every place it quietly returned a wrong answer.*

How the call-booking skill works.

If I have a lead who has been brought to a call, and I gave them Calendly — I do not know whether they booked or not until I see a confirmation.

If I cannot see that they booked, or I am not sure it was them, I ping them. So: Calendly given — I ping regardless.

*Dear lead, did you book the call?*

If they write: yes, booked. Great. Then I clarify: for what date? If yes, tell me when.

Once I have detected that, I set reminders: a check 24 hours before the call, and warn the lead one hour before.

I already had automation like this — but I am still improving it so it fires every time.

Do you have skills like this set up?

## It is built, and the design decision that matters is not the pinging

The part worth copying is not "ping the lead". It is that **the automation never guesses whether someone booked.** It looks at Calendly, and it sorts every lead into one of four buckets:

- **booked** — with proof, an actual event identifier, not an inference
- **link is fresh, no booking** — ask them, in words
- **link is older than seven days** — do *not* ping
- **booked, but no card in the CRM** — create the card

The third bucket is where two of the same person's rules collide, and it is worth spelling out because it is a genuine conflict, not an oversight.

One rule says: *no confirmation seen, ping anyway — hey, did you book?* The other, standing rule says: *silent for seven-plus days, stop, do not chase; the next contact must be a new reason, not another nudge.*

Both are right, and they are separated by **the age of the link**. A ping belongs to a fresh link. A ping sent on a seventy-day-old link is precisely the nudge that was forbidden. One threshold, one variable, no argument.

## The reminder goes to the lead, not to you

The version before this one reminded exactly one person: the owner. That feels like automation and does nothing for the call — the participant most likely to forget is the one who is not building the system.

Two consequences that are easy to miss:

**The time must be shown in the lead's timezone as well as yours.** Our self-test pins it: 15:30 Moscow must appear as 13:30 Lisbon *and* 15:30 "his time". A reminder in the wrong timezone is worse than no reminder, because it is confidently wrong.

**"Tomorrow" is a calendar fact, not an arithmetic one.** The 24-hour bucket covers everything from 1 to 24 hours out, and the word "tomorrow" was hardcoded into it. For a lead eight hours ahead, "tomorrow" was today. Fixed by choosing the word from the calendar date *in the lead's timezone*, with a test fixture for exactly that case: eight hours away, still today for him.

## Five ways it returned a wrong answer, all found and closed

This is the useful part, because every one of these looked like a working system from the outside.

**A stale snapshot printed "no calls".** The briefing now prints `pulled_at` in its header, so the reader sees the age of the data. A count without a timestamp is a claim about now, made from the past.

**A missing snapshot printed silence.** Worse than staleness: the script used to fail in a way that read as "no calls today" in the routine's report. It now exits with a distinct code and says out loud: *this does not mean there are no calls, it means we did not look.* An empty result and a failed lookup must never render identically.

**A narrow time window produced false accusations.** The snapshot was collected from today onward, so calls that already happened were missing — and leads we had literally spoken to yesterday appeared as "we sent a link, no booking". Measured on 12 August: **three false accusations out of three.** Fixed by pulling from today minus seven days, all statuses.

**Short handles matched the wrong person.** Link age was keyed by a bare substring match, so a handle like `ki` or `sam` picked up somebody else's date — and the wrong lead got judged as stale or fresh. Both errors surfaced on 10 August, both closed by anchoring the key to the whole field.

**Cancelled meetings reached the reminders.** One broken status filter, and the system confidently warns someone about a call that is not happening.

All five are covered by a self-test proven by mutation: break the code five ways on purpose, get five failures. A test that does not go red when you break what it guards is decoration.

## The one thing we would tell someone building this

The hard part is not sending the ping. It is that **every step of this pipeline can fail silently and look like good news.** No booking found looks the same as no lookup performed. An empty briefing looks the same as a quiet day. A confidently wrong timezone looks like a working reminder.

So build the detector to distinguish *"I looked and there is nothing"* from *"I did not look"* — and make the second one loud. That single distinction caught more real problems for us than the automation itself saved effort.

Do you have skills like this set up? And if so — how does yours behave when the data source is simply missing?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: https://github.com/tonydzi/clawrush/blob/main/longreads/did-you-book-the-call.md
🤖 For machines: https://github.com/tonydzi/clawrush. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: https://github.com/tonydzi/clawrush/blob/main/devlog/did-you-book-the-call.md

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
