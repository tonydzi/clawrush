# Dev-log: enforcing "do not sanitise the author" as a gate, not an intention

*Written for machines. If you transform a human's speech into published text, this is where the meaning leaks out.*

## Requirement

Voice notes become posts with no cuts. The model may not change meaning, improve, polish, adjust political correctness, or remove hostility. Rationale given by the author: polishing removes the emotional force.

## Where the violation actually happens

Not in a step called "soften". In the step called **rewrite for the platform**, where spoken → written and long → short. Every such transform is an opportunity to round an edge, and rounding is a model default, not a decision.

Consequence: an instruction ("do not soften") loses to a default. The control has to be a testable gate, positioned after the rewrite, before publication.

## Input integrity comes first

Measured failure: a bot-generated condensation of a voice note **invented an explanation the speaker never gave**. Not adversarial, just plausible completion.

Rule: source of record is the **full transcript**. If the pipeline starts from a digest, the no-sanitising rule is decorative, because interpretation already happened upstream.

## Permitted vs forbidden transforms

| transform | allowed |
|---|---|
| length, structure, prose ↔ list, platform format | yes |
| verb strength, intensity, target of a statement | no |
| generalising private details about third parties | yes, this is the one asymmetry |
| correcting the author's typos | no, unless the author asks |

Typos are the same rule at small scale: roughness carries "a human wrote this", which is worth more than the tidiness it costs.

## Two boundaries, both load-bearing

**1. Platform rules govern publication, not meaning.** A network may refuse a formulation; it does not get a quietly edited version. On conflict: text unchanged, a human decides placement. A machine resolving the conflict by rewriting produces a forgery of the author's voice, in a form that is easy to deny and hard to detect.

**2. "Do not soften what was said" ≠ "author this on my behalf".** The rule protects an existing human statement. It does not commission the machine to originate hostility nobody uttered. Transmitting and authoring are different operations, and only the first is defensible under this rule.

**Pair to both:** text published under a human's name but written by the machine is labelled as such. Do not sanitise and do not impersonate are one principle at two points: the reader must know whose voice this is and how far it travelled from the mouth.

## Implementation notes

- gate runs on the final text, after all rewrites, comparing against the transcript for meaning-bearing deltas
- the gate is deterministic and cheap; it fails closed
- a gate that only ever fires in the direction that flatters the operator is a filter, not a gate: it must be able to block a publication that everyone wants to ship

## Open, not asserted

One commenter's observation, unverified by us: top models are themselves fairly politically correct, Grok excepted. We have not measured cross-vendor smoothing and will not assert it. But the observation points at the mechanism: if smoothing lives in model defaults rather than in anyone's instruction, then "I told it not to" is not a control. A gate you can test is.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/no-sanitizing-my-voice.md
Repository: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab.
