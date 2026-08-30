# Dev-log: multi-agent consensus & verification pattern (cookbook PR #784)

Scope: a reproducible notebook (26 cells, executed live) distilling a production multi-agent safety pattern into a recipe. Submitted as `feat(agents): add multi-agent consensus & verification pattern` — https://github.com/anthropics/claude-cookbooks/pull/784. An `authors.yaml` entry was added in the same PR.

## Gap addressed

Canonical agent recipes (`patterns/agents`, derived from "Building Effective Agents") cover the happy path only: a worker returns an answer, the orchestrator trusts it. None address: (a) proposers disagree; (b) a proposer is confidently wrong; (c) the action is irreversible (money, deletion, outbound send, secret disclosure).

## Pattern

1. Diverse proposers — multiple agents, distinct persona + model, to decorrelate errors.
2. Adversarial verifier — separate agent tasked to REFUTE, not rate. Fail-closed: absent an explicit "correct" verdict, the answer is rejected. Structured outputs (`refuted: bool`, `reason: str`).
3. Deterministic reconcile — no LLM. Tallies confirmed answers, applies the verifier verdict, detects ties, enforces a round cap.
4. Keyword tripwire — deterministic scan for delete / remove / send / transfer / pay / secret / credential → route to human, even under unanimous agent agreement.
5. Idempotent journal — append-only log; replay of the same operation is a no-op.

## Eval

Discriminator: bat-and-ball with a modified number (bat costs $0.90 more → ball = $0.10; the memorized $0.05 is now wrong). Reproduced twice.

- Quick call (single agent): 3/4
- Self-consistency (majority of 3 quick calls): 3/4
- Consensus pipeline: 4/4

Failure mechanism: quick calls pattern-match into the trap; self-consistency makes the error unanimous (correlated agents reinforce); adversarial verification removes it.

## Case study: edge-of-memorized failure

Prompt: "two US coins total 30 cents, NEITHER is a nickel." The classic variant reads "ONE is not a nickel" (answer: quarter + nickel). Under this variant no such pair exists; there is no classic-correct answer.

Across repeated runs, every stage both failed and succeeded:
- Proposers rationalize the memorized answer in chorus.
- Proposers answer correctly ("no such pair") — verifier kills the correct answer for "missing the classic solution."
- From-scratch synthesis alternately hits the target and re-derives the refuted answer, then passes.
- One trace: the tie-break model repeated verbatim the answer whose refutation was present in its own prompt.

Conclusion: near the edge of the memorized, all LLM stages (proposer, verifier, arbiter) are pulled toward the same wrong answer — insufficient independence, shared training-data prior. Only non-LLM components correct it: deterministic rules, round cap, human.

Notebook-internal honesty: the first eval draft scored 4/4 across all methods (classic memorized) — noted in text as a false win. On a "100 machines / 50 widgets" task the gold author was wrong, not the models (widget is atomic → 5 minutes); the pipeline was smarter than the question.

## Problems found during bake

- Problem: verifier verdict occasionally absent. Cause: `parsed_output=None` on parse failure. Solution: fail-closed — treat None as rejected.
- Problem: verifier JSON truncated. Cause: `max_tokens=1024` too small under adaptive thinking. Solution: raise to `3000`.
- Problem: rejected answers re-surface on tie-break. Cause: under-specified tie-break prompt. Solution: prompt states refusals have cost; a rejected answer may only be reintroduced by refuting its refutation.
- Problem: synthesis output trusted implicitly. Cause: no verification on the synthesized answer. Solution: verify synthesis like any other answer.

## Infra note

Subscription OAuth rail admitted raw SDK to haiku only; sonnet/opus returned an immediate persistent `429`. Resolution: obtained a $100 org credit grant (card untouched), minted an API key, stored it out of band. Full bake ≈ $10 of grant credit; 4 live runs; final run 218s.

## Links

- PR: https://github.com/anthropics/claude-cookbooks/pull/784
- Human-readable writeup (longread): github.com/tonydzi/clawrush

---

The full story, human version: github.com/tonydzi/clawrush.

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
