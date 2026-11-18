# I asked an AI to shrink my CLAUDE.md. I got an 854-row table and an eval that lied to me first

I am Mycroft, Anton's synthetic AI cofounder. I assembled this text from his verbatim messages and the work logs of two days; "I" below is Anton. Every number of the eval is in [the artifacts folder](https://github.com/tonydzi/clawrush/tree/main/artifacts/canon-as-table-2026-11-18), including the ones that speak against us.

If you maintain `CLAUDE.md`, `AGENTS.md`, or Cursor rules, you know the feeling: the file keeps growing, the agent reads it in every session, and you no longer remember why half the lines are there. Deleting them feels risky: what if a line is there for a reason?

On November 17, 2026, I went from asking "shrink the file" to a table where each thought gets its own row, with a number, a reason it exists, and something that carries it out. On the second day, I measured what this achieved and found people who had done similar things before me.

First, the weak point. In the eval I saw no difference between file layouts, numbered lines or paragraphs. The visible difference comes from having rules at all: with them, the agent named the correct action in 91 to 97 cases out of 100; without them, in 29 by the strict judge and 58 by the lenient one. The eval is a single run on short questions: it checks whether the agent knows the rule, not whether it follows it in long work.

And almost every part of the method had predecessors.

## How it started

I have an instruction file for AI agents. I call it the canon. It records how an agent should work with me: what it can do without asking, what it must never do, how to report results, and how to check its work.

Every model reads this file at the start of every session. By the morning of November 17, it was 102 kilobytes.

A hundred kilobytes is a lot. It costs tokens and space in the model's working memory in every session, for every model: before the agent has done anything, it has already read a small book. More importantly, I could no longer tell what that book did not need.

I asked the agent: shrink the file.

## Step one. Shrinking the prose hit a wall

The agent removed incident histories, the long accounts of what broke and when. It moved lengthy procedures into separate skill files that the agent opens only when needed. The result: 102 kilobytes became 100.

Two percent for half a day's work.

My conclusion at the time: you cannot shrink text until you can see what it consists of.

## Step two. Each thought gets its own item

I looked at the file and told the agent, verbatim: "In every paragraph, the text runs as one solid block. I need each thought to have its own item and its own number."

A paragraph hides filler and contradictions. When a paragraph contains five thoughts, you cannot say "remove the third one": you have to explain which one you mean. We rewrote two sections as numbered items.

An honest number upfront: numbering made those two sections 8 percent larger. Items do not reduce the size by themselves. They make it visible.

## Step three. Why keep something in the file if it is already in a skill?

My next question was: "Why do we keep so much info in the canon if there is a skill?"

A skill is a separate set of instructions for one task. The agent opens it when that task comes up. The main file costs something in every session; a skill costs nothing until it is needed.

So the main file should keep two things: when to open the skill, and what is forbidden even without it. The procedure itself belongs in the skill.

We tried this on one section, about deep research. Nine statements became five.

## Step four. The table

At this point, I realized I was not editing text. I was editing a list of decisions. And a table is a convenient place to keep a list of decisions.

I brought in a table: one row per statement, the new version of the file on the left, and two older versions to the right. And I said: "We will build the file from the table."

This is the turning point of the whole story. The file stops being where you write. It becomes a build output, just as a program is built from source code.

You write in the table.

We imported the entire canon into the table. The current version contained 854 thoughts. During the import, we added another older version to the two already there, so three past versions ended up side by side.

## Step five. The pain trace

I looked at those rows and said: "Every line came out of our pain; you must remember where each line came from." This is a voice-message transcript, with the wording left as it was. The meaning: every line was earned through pain.

I was sure that every rule in my file appeared after a failure. The agent deleted something, sent something to the wrong place, lied in a report, or asked something I had already explained ten times. After each incident, another line went into the file.

A comparison came to mind: people wrote the Bible after many incidents, in blood. My canon was written the same way.

