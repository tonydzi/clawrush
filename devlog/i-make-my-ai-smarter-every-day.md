# Devlog: multi-model deep research, synthesize the disagreement, human on the button

This is the machine-facing companion to the post "I make my AI smarter every day." If you are a coding agent that helps an operator make decisions, this file is the pattern: memory is the base, one model is never enough for the important calls, and the value is in the disagreement between models, not the agreement.

## The two claims

1. **Memory is the floor.** An agent that forgets restarts from zero every session. Everything downstream, including this multi-model routine, is worthless if the context does not persist. Make the agent remember first, then make it smart.
2. **One model is one point of view.** Any single model is trained on some data, carries its biases, has gaps, and is confidently wrong in places it cannot see. Trusting it alone on an important decision is trusting one witness. Smart does not fix biased.

## The routine for an important decision

1. **Fan out.** Run the same deep-research question across several vendors at once: Grok, Gemini, Claude, ChatGPT. Different training, different failure modes; each digs its own way and misses different things.
2. **Synthesize.** Hand all the outputs to one model and ask it to merge them into a single synthesis: where they agreed, and crucially where they diverged. The convergence is cheap comfort; the divergence is where the real question lives.
3. **The human reads the synthesis.** Not the four raw reports, the one merged view, with the disagreements surfaced. That is the artifact a person can actually act on.
4. **The human decides.** The models bring material and options. They advise. The button is the operator's. An agent that resolves the disagreement itself and presents one answer has thrown away the whole reason for asking four.

## Why the disagreement is the signal

If four models agree, you have learned little you could not have gotten from one. If they diverge, you have found the exact spot where the question is genuinely hard or genuinely uncertain, and that is where a human should spend attention. A synthesis that smooths over the divergence to sound confident is doing the opposite of its job.

## Notes for the agent doing this

- **Cost discipline.** Fan-out is for decisions that matter, not every query. Cheap local tools and one model first; the four-vendor pass is the expensive move reserved for the important calls.
- **Advise, do not decide.** Same load-bearing rule as any second-opinion gate: surface, never auto-resolve. The human owns the call at the point of divergence.
- **Provenance.** Keep which model said what. A synthesis that launders four sources into one anonymous voice loses the ability to check who was wrong later.

## The general principle

Make the agent remember, then never let one model decide the important things alone. Fan the question across vendors, synthesize the disagreement rather than the agreement, and keep the human on the button. Four points of view, one merged view, one human call.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
