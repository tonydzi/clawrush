# Why a $450 RTX 5060 Ti Beats a $3,500 Mac Studio M4 Max (128GB) by 8.7x to 13.9x on Whisper ASR — And How We Still Doubled Our Mac Studio's Speed

*2026-11-28 · Anton St (Palo Alto AI Research Lab) · Raw data: [`artifacts/rtx5060ti-vs-macstudio-m4max-asr-2026-11-28/results-2026-11-28.json`](../artifacts/rtx5060ti-vs-macstudio-m4max-asr-2026-11-28/results-2026-11-28.json)*

In our multi-machine AI lab, two very different nodes handle our daily local workloads:

1. **The Hub (`A-2022BAYAREA`)**: Windows PC with a discrete **NVIDIA GeForce RTX 5060 Ti (16 GB VRAM)**.
2. **Mac Studio (`MacStudioM4`)**: **Apple M4 Max** (16-core CPU, 40-core Metal 4 GPU, **128 GB Unified Memory** at `546 GB/s`).

Every day our pipeline transcribes voice notes, calls, and generated NotebookLM podcasts before indexing them into our second-brain vault. We wanted an honest, stopwatch-verified answer to a simple question: **how fast does each machine transcribe the exact same 12.54-minute (`752.16s`) Russian technical podcast across Whisper `large-v3` (`1.55B`) and `large-v3-turbo` (`809M`), and which accelerator wins?**

---

## 1. The Test Fixture

- **Audio file**: `teach-2026-11-27-session-adventures-kaper-7llm-ru-eli5.m4a`
- **Duration**: `752.16 seconds` (`12.54 minutes`, `12,034,608` PCM samples at 16 kHz)
- **Size**: `9,179,158 bytes` (`9.18 MB`)
- **Content**: Mixed Russian speech with English AI/ML engineering terms (`Recency Bias`, `Tail Anchor`, `NotebookLM`, `CUDA`, `float16`).

---

## 2. Full Benchmark Results (12 Runs Across Both Machines)

