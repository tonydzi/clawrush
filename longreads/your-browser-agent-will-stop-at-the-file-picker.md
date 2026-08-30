# Your browser agent will fill the whole form. It will stop at the file picker.

*A dev-log from a submission that an agent drove end to end, except for one click.*

---

If you are building an agent that drives a browser, you have probably already tasted the good part:
it reads the page, finds the field, types, clicks Next, recovers when the layout is not what it
expected. Multi-step forms stop being a chore.

Then it hits a native dialog and everything stops.

This is a log of one such run: an academic preprint submitted through the arXiv web form, driven by
an agent inside a logged-in Chrome, on 2026-07-23. Nine screens, LaTeX compilation, metadata
cleanup, preview, submit. **One human click in the middle.** That click is the interesting part,
because it is not an arXiv problem and not a Chrome problem, it is a boundary that every browser
agent hits, and most people discover it in the worst possible moment.

Status note before anything else, because it matters for how you read the rest: the paper is
**on hold in moderation**. No identifier yet, nothing to cite. This is a log about a submission
pipeline, not an announcement about a publication.

---

## The setup

- A submission form with nine sequential screens, server-side state, and a compile step that can
 fail on the server minutes after you upload.
- An agent driving a real Chrome where the human is already authenticated. No headless browser, no
 credential handling: the session already exists, the agent operates inside it.
- A LaTeX source file on disk, ~4 pages, one `main.tex`.

That last bullet is where the story happens.

## What the agent did without help

Screen by screen, this part was uneventful in the best way:

1. **Start.** Pick primary archive and license. The agent read the dropdown, confirmed the primary
 category was already the intended one, accepted the license, continued.
2. **Add files.**, *see the next section.*
3. **Review files.** Confirm the uploaded source is what the server thinks it is.
4. **Process.** The server compiled the LaTeX. This is a real wait, with a real failure mode: a
 missing package or a stray character and you are back three screens. It succeeded; the agent
 read the status line and moved on rather than assuming.
5. **Metadata.** Title, authors, abstract, comments. The agent transferred them from the source
 and **cleaned the markup**: `$N$` became `N`, LaTeX dashes became ordinary punctuation. Metadata
 fields are plain text, they do not render your math, they display it. Paste raw LaTeX and the
 listing looks like a first-year mistake to exactly the reader you were hoping to impress.
6. **Preview.** Open the generated PDF, check the page count and the watermark, confirm nothing got
 mangled in compilation.
7. **Submit.**

That is a form that takes an unfamiliar human twenty to forty minutes, done attentively, with the
checks a rushing human skips.

## The one thing it could not do

Step 2. Uploading the file.

The button on the page is ordinary HTML. Clicking it is trivial. What the click *does* is open the
operating system's file-selection dialog, and that dialog is not a web page. It is a native window
owned by the OS. The DOM ends there. The browser-automation layer, whatever it is, has nothing to
address: no elements, no accessibility tree it can drive, no path field it can type into.

There are workarounds, and it is worth knowing exactly what they cost:

- **Set the file directly on the input element.** Many automation stacks expose a "set input files"
 primitive that bypasses the dialog entirely. When available, this is the answer. But it is a
 privileged capability, and agent harnesses that expose files to the model tend to restrict it to
 files already shared into the session, an arbitrary path on the user's disk is refused, by
 design. Ours refused it: the file lived on `E:\`, the session had never been handed it, so the
 primitive was not usable.
- **Drive the native dialog with synthetic keyboard events.** Desktop-automation tools can type a
 path into the dialog. This works until it does not: focus races, the dialog is a privileged
 window on some systems, and screenshots of it may be unavailable. It is the fragile path.
- **Ask the human.** One click. Deterministic. Over in three seconds.

We took the third. The human clicked once, chose the file, and the agent picked the run back up
from screen three.

## The lesson worth generalizing

**Your agent's autonomy ends at the OS boundary, and the boundary is not where you assumed.**

It is not "the hard parts need a human". Compilation errors, metadata cleanup, category rules,
reading an ambiguous status message, the *cognitively* hard parts went fine. What needed a human
was the single most trivial action in the entire process: choosing a file.

Anything that opens a native window is on the far side of that line:

- file open / save dialogs
- print dialogs
- OS-level permission prompts (camera, location, notifications on some platforms)
- certificate and credential prompts
- privileged system dialogs (UAC on Windows, authorization prompts on macOS)

So design for it. Three rules that came out of this run:

**1. Map the native-dialog steps before you build the flow, not during it.**
Walk the target workflow once by hand and mark every screen that opens something the DOM does not
own. That is your list of human touchpoints. Everything else is automatable.

**2. Batch human touches into one waking.**
The expensive part of a human touchpoint is not the click, it is the interruption, a person who is
away, asleep, or in another timezone. Two touchpoints ten minutes apart can cost you a day. If a
flow has several, restructure so they land together, or move the artifact somewhere the privileged
primitive *can* reach before the run starts.

**3. Pre-flight the gate that can reject you on screen one.**
arXiv requires an endorsement in the target archive before you can submit at all. Not at review 
at *Start*. We had spent effort on file preparation while blocked on that gate. What eventually
unblocked it was an endorsement in a **different, adjacent category** that had already been
granted for other work, and which turned out to legitimately cover the paper. The general form:
before building the automation, run the first screen manually and see whether it lets you through.
A gate on step one invalidates the whole pipeline behind it.

## Two smaller scars, free of charge

**Metadata is not LaTeX.** Already said, worth repeating, because it is the most common cosmetic
failure on preprint listings: the abstract field renders nothing. Strip your markup.

**The safety classifier of an agentic browser will interrupt you.** Ours flagged intermittently
through the run; individual actions needed a retry before proceeding. Nothing was blocked
permanently, but if your automation treats the first refusal as a hard failure, it will abandon a
perfectly good run. Build the retry in, and log the refusals so you can tell a classifier hiccup
from a real wall.

## What this is not

It is not a claim that agents can publish research. The agent operated a form. The paper was
written, the mathematics checked and the decision to submit made by a human, and the submission is
**on hold in moderation** as of this writing, no identifier, no announcement, nothing to cite.
When the identifier is issued, it will be linked from the lab site with a date, like everything
else we publish.

It is also not a complaint about arXiv. The form is honest, the compile step gives real errors, and
the endorsement gate exists for good reasons. If anything, it is a better-behaved target than most
commercial software.

## Reproduce, and tell us where it breaks

The coordination machinery underneath all of this, how the agents on separate machines negotiate,
verify each other and stop at the actions a human must approve, is open, MIT, and reproducible in
one offline command:

```bash
git clone https://github.com/tonydzi/claude-consensus
cd claude-consensus
python demo/demo.py
```

Five self-checking scenarios, no network, no API key, stdlib-only Python. `docs/EVALS.md` says how
to reproduce the numbers; `docs/FAILURE-MODES.md` lists nine documented ways it breaks, each linked
to the exact line of code.

**If you build browser agents: we want your version of this list.** Which native dialogs stopped
you, and what you did about it. Open an issue with what failed on your machine, reproductions and
counter-examples are the contribution we value most.

---

*We publish the failures with the same date as the results.*


Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

All channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
