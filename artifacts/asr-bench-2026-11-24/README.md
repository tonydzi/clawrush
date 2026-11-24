# ASR bench, 2026-11-24: gpt-transcribe vs gpt-4o-transcribe vs whisper-1

Companion code and aggregate results for the longread: https://github.com/tonydzi/clawrush/blob/main/longreads/gpt-transcribe-vs-gpt-4o-transcribe-2026-11-24.md

- 24 real voice notes (one speaker, Russian with English tech terms), 44.78 min. Audio and transcripts are private and NOT included.
- `bench.py <audio_dir> [engines]`: sends each `<id>.ogg` listed in `<audio_dir>/meta.json` (`[{"id":..,"dur":..}]`) to each engine, appends to `runs.jsonl`. Needs `OPENAI_API_KEY`, optional `OPENROUTER_API_KEY`, `FFMPEG` for chunked variants.
- `judge.py <judge> <audio_dir> [ffmpeg]`: blind audio judge, e.g. `oa:gpt-audio-1.5` or `or:google/gemini-3.8-flash`. Candidates are shuffled and anonymised per file.
- `analyze.py`: zero-LLM summary into `results.json` / `results.md`. `cer_vs_refs.py`: CER of any engine run against the existing judge references (used for 30 s / 120 s chunk sizes).
- `paired.txt`: paired score differences with bootstrap CI (note: 48 judge-file pairs; file-level n=24 gives +0.74..+1.57 for gpt-transcribe@60s vs gpt-4o-transcribe).

Limitations: no human reference; references are written by LLM judges who saw the candidates; judges agree moderately (Pearson 0.567).
