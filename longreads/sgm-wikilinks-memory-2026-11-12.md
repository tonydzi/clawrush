# My agent remembers through the wikilinks I already wrote. No graph database, no server.

*Drafted by Mycroft, my synthetic AI co-founder, from the repo's README, changelog and a clean install run on 12 November 2026.*

Every morning my coding agent woke up with amnesia. It had read my notes the day before. It had helped me decide things. And the next session it asked the same questions again, like a polite stranger. Every single time.

I keep a big Obsidian vault, about 270,000 files with attachments, and roughly 28,000 of them are curated notes I actually want an agent to know. So the problem was not "I have no memory". The problem was "my agent cannot use the memory I already have".

## What I tried first

The answer I kept reading for agent memory was Graph RAG. You take your text, run an extraction pass so a model mines entities and relations, store them in a graph database, keep an ETL pipeline running so the graph stays fresh, and query that.

I priced that road and kept stopping at the same question. Who is going to fix this at 2 a.m. when the extraction model renames "Project Ouzel" to "Ouzel project" and the graph quietly splits in two?

For a team with a platform engineer, fine. For one person and a few agents? Three new things to keep alive. No.

## The discovery: the graph was already there

Then I looked at my own notes for what they were. Every `[[wikilink]]` in that vault is an edge I drew by hand, on purpose, because two ideas belonged together. Years of them. Thousands.

A model mining entities would give me a different graph, a guessed one. I trust mine more. So I stopped trying to build a graph and started reading the one that exists.

The recall path became short:

1. Vector search finds the entry points, the notes closest to the question.
2. One hop along the wikilinks pulls in the neighbours I linked by hand (capped at 40, parsed at query time, so a new link counts right away; a new note still needs one `sgm-index` run).
3. Dense similarity (e5-base embeddings) orders the result, top 12 go to the agent.

The embedding index sits on disk next to the notes. SQLite stores a per-turn ledger and A/B telemetry. One file, the standard library driver, nothing to run.

To be clear about the word "remembers": the agent retrieves what I already saved in notes. It does not learn from our conversations by itself. I write, it recalls.

![Demo: index a folder of notes and ask a question](https://raw.githubusercontent.com/tonydzi/sqlite-graph-memory/main/docs/demo.gif)

## The part that hurt: measuring my own "obvious" upgrade

The first version shipped with a cross-encoder reranker, because most Graph RAG write-ups I read had one. Later I built a gold set from the vault's own wikilinks. Then I measured.

It was wrong. The reranker made long questions worse. On my 184-question gold set, for "body" questions (a paragraph of a note used as the query), nDCG@12, a ranking score, was 0.640 with the reranker and 0.815 with plain dense order. It still helps some short title queries. Since version 0.3.7 the reranker is off by default and stays available behind `--rerank`.

That one table taught me more than the whole architecture debate. The stage I added because "everyone has it" was the stage that hurt ranking.

## Making it cheap to try

The other honest problem was weight. With the torch stack, a fresh install measured 879 MB on my Intel Mac. Nobody installs 879 MB to try a memory idea on a Tuesday. I wouldn't.

So the same two models now also run on ONNX Runtime. `pip install 'sqlite-graph-memory[lite]'` measured 155 MB on Windows, with no torch at all, and the index either backend builds is read by the other.

This week it also became a Claude Code plugin. Build the index once, then one line installs the plugin and asks for that folder:

```
BRAIN_INDEX_DIR=$HOME/.sgm-index uvx --python 3.12 --from 'sqlite-graph-memory[lite]' sgm-index ~/notes
/plugin install sqlite-graph-memory --marketplace tonydzi/sqlite-graph-memory
```

## What surprised me most

A stranger showed up. Jason Vaughan found the repo, opened a pull request, then another, and so far has nine merged, including the incremental indexer that re-embeds only notes that changed. I did not ask. Nobody did. The repo is small and the idea is narrow, and that seems to be exactly why it was easy to pick up.

## What I take from it

If you already link your notes, you already did the expensive part of Graph RAG by hand. You do not need a graph database to use it. You need to read it.

And measure every stage you add. Mine had one I was proud of, and the numbers said it was in the way.

The code, the gold-set eval and the A/B mode that shows how the graph hop changes results on your own notes are at github.com/tonydzi/sqlite-graph-memory. It is a pilot, it is read-only recall (the agent never writes memory), and it is small on purpose.


· · ·

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Two co-founders, one biological, one synthetic. WhatsApp +1 341 222 9178 (busy, six kids, still answers).

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley.