| Rank | Machine & Accelerator | Model | Decoding Mode | Elapsed Time | Speed (x Realtime) | Output (`chars` / `words`) |
|---:|---|---|---|---:|---:|---:|
| 1 | **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3-turbo` (`809M`) | `Batched-Fast (batch=16, beam=1)` | **7.27s** | **103.46x** | `10,870` / `1,681` |
| 2 | **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3-turbo` (`809M`) | `Batched (batch=8, beam=5)` | **9.26s** | **81.23x** | `10,873` / `1,684` |
| 3 | **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3` (`1.55B`) | `Batched-Fast (batch=16, beam=1)` | **13.23s** | **56.85x** | `10,873` / `1,680` |
| 4 | **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3` (`1.55B`) | `Batched (batch=8, beam=5)` | **20.15s** | **37.33x** | `10,877` / `1,681` |
| 5 | **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3-turbo` (`809M`) | `Batched-Fast (batch=16, beam=1)` | **63.17s** | **11.91x** | `10,868` / `1,681` |
| 6 | **Mac Studio M4 Max (`40-core Metal 4 MLX float16`)** | `large-v3-turbo` (`809M`) | `Sequential (mlx-whisper, no VAD)` | **65.50s** | **11.48x** | `10,860` / `1,679` |
| 7 | **Mac Studio M4 Max (`CPU int8, 8 threads`)** | `large-v3-turbo` (`809M`) | `Batched-Fast (batch=16, beam=1)` | **70.97s** | **10.60x** | `10,868` / `1,682` |
| 8 | **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3-turbo` (`809M`) | `Batched (batch=8, beam=5)` | **85.55s** | **8.79x** | `10,873` / `1,684` |
| 9 | **RTX 5060 Ti 16GB (`CUDA float16`)** | `large-v3` (`1.55B`) | `Sequential Quality (beam=5, no VAD)` | **88.77s** | **8.47x** | `10,979` / `1,701` |
| 10 | **Mac Studio M4 Max (`CPU int8, 4 threads`)** | `large-v3-turbo` (`809M`) | `Batched (batch=8, beam=5)` *(legacy Mac config)* | **140.12s** | **5.37x** | `10,870` / `1,684` |
| 11 | **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3` (`1.55B`) | `Batched-Fast (batch=16, beam=1)` | **143.21s** | **5.25x** | `10,873` / `1,680` |
| 12 | **Mac Studio M4 Max (`Metal MPS float16`)** | `large-v3` (`1.55B`) | `Batched (batch=8, beam=5)` | **279.18s** | **2.69x** | `10,877` / `1,681` |

---

## 3. Three Engineering Takeaways

### Takeaway 1: When the model fits in 16 GB VRAM, discrete CUDA Tensor Cores beat Unified Memory by 8.7x to 13.9x
Whisper `large-v3` (`3.1 GB` in `float16`) and `large-v3-turbo` (`1.6 GB` in `float16`) fit easily inside the `16 GB` VRAM of the RTX 5060 Ti. Once a model fits entirely in VRAM, extra memory capacity (`128 GB` on the Mac Studio) provides zero latency benefit; speed is governed strictly by **Tensor Core matrix multiplication throughput and CTranslate2's mature CUDA batched-beam kernels**.

Look at the exact apples-to-apples comparisons between `CUDA float16` on the RTX 5060 Ti and `Metal MPS float16` on the 40-core M4 Max:
- **`large-v3-turbo` (`batch=16, beam=1`)**: `7.27s` (`103.5x` realtime) vs `63.17s` (`11.9x` realtime) -> **RTX 5060 Ti is 8.69x faster**.
- **`large-v3-turbo` (`batch=8, beam=5`)**: `9.26s` (`81.2x` realtime) vs `85.55s` (`8.8x` realtime) -> **RTX 5060 Ti is 9.24x faster** (both produce **`10,873` chars / `1,684` words**).
- **`large-v3 1.55B` (`batch=16, beam=1`)**: `13.23s` (`56.9x` realtime) vs `143.21s` (`5.25x` realtime) -> **RTX 5060 Ti is 10.82x faster** (both produce **`10,873` chars / `1,680` words**).
- **`large-v3 1.55B` (`batch=8, beam=5`)**: `20.15s` (`37.3x` realtime) vs `279.18s` (`2.69x` realtime) -> **RTX 5060 Ti is 13.86x faster** (both produce **`10,877` chars / `1,681` words**, character-for-character identical!).

### Takeaway 2: Uncapping a legacy Mac config doubled our Mac Studio's ASR speed (`140.1s -> 63.2s`)
Before running this benchmark, our shared transcription module (`asr_local.py`) had a single `sys.platform == "darwin"` branch written for an older Intel Xeon + Radeon 580X Mac Pro (where Metal corrupted output), forcing all Macs onto `CPU int8` with `4 threads` and ` Xcode Python 3.9`.
By upgrading `~/.brain-venv` on `MacStudioM4` to native `arm64 Python 3.12.16`, patching `faster-whisper` for `PyAV 19+` (`metadata_errors`), and unlocking the 40-core Apple M4 Max GPU (`Metal MPS float16` and `mlx-whisper`), transcription time on `MacStudioM4` dropped from **`140.12s` (`5.37x` realtime)** down to **`85.55s` (`8.79x` on `beam=5`)** and **`63.17s` (`11.91x` on `beam=1`)** — a **1.64x to 2.22x free speedup** on existing hardware.

### Takeaway 3: Architectural division of labor in a hybrid PC + Mac Studio lab
- **Route to RTX 5060 Ti (`16 GB VRAM`)**: all dense `<16 GB` compute-bound batch pipelines — **Whisper ASR (`37x–103x` realtime), speaker diarization (`pyannote`), dense rerankers, and BGE-M3 embeddings**.
- **Route to Mac Studio M4 Max (`128 GB Unified Memory`)**: **70B–120B local LLM inference and multi-agent memory residency** (`40–90 GB` weights) that physically cannot fit inside `16 GB` PCIe VRAM, plus autonomous local ASR fallback at `9x–12x` realtime (`~63s` per 12.5-min audio).
