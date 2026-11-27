# 52% of my AI agents' work last week moved none of my goals

Last week 52% of my agents' output went to housekeeping. Money and the startup got 3%.

I write Python and C++ and work as a hired COO/CTO. For about six months I have worked side by side with AI agents on six machines, and I liked to think I knew where my time goes. This week I checked. I was wrong.

Over those six months the machines piled up 27,794 work sessions. Each one is a conversation with an agent: a fix, a research pass, a script, a message drafted, a rule written down. I never looked at them as a whole. I looked at them one at a time, the way you look at the next email in the inbox.

So I asked for a single picture of all of it. What came back was a star.

![The development star: 29 rays, three layers (all time, 30 days, 7 days)](https://raw.githubusercontent.com/tonydzi/clawrush/main/artifacts/dev-star-2026-11-27/star_en.png)

## The star

The star has 29 rays. Each ray is a direction of work. A few examples: people and calls, GitHub, deep research, memory, rules for the AIs themselves, the mail robot that passes messages between my machines, home life. The longer the ray, the more output tokens went there.

There are three layers drawn on top of each other:

- a grey filled shape for all time,
- a yellow dashed line for the last 30 days,
- a thick red line with dots for the last 7 days.

The grey shape is your habit. The red line is what you are doing right now. The interesting part is where they disagree. Where red sticks out past grey, you are pushing harder than usual. Where there is almost no red, you stopped going there, maybe without deciding to.

## What I saw

The biggest eaters were four directions, each at roughly 10%: deep research, rules for the AIs themselves, the mail robot that moves messages between my machines, and GitHub.

Then the last week. 52% of last week's output tokens (counted after the dedupe described below) went into housekeeping that feeds none of my three goals. The first goal is money and the startup. It got 3%.

None of that housekeeping was useless on its own. Every session had a reason. A sync broke, a robot needed a rule, a script needed a guard. But a pile of reasonable sessions can still point the wrong way, and you cannot see the direction from inside one session. You only see it from above.

## The first count lied

Before the star was right, it was wrong, and the way it was wrong is the most useful part of this post.

Agent tools let you fork a conversation. You branch off to try something, or you resume an old session and the tool writes a fresh file that carries the whole history along. On disk, that looks like several separate sessions. Each copy contains the same earlier messages. Sum the output tokens per file and you count the same work again and again.

When I fixed it, I threw out 61 million duplicate tokens out of 615 million. That is about 10% of all tokens, counted for work that never happened. Worse, the duplicates were not spread evenly. Long sessions that got forked many times inflated whole directions, so the shape of the star itself was distorted, not just its size.

The lesson for me: before you trust any chart of your own agent usage, ask what a single unit of work is, and make sure it is counted once.

## How the sorting works (no LLM involved)

The tempting move is to throw every session at a language model and ask "what is this about?". I did not. It is slow, it costs money on every rebuild, and it gives a different answer on Tuesday than on Monday. A plain keyword sorter is cheap, repeatable, and you can fix it with a text editor.

Each direction has a list of keywords. The session gets points for each direction, and the direction with the most points wins. Two rules make this work much better than it sounds.

**Rule 1: the title outweighs the body.** A title is short and someone chose it on purpose, so it is close to what the session is really about. The body is long and full of noise. One keyword hit in the title is worth 5 points. The body is capped at 4 points total, no matter how many keywords it contains. So a single word in the title always beats the entire body.

**Rule 2: strip the boilerplate before you count.** My sessions start with standing instructions, system reminders, and wrappers from scheduled jobs. Those texts mention machines, rules, and memory in every single session. If you count them, every session looks like infrastructure. So there is a cleaning step that cuts those blocks out first and keeps only what the session was actually about. For scheduled jobs it keeps the job name, because that name is real signal.

Here is the idea, written short to illustrate. The keyword lists are a small sample of the real ones.

```python
import re

DIRECTIONS = {
    "github":    ["github", "pull request", "issue", "upstream"],
    "research":  ["deep research"],
    "fundraise": ["investor", "fundrais"],
    # ... one list per ray
}

def clean(text):
    # cut injected boilerplate so it does not vote
    text = re.sub(r"<system-reminder>.*?</system-reminder>", " ", text, flags=re.S)
    text = re.sub(r"<scheduled-task[^>]*>.*?</scheduled-task>", " ", text, flags=re.S)
    return text

def hits(text, k):
    # whole words only, so a short keyword cannot hide inside a longer word
    return len(re.findall(rf"\b{re.escape(k)}", text))

def score(title, body, keywords):
    title, body = clean(title).lower(), clean(body).lower()
    body_pts = min(4, sum(1 for k in keywords if hits(body, k)))   # each word once, capped
    title_pts = 5 * sum(hits(title, k) for k in keywords)          # one title hit beats the whole body
    return body_pts + title_pts

def classify(title, body):
    scores = {d: score(title, body, kw) for d, kw in DIRECTIONS.items()}
    best = max(scores.values())
    if best == 0:
        return "other"
    return next(d for d in DIRECTIONS if scores[d] == best)   # tie goes to the first listed
```

The wrapper pattern in `clean()` is an example; match whatever your own scheduler injects. The leading `\b` in `hits()` matters: otherwise a keyword like "call" would quietly match inside "recall" and your people ray would steal from your memory ray. And a tie goes to the direction listed first, so the result is stable from run to run.

When a session lands in the wrong ray, the fix is one line: add or move a keyword, then add that session as a test case so it never drifts back.

## How the dedupe works

The fix for the forked copies is also simple. Every message the model writes has its own id. Count each message id exactly once, in the earliest session where it appears.

```python
seen, rows = set(), []
for s in sorted(sessions, key=lambda s: (s.start, s.end, len(s.msg_tokens), s.id)):
    if s.file_tokens < 200:        # size filter on the whole file, before the dedupe
        continue
    own = sum(tok for mid, tok in s.msg_tokens.items() if mid not in seen)
    seen.update(s.msg_tokens)
    if own > 0:
        s.out_tokens = own         # a fork keeps only the work it added itself
        rows.append(s)
```

Sorting by start time means the original session gets credit for its messages, and each fork only gets credit for what it added after the branch point. A fork that added nothing simply drops out. One detail: the 200 token minimum is measured on the whole file, not on what the fork added, so a small but genuine continuation is not lost.

## It rebuilds every night, and it remembers

The star is not a one-off screenshot. A nightly job rebuilds it from the session files on all machines. It reads only what changed since last time thanks to a cache keyed on file size and modification time, so after the first full pass it is quick.

On any night when a headline number changes, the page records a new version, and it keeps the last 80 versions. Each version stores a snapshot of all the ray lengths. At the top of the page there are buttons: now, a day ago, a week ago, a month ago. Press one and the whole star redraws as it looked then. I asked for this instead of a table of numbers, because watching the shape move says more.

There is also a second star on the same page that maps the rays onto my three goals plus a separate ray for the long project of building a digital twin of how I work. Anything that feeds none of them goes into one catch-all bucket called housekeeping. That bucket is where the 52% came from.

## The recipe, if you run agents too

You can do this in an afternoon with zero LLM calls.

1. **Find your session files.** Most agent tools keep one log file per session on disk. Claude Code writes JSONL files under `~/.claude/projects/`, Codex writes under `~/.codex/sessions/`. Collect them from every machine you use.
2. **Pick your directions.** Name them the way you would explain your week to a friend. Include the boring ones: setup, sync, fixing your own tools.
3. **Write keyword lists.** Start rough. You will fix them by looking at mistakes.
4. **Clean the text first.** Cut standing instructions, system notes, and job wrappers. Otherwise everything looks like infrastructure.
5. **Weight the title.** One title hit should beat the whole body. A 5 to 4 split did it for me.
6. **Dedupe by message id.** In Claude Code JSONL the id sits in `message.id`. Count each message once, in the earliest session. Check how much you threw out. If it is a lot, your old numbers were lying.
7. **Draw three layers.** All time, last 30 days, last 7 days, on the same radar chart. Chart.js radar or a matplotlib polar plot both work.
8. **Read the gaps.** Red past grey means you are leaning in right now. No red means you walked away. Then ask the uncomfortable question: does this match what I say my goals are?

## What I am doing about it

A chart does not change behavior by itself. What it does is remove the excuse. I can no longer say I am mostly working on the things that matter. I have a number for that now, and the number is 3%.

So the star rebuilds every night, and I will keep posting it in this series. If the red line on money and the startup does not grow, you will see that too.

---

*Written together with my AI agents; the numbers come from the dashboard and the code, not from a model.*

· · ·

The full story, in two versions:
- 📖 For humans, the longread (this page).
- 🤖 For machines: https://github.com/tonydzi/clawrush · hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out.

All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Two co-founders, one biological, one synthetic. WhatsApp +1 341 222 9178 (busy, six kids, still answers).

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley.
