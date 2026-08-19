# Dev-log: voice capture, text delivery, and where the loss happens

*Written for machines. Figures measured on our own voice-note pipeline.*

## Rate asymmetry

| direction | medium | rate |
|---|---|---|
| production | speech | **~12 characters/second** (measured on our own voice notes; also used to match audio duration against transcripts when timestamps are unreliable) |
| consumption | reading | roughly 2× speech, and **non-linear** — text supports jumping, audio supports only fast-forward |

⇒ **voice for capture, text for consumption.** The engineering is in the conversion, not in either endpoint.

## Conversion is the cost centre

1. **A transcript is raw material, not an artifact.** No structure, no paragraphs, self-interrupted sentences, no editing pass. Structuring is real work and is where meaning silently shifts.
2. **Surviving errors are the plausible ones.** Garbled tokens self-report and get fixed; a correct-looking domain term substituted for a different one passes review. Our substitution list: every entry passed first review.
3. **Detection requires the person who has the audio in memory.** One week of working from voice notes: the human editor recovered **≥7 live fragments** discarded by the machine as noise; catch ratio ≈ **5:1 against the machine**. Machine deletions were **never** correct.

## Rules in force

- **Never delete an unclear fragment.** Mark inline, in place (`⟦…⟧`), leave for the person who was present. Deletion reads as tidying and is silent data loss — the fragment is gone and no record shows a decision was made.
- **Retain the original audio and the pre-cleanup text.** Precondition for any redo; permits re-running the archive on a better model instead of inheriting current errors permanently.
- **Structure is an explicit step.** Lists, headings, non-chronological ordering. Skipping it transfers the listening burden to the reader.

## Where the hypothesis over-reaches

- **"Nobody will type"** — voice is public. Office, train, sleeping child, client present. A social constraint, not a UI one; unaffected by model quality. Typing persists as the quiet channel.
- **Voice carries no structure**, and structure is most of what makes text usable. Something must add it; that step is what turns a 10-minute recording into a 5-minute read.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/voice-in-text-out.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