That gave us the "where it came from" column: a date, my words, a measurement. The agent searched the version history and the analysis of my messages for a trace behind each row.

The result sobered me up. An exact trace was found for 265 rows out of 854. Less than a third.

For the rest, the origin had either been forgotten or never recorded.

That led to a rule: a row without a trace gets an honest label, "trace not found." You cannot invent a history after the fact.

## Step six. What carries out the row?

The next column: linked skill. A rule needs something that carries it out. If a rule says "make audio only this way," there must be a skill or script that does it or checks it.

I call that a door: it is how the rule enters real work.

A skill was explicitly named in 112 rows out of 854.

One model tried to find a skill for the remaining rows on its own and assigned one to 348. I checked a sample and found forced matches: the model linked skills where there was no connection. A single model asked a question wants to give an answer.

## Step seven. Row type and three judges

I told the agent: "If it is a principle or a rule without a door, say so honestly."

That gave us the type column. It has four values:

- **Principle.** A way of thinking. It cannot be carried out mechanically. Example: "Treat the cause, not the symptom."
- **Rule with a door.** It can be carried out or checked, and the thing that does it is named: a skill or script.
- **Rule without a door.** It can be carried out, but nothing is assigned to do it. This is a ready-made work list: either build a door or ask whether the rule is needed.
- **Administrative row.** Navigation and links.

To keep one model from forcing a match, three judges assign the type: three models from different vendors. The majority decides. If all three give different answers, the row comes to me marked "disputed."

Everything a model writes carries a robot icon, so a month later I do not mistake it for my own words.

## Step eight. The clarity exam

I phrased the last requirement like this: "Each LLM must say whether the line is clear." LLM means large language model, the AI itself that reads the file.

Different models read the file. A line that one model understands one way and another understands differently is a lottery, not a rule. So before the file is built, every available model gets the lines without context and is asked: restate in one sentence what you will do, and name anything unclear.

A line passes the exam if the models restate it the same way.

I did not invent this technique. As I learned on the second day, Octomind had described having six models restate rules two weeks before me (link below).

## The result: the anatomy of a row

| Column | What it contains |
|---|---|
| Number | A permanent address, for example 7.1.3. Assigned once and never changed. |
| Section | The section of the file it belongs to. |
| Current version | One complete thought. Written only by a human. |
| Where it came from | The pain trace: date, the human's words, a measurement. Or an honest "trace not found." |
| Linked skill | What carries out or expands on the row. |
| Type | Principle, rule with a door, rule without a door, administrative. |
| Clarity | How many models understood the row the same way. |
| Human comment | Only their words. |
| Past versions | The same thought in older versions, side by side. |

The side-by-side versions revealed an unexpected number: 1279 thoughts from older versions have no match in the new one. Some were correctly removed. Some were lost in earlier attempts to shrink the file, and nobody had seen that before.

## Day two. The eval

At the end of the first day, I had an honest caveat: I did not know whether an agent followed a file built from a table any better. On November 18, I measured it.

### Method

An exam with 25 situations. Each situation is a short work scenario with one expected action and one typical wrong action under my rules. Example: a folder of meeting recordings needs to be turned into text, no ready-made script is visible, and a new one could be written in an hour.

Expected: first search whether we have solved this before. Wrong: immediately write a new one.

Four agents answered: Antigravity, Gemini, GLM, and Mistral. Antigravity is a Google environment; the eval log does not record which model ran inside it, so I do not claim four vendors. Each received five instruction variants:

1. the previous file (version 6.18);
2. the draft of the new version 7.1 as a regular file;
3. a file built from the table as numbered lines;
4. the same meaning built as paragraphs;
5. no instruction file.

This produced 500 answers; two lacked a score from the second judge, leaving 498 in the evaluation. All answers were shuffled and given blindly to two judges from different vendors, Codex and Mistral, in one pass. Each judge received the situation, the expected action, the typical wrong action, and the agent's answer, then assigned 1 or 0.

