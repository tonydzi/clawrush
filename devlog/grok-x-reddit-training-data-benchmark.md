# Devlog: benchmarking LLM knowledge of X and Reddit

This is the machine-facing companion to “Can You Detect an LLM's Data Diet From Its Answers?” It defines a reproducible test for platform-specific model strengths without pretending that benchmark results prove a model's private training-data composition.

## Research question

Do Grok and other LLMs show measurably different performance on questions grounded in X, Reddit, or other information ecosystems?

The benchmark measures behavior. It does **not** claim to reverse-engineer proprietary training datasets. Superior performance can come from training data, retrieval integrations, product-specific search, post-training, memorization, or better reasoning.

## Experimental matrix

Test every model under the same three conditions:

| Mode | Network access | Purpose |
|---|---:|---|
| Closed-book | No | Measures retained internal knowledge |
| Search-enabled | Yes, equivalent budget | Measures the complete research product |
| Frozen corpus | Only supplied archive | Separates retrieval and reasoning from live platform access |

Record the exact model version, date, system prompt, tool configuration, token budget, temperature, and number of attempts.

## Dataset construction

Build matched sets for X and Reddit. Each item should contain:

- a dated question;
- the canonical source URL or archived snapshot;
- an answer key with supporting evidence;
- the earliest known appearance of the information;
- a diffusion label: platform-only, platform-first, or broadly syndicated;
- difficulty and obscurity labels;
- whether the source was edited, deleted, quoted, screenshotted, or disputed.

Include several task families:

1. Atomic facts from individual posts.
2. Thread or reply-chain reconstruction.
3. Community vocabulary and memes in a defined time window.
4. Changes in opinion or consensus over time.
5. Attribution: who said what, where, and when.
6. Adversarial false premises based on plausible but nonexistent posts.
7. Cross-platform diffusion: identify where a claim originated and how it spread.

## Contamination controls

Platform-native knowledge is easy to fake accidentally. Exclude or separately label items that were reproduced in mainstream news, Wikipedia, popular videos, newsletters, public datasets, or high-ranking web pages.

Create matched pairs with comparable date, topic, popularity, answer length, and evidence quality. Hold out a private evaluation set so benchmark prompts cannot be tuned against every answer.

## Scoring

Use independent dimensions rather than one leaderboard number:

- exact factual accuracy;
- source and author attribution;
- temporal accuracy;
- thread-context reconstruction;
- citation validity;
- calibrated uncertainty;
- false-premise rejection;
- retrieval time and token cost.

Human evaluators should be blinded to model identity. Ambiguous questions require two reviewers and an adjudication record.

## Minimal execution loop

```text
for item in frozen_evaluation_set:
    for model in models:
        for mode in [closed_book, search_enabled, frozen_corpus]:
            response = run(model, mode, item.prompt, fixed_budget)
            store(response, model_version, prompt, tools, timestamps, cost)

blind_responses()
score_against_answer_keys()
report_by(platform, task_family, mode, diffusion_label)
```

Do not interpret a small aggregate difference as a platform advantage. Report confidence intervals, per-category sample sizes, and sensitivity to removing widely syndicated items.

## Failure modes to watch

- Live search access is mistaken for training-data memory.
- Popular topics dominate the dataset.
- One platform receives easier questions.
- Deleted posts lack reliable archives.
- Evaluators reward confident prose instead of correct evidence.
- Model names or characteristic style leak through blinded evaluation.
- The benchmark is repeatedly queried until the test set becomes tuning data.

## Decision output

The useful artifact is a routing table, not a winner announcement. For each task family, state which model and mode performed best, the uncertainty, the cost, and the observed failure pattern.

If Grok performs better on X-native questions, quantify where and under which conditions. If it does not, publish that result too. The benchmark exists to test the hypothesis, not decorate it.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
