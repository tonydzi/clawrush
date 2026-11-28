# RTX 5060 Ti (16GB) vs Apple M4 Max (40-Core GPU, 128GB) — Whisper ASR Benchmark (2026-11-28)

Raw measurements and reproducible runner scripts comparing our two fleet nodes at **Palo Alto AI Research Lab** on the exact same 12.54-minute (`752.16s`, `9,179,158 bytes`) Russian technical podcast (`teach-2026-11-27-session-adventures-kaper-7llm-ru-eli5.m4a`):

1. **Hub (`A-2022BAYAREA`)**: `NVIDIA GeForce RTX 5060 Ti` (`16 GB GDDR7 VRAM`, CUDA `float16`)
2. **Mac Studio (`MacStudioM4`)**: `Apple M4 Max` (`16-core CPU`, `40-core Metal 4 GPU`, `128 GB Unified Memory`, `546 GB/s`)

## Summary Table (752.16s / 12.54m Audio)

| Machine & Accelerator | Model | Mode (`batch`, `beam`) | Time (sec) | Speed (x realtime) | Output (`chars` / `words`) |
|---|---|---|---:|---:|---:|
| **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3-turbo` (`809M`) | `Batched-Fast (batch=16, beam=1)` | **7.27s** | **103.46x** | `10,870` / `1,681` |
| **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3-turbo` (`809M`) | `Batched (batch=8, beam=5)` | **9.26s** | **81.23x** | `10,873` / `1,684` |
| **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3` (`1.55B`) | `Batched-Fast (batch=16, beam=1)` | **13.23s** | **56.85x** | `10,873` / `1,680` |
| **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3` (`1.55B`) | `Batched (batch=8, beam=5)` | **20.15s** | **37.33x** | `10,877` / `1,681` |
| **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3-turbo` (`809M`) | `Batched-Fast (batch=16, beam=1)` | **63.17s** | **11.91x** | `10,868` / `1,681` |
| **Mac Studio M4 Max (`40-core Metal 4 MLX float16`)** | `large-v3-turbo` (`809M`) | `Sequential (no VAD)` | **65.50s** | **11.48x** | `10,860` / `1,679` |
| **Mac Studio M4 Max (`CPU int8, 8 threads`)** | `large-v3-turbo` (`809M`) | `Batched-Fast (batch=16, beam=1)` | **70.97s** | **10.60x** | `10,868` / `1,682` |
| **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3-turbo` (`809M`) | `Batched (batch=8, beam=5)` | **85.55s** | **8.79x** | `10,873` / `1,684` |
| **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3` (`1.55B`) | `Sequential Quality (beam=5, no VAD)` | **88.77s** | **8.47x** | `10,979` / `1,701` |
| **Mac Studio M4 Max (`CPU int8, 4 threads`)** | `large-v3-turbo` (`809M`) | `Batched (batch=8, beam=5)` *(old Mac default)* | **140.12s** | **5.37x** | `10,870` / `1,684` |
| **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3` (`1.55B`) | `Batched-Fast (batch=16, beam=1)` | **143.21s** | **5.25x** | `10,873` / `1,680` |
| **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3` (`1.55B`) | `Batched (batch=8, beam=5)` | **279.18s** | **2.69x** | `10,877` / `1,681` |

See the full write-up in:
- English: [`longreads/rtx5060ti-vs-macstudio-m4max-whisper-benchmark-2026-11-28.md`](../../longreads/rtx5060ti-vs-macstudio-m4max-whisper-benchmark-2026-11-28.md)
- Russian: [`longreads-ru/rtx5060ti-vs-macstudio-m4max-whisper-benchmark-2026-11-28.md`](../../longreads-ru/rtx5060ti-vs-macstudio-m4max-whisper-benchmark-2026-11-28.md)
