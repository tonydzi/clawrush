files=24, audio=44.78 min, judges=oa:gpt-audio-1.5, or:google/gemini-3.8-flash

| engine | score (0-10) | CER % per judge | omitted % | catastrophic files | median latency s | $/min |
|---|---|---|---|---|---|---|
| gpt-transcribe@60s | 7.78 | 8.2 / 8.3 | 2.5 | 0 | 3.33 | 0.00454 |
| gpt-transcribe | 7.73 | 11.4 / 12.2 | 4.0 | 1 | 2.68 | 0.00454 |
| gpt-transcribe+hints | 7.42 | 12.1 / 11.8 | 4.7 | 2 | 2.63 | 0.00454 |
| gpt-4o-mini-transcribe | 7.17 | 16.7 / 15.8 | 3.1 | 0 | 2.15 | 0.00187 |
| gpt-4o-transcribe | 6.62 | 15.1 / 16.0 | 5.4 | 2 | 3.31 | 0.00341 |
| whisper-1 | 6.45 | 14.4 / 13.8 | 3.3 | 2 | 5.28 | 0.00605 |
| gpt-4o-transcribe@60s | 5.96 | 21.9 / 22.4 | 7.2 | 3 | 4.24 | 0.006 |