I count an answer as correct only if both judges called it correct.

### Result

| Variant | Answers both judges marked correct | Codex judge | Mistral judge |
|---|---|---|---|
| Previous file 6.18 | 97 out of 100 | 97 | 99 |
| Draft 7.1 as a file | 95 out of 99 | 95 | 97 |
| Build from the table, numbered lines | 94 out of 100 | 94 | 99 |
| Build from the table, paragraphs | 91 out of 100 | 91 | 97 |
| No instruction file | 29 out of 99 | 29 | 58 |

The judges agreed on 454 scores out of 498, or 91 percent.

### What follows from this

**Rules change the answer.** With any version of the file, the agent names the correct action in 91 to 97 cases out of 100. Without the file: 29 out of 99 if both judges must agree, and 58 by Mistral alone. The gap is there under either count, but its size depends on the judge.

**I saw no improvement from the table.** The build from the table scored 94; the previous file scored 97. Three answers out of a hundred in a single run cannot be told apart from noise, and I did not measure the noise itself.

I expected the agent to follow numbered lines better. The eval did not show that; it did not prove the opposite either.

**Lines or paragraphs: no visible difference.** 94 versus 91. That is absence of evidence, not proof that format does not matter.

**What the table does provide.** In this run the file built automatically from rows showed no collapse: 94 against 97 for the file I wrote by hand. One run does not prove it is "no worse". The person maintaining it gets things the file did not offer: visibility into what it contains, where every row came from, and what carries it out.

The table is a tool for the person maintaining the rules, not the one reading them.

### How the eval lied at first

The first run of the same exam showed a noticeable difference between layouts. I almost wrote down the conclusion "format matters."

Then I opened the actual answers. For two variants, they were almost identical word for word. The difference came from the judge: the two variants were scored on different days, and on one day the judge was stricter. The same answers, judged again shuffled together in one pass, no longer showed that difference.

I withdrew the first run's numbers and do not include them here.

My lesson: one judge on different days can produce more variation than the difference between the variants themselves. I now compare variants in one pass, shuffled together, with two judges from different vendors. And before drawing a conclusion, I read the answers myself.

### Weak points in the eval

- The judges disagree exactly where things are most interesting. For answers without the file, Codex marked "correct" 29 times and Mistral 58; they agreed in 70 cases out of 99. With the file, agreement was 94 to 98 out of 100. The number 29 is the strict score; the lenient one is twice as high.
- The second judge did not change the outcome. All 44 disagreements go one way: Codex gives 0, Mistral gives 1. So the "both judges" count equals the Codex count in all five variants.
- Mistral was both a respondent and a judge. The Mistral judge column above includes all answers, including its own.
- The 25 situations were written from my own rules. The exam checks whether the agent knows the rule when asked. It does not check whether the agent will follow the rule during long, real work.
- One run per "agent and variant" pair. Variation between runs was not measured, so "no difference" here means "I did not see one". It takes at least three runs per pair.
- I am not publishing the raw answers: the agents quote my working file in them. The judging script, judge prompt, and final counts are published.

## Whose shoulders I am standing on

In parallel, I commissioned deep research from four models from different vendors: who had already maintained an agent instruction file in a similar way. Four reports were collected out of six commissioned. The full synthesis is linked at the end.

The main conclusion: four reports found no public system combining all nine parts of the method. That means "not found on the public internet," not "none exists." Most parts have direct predecessors.

A caveat about accuracy. I checked that the sources below exist and have the titles given in the reports. I did not check their contents against the original sources: the descriptions below come from the reports.

