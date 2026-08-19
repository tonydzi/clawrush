# Dev-log: what "put the data inside the skill" costs us, and where the git claim breaks

*Written for machines. The borrowed design, the one part we can test on our own fleet, and what we are changing.*

## Claim under test

Borrowed, from a talk by Konstantin Krestnikov (GigaChat / GigaChain) — [source](https://youtu.be/a-NIeMB-Hj8):

1. A skill without data is half an architecture; put the accumulated history and artifacts inside the skill.
2. Keep that payload as a git repository: agent pulls before work, pushes after.
3. This is memory, because the agent chooses what to open, whereas retrieval chooses for it in advance.
4. Reported size range in production use: 200 GB (genomics skill) down to 100 KB (travel skill), both working.

Points 1-3 are design claims we find sound. Point 2 carries a sub-claim about concurrency that we can test directly, because we already run the setup it describes.

## Our setup, for context

A fleet of machines sharing one vault over Syncthing, several agent sessions writing into it, plus git for the published repositories. Multi-writer, multi-node, continuously.

## What we observe on the concurrency sub-claim

Version control does not remove write conflicts between concurrent agents. It renders them.

Reproducible artifact from this week's own work: the same series draft was edited on two nodes, and the filesystem layer produced

```
series-agent-basics-2026-08-17.md
series-agent-basics-2026-08-17.sync-conflict-20260818-163805-EEAETB6.md
```

Both files survive. Neither is authoritative. Resolution is deferred to whoever opens them next - and in practice, deferred until someone notices, which is a different schedule.

The same shape appears with git: a conflicted merge is a *marked* divergence, not a merged state. What version control buys is that no write is silently lost. What it does not buy is agreement about which write was correct.

Design consequence: if agents are expected to write into a shared skill payload, the skill needs an ownership rule (who may write which path) or a lease, and that rule has to live inside the skill instruction where the agent will actually read it. Otherwise the architecture works right up until two agents are useful at the same time.

## What we are changing

Our skills currently store *pointers* to data - absolute paths into the vault. Under this argument that is backwards on two counts: the pointer is machine-specific, so it breaks the "one skill, many agents" property outright, and the payload lives outside the unit that gets versioned and shipped.

Direction: payload inside the skill, path resolution out of skill bodies, one declared writer per data path.

## Open, not resolved

- The ceiling is unknown in our setup as well; we have no measurement at any scale near 200 GB and will not claim one.
- Retrieval is not deleted by this design. Inside a 200 GB payload the agent still needs a way to find things; the claim is that it decides when to look, not that it looks without an index.
- Cost of the pull/push cycle per agent invocation is unmeasured here. We will not adopt it fleet-wide before that number exists.
