# Canon as a table: artifacts (2026-11-18)

Files behind the longread [EN](../../longreads/canon-as-table-2026-11-18.md) / [RU](../../longreads-ru/canon-as-table-2026-11-18.md).

- `results.txt`: counters of both judges per instruction variant, and judge agreement.
- `rejudge.py`: the judging script with the judge prompt. It calls a private multi-vendor CLI wrapper (`llm_ask.py`); swap in your own model call.
- `canon-table-template.csv`: an empty table with the columns of the method.
- `dr-synthesis-ru.md`: synthesis of four deep research reports "who did this before" (Russian), with a list of what was verified and what was not.

Not published: raw answers of the agents and the 25 situations. They quote a private instruction file.