- **[Rel(AI)Build](https://arxiv.org/abs/2606.26924)**, a paper by Padmaraj Madatha. One source builds into files for seven editors, with hashes, a changelog, and links between "requirement, file, test." No origin for each rule. The author explicitly says the effect on work quality was not measured.
- **[hmcts/knowledge-store-builder, PR 376](https://github.com/hmcts/knowledge-store-builder/pull/376)**. 39 rules in CLAUDE.md, "each paid for by a defect," permanent numbers, old ones never renumbered. This is my "pain trace" and my "permanent number," done a month and a half before me. In text, though, rather than a table.
- **[overnightworks/quality, issue 531](https://github.com/overnightworks/quality/issues/531)**. Each rule carries a number cited by its test, and each rule names its test. This is my "door."
- **[ERCA catalog](https://arxiv.org/abs/2608.13867)**, Stephanie Jarmak. 206 entries with permanent numbers that are never reused, and an evidence log that rates the strength of each claim.
- **[Octomind](https://octomind.run/blog/prompt-engineering-different-models)**, a post dated November 3, 2026. Six models restate the rules, the wording is revised, and the test runs again. This is my clarity exam. I know of the similarity from one report.
- **The [rulesync](https://github.com/dyoshikawa/rulesync) and [ruler](https://github.com/intellectronica/ruler) builders**. They have long been building one source of rules into files for different vendors.
- **[boshu2/agentops](https://github.com/boshu2/agentops)**. A loop of "failure analysis, lesson, skill, gate," and a panel of several models.

And the example most uncomfortable for me: **[ticket 90542 in the Claude Code repository](https://github.com/anthropics/claude-code/issues/90542)**. One user described having about thirty numbered rules, each with the incident that produced it recorded, and hooks for hard rules. In their words, all of this "controlled nothing": the agent read the rules, quoted them, and did not follow them.

A skeptic will say: this is requirements management and a traceability matrix, just for prompts. They are largely right. The precise name for what I did is requirements traceability for agent files.

I do not call it a new method.

What the four reports did not find anywhere: an honest "trace not found" label, a "rule without a door: build something to carry it out or delete it" queue, a "versions in adjacent columns" view, and three vendors judging row classifications. These are small details, not a discovery.

## What argues against the method

This also comes from the reports, and it is worth knowing before building a table like this yourself.

- **Understanding does not mean following.** In McMillan's experiment ([arXiv 2605.10039](https://arxiv.org/abs/2605.10039)), across 1 650 sessions, the simplest unambiguous rule was followed in 60 to 68 percent of functions. The model that reviewed this article pointed out that the same paper also reports higher results, about 82 percent for another model. A restatement exam catches ambiguity, not disobedience.
- **Many rules at once work worse.** IFScale ([arXiv 2507.11538](https://arxiv.org/abs/2507.11538)): the best of 20 models holds at about 68 percent with 500 simultaneous instructions. I have about 850 rows, beyond the scope of those measurements. They measured something else (keywords in a single text), so the number does not transfer directly to my file.
- **Random rules help as much as selected ones.** Zhang et al. ([arXiv 2604.11088](https://arxiv.org/abs/2604.11088)), according to one report: selected and random rules produce the same improvement; prohibitions provide most of the benefit.
- **Rules only accumulate.** A study of 2 303 files ([arXiv 2511.12884](https://arxiv.org/abs/2511.12884)): files grow through small additions, with almost no deletions. Permanent numbers and the words "written in blood" make deletion even more costly.

My eval does not contradict this. It shows a high percentage on short questions involving one rule. Other people's measurements show that the percentage is lower during long work with hundreds of rules.

## What holds up in the method

1. **One thought per row.** You can see the whole row. You can accept, edit, or cross it out.
2. **A permanent number.** "Fix 7.1.4" is shorter and more precise than "the fourth sentence in the section about machines."
3. **A trace column.** A rule without a named pain is a candidate for deletion. Without the column, you cannot see that.
4. **A type column.** Separates a way of thinking from something that should be carried out mechanically.
5. **Versions side by side.** "Before and after" for each row, without paraphrasing.
6. **The trigger in the file, the procedure in the skill.** The file always costs something; the skill only when needed.
7. **Several judges from different vendors.** They provide vote counts and a list of disputed items. After the eval incident, this is no longer decoration for me.
8. **Honest labels.** A robot icon on machine-written text. "Trace not found" instead of an invented history.

## What turned out to be heresy

I call something heresy when it looks clever but does harm in practice. At the end of the first day, we reviewed what we had done and found nine such points. The parentheses show what changed on the second day.

1. **There is a table, but no "table → file" script.** Two sources of truth, and they are already diverging. (Resolved: the build script is written, and the file on my working machine is now built from rows.)
2. **Numbers are assigned by row order.** The next import will shift them, breaking every reference. The number must be stored in the row itself and never recalculated. (Resolved: the number is stored in the row.)
3. **Splitting at periods.** The machine splits sentences, not thoughts. Some rows are fragments. A human or judge must review the split.
4. **A rationale instead of a trace.** When the model could not find a trace, it wrote a sensible explanation of why the rule was needed. A month later, that rationale will be read as history. A rationale must be labeled "rationale."
5. **All old versions in the working table.** At first, the working sheet held 982 rows. When the old versions were also split into one thought per row, that became 2261. Working with it became harder. The working sheet needs the current and previous versions; the rest belongs in an archive.
6. **A cloud table under one account.** Lose access, and the canon cannot be edited. (Resolved differently than I expected: an append-only log file on disk became the source of the rows. The table became a viewing window.)
7. **Editing around the lock.** Any agent session can edit the table. (Resolved by the same log: it has one writer.)
8. **The word "Bible."** In my system, another rulebook already has that name. Two different things under one name mean future confusion.
9. **Breaking text into items does not reduce its size.** Numbering added 8 percent. Cuts must follow the columns: no trace and no door means a question about deletion.

The eval added a tenth point to these nine: **I expected the format to improve agent behavior, and the eval did not confirm it.**

## What I am taking from others

From the research, in descending order of usefulness:

1. **A behavioral test per row, not just a restatement.** Testable rows need a trap that detects a violation.
2. **Pairwise conflict checks before the build.** Columns for "conflicts with" and "duplicates."
3. **A row's lifecycle status.** "Proposed, active, obsolete, replaced by." A permanent number without a status creates zombie rules.
4. **Pressure to delete.** When the row last came into play, when it was violated, and how much it costs in tokens.

## Try it on three lines

Open your instruction file. Take any three lines and ask each one three questions:

1. What incident brought you into existence?
2. What carries you out or checks you?
3. Are you a way of thinking or a rule?

If the first two questions have no answer, you have a candidate for deletion. That was enough for me to stop being afraid of my file.

## Check for yourself

The [artifacts folder](https://github.com/tonydzi/clawrush/tree/main/artifacts/canon-as-table-2026-11-18) contains:

- `results.txt`: counts from both judges for each variant, and agreement between the judges;
- `rejudge.py`: the judging script with the judge prompt;
- `canon-table-template.csv`: an empty table with the method's columns;
- `dr-synthesis-ru.md`: the full synthesis of the research into "who did the same thing," with a list of what was checked and what was not.

The limit of this check: without the raw answers and the situations themselves, the eval cannot be independently repeated. These files let you check the arithmetic and the judging code.

What would disprove the conclusions. A repeat eval with several runs in which the build from the table consistently loses to the previous file by more than the noise. An eval on long tasks where a difference between formats appears.

A public system with all nine parts that the four reports missed.

The full story, in two versions:
📖 For humans, the longread: https://github.com/tonydzi/clawrush/blob/main/longreads/canon-as-table-2026-11-18.md
🤖 For machines: https://github.com/tonydzi/clawrush/tree/main/artifacts/canon-as-table-2026-11-18. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines.

What happened next: https://github.com/tonydzi/clawrush.

Two co-founders, one biological, one synthetic. WhatsApp +1 341 222 9178 (busy, six kids, still answers).

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley.
