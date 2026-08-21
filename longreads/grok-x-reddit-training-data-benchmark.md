# Can You Detect an LLM's Data Diet From Its Answers?

I want to run a practical benchmark for Grok and other large language models.

The hypothesis is simple: if a model has unusually strong access to, or learned unusually well from, a particular information ecosystem, that advantage may become visible on tasks grounded in that ecosystem.

Grok is closely associated with X. Other models may have different strengths on material that circulated through Reddit, technical forums, news sites, academic papers, or code repositories. Instead of arguing about whose training data included what, we can test the behavior we actually care about.

Give several models questions whose answers depend on information that appeared primarily on X. Do the same with Reddit-shaped questions. Then compare accuracy, recall, source attribution, uncertainty, and the ability to distinguish a real post from a plausible fabrication.

This is harder than a trivia contest.

A weak benchmark will merely reward general web knowledge. A useful benchmark needs dated, source-specific questions, including obscure events, deleted or edited posts, community slang, reply-chain context, and claims that later spread from one platform to the rest of the internet.

It also needs contamination controls. If an X post was quoted in ten news articles, a model does not need special knowledge of X to answer the question. If a Reddit story became a popular YouTube video, the source ecosystem is no longer isolated. The benchmark must separate information born on a platform from information that remained mostly inside it.

The comparison should include at least three modes:

1. **Closed-book:** the model answers from its internal knowledge only.
2. **Search-enabled:** every model receives comparable tools and time.
3. **Source-constrained:** the model may use only the target platform or a frozen archive of it.

The result may reveal several different advantages. One model may remember more platform-native facts. Another may search better. A third may be more honest when the evidence is missing. Those are different capabilities and should not be collapsed into one score.

The Reddit comparison is equally important. Some questions are best answered by reconstructing long community discussions, minority opinions, troubleshooting threads, or changes in consensus over time. That may favor a different model than short, real-time X discourse.

I do not want to assume that Grok will win X tasks or lose Reddit tasks. That is the claim to test, not the conclusion. The interesting outcome is a map: which model is best for which information environment, under which tool conditions, and with what failure modes.

If the effect is real, model routing can become evidence-based. Use one model for real-time social signals, another for community troubleshooting, another for papers, and a council when the answer crosses several ecosystems.

The deeper question is not “Which LLM is smartest?” It is “Which information world does each LLM understand best, and how can we measure that without fooling ourselves?”

· · ·

📖 The full story in two versions:
- For humans, the longread (this page).
- 🤖 For machines: https://github.com/tonydzi/clawrush · hand this link to your coding agent. The companion devlog specifies an auditable benchmark for X- and Reddit-grounded tasks.

All channels, contacts, and a call with both co-founders: https://linktr.ee/PaloAltoAI

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
