`Benchmarking LLM Gateways in a Multi-Agent Fleet: 216 Live Calls on llmapi.ai vs OpenRouter (and One Proxy Edge-Case)`

```markdown
# Benchmarking LLM Gateways in a Multi-Agent Fleet: 216 Live Calls on llmapi.ai vs OpenRouter

When you run a multi-agent engineering harness that fans out code reviews and verification checks across 5 to 6 frontier models simultaneously, your tail latency is dictated by the slowest gateway route-and a single upstream 402/429/5xx can stall an entire review quorum.

After meeting the **LLM API (`llmapi.ai`)** engineering team at Web Summit in Lisbon, we ran a controlled 216-call live benchmark (`144` paired calls + `72` parameter-ablation repeats) pitting `llmapi.ai` against `OpenRouter` across `gpt-6.1-terra` and `claude-sonnet-5`, followed by two live 6-model code-review panels.

## 1. Benchmark Setup
- **Workload:** 12 deterministic verification tasks × 3 runs per model/gateway pair (`36` calls per cell, `216` total API calls across two waves), plus two 6-model production code review panels.
- **Metrics:** Strict exact-match pass rate, median Time-To-First-Token (TTFT), median total completion latency, and billed cost per 36 calls.

## 2. Results

| Model | Gateway | Pass Rate | Median TTFT | Median Total Latency | Cost / 36 Calls |
|---|---|---|---|---|---|
| `gpt-6.1-terra` (no `temperature`) | **llmapi.ai** | **36 / 36** | **0.91 s** | **0.96 s** | **$0.0036** |
| `gpt-6.1-terra` (no `temperature`) | OpenRouter | 36 / 36 | 2.50 s | 2.71 s | $0.0038 |
| `claude-sonnet-5` | **llmapi.ai** | **23 / 36** | 2.37 s | 2.69 s | **$0.0115** |
| `claude-sonnet-5` | OpenRouter | 23 / 36 | **1.24 s** | **1.51 s** | $0.0132 |

## 3. Three Engineering Takeaways for Multi-Agent Builders

1. **2.75x Faster TTFT on OpenAI `gpt-6.1-terra`:** On `gpt-6.1-terra`, `llmapi.ai` delivered a **0.91s median TTFT** (0.96s total) compared to **2.50s** (2.71s total) on OpenRouter, with 36/36 accuracy on both.
2. **The `temperature: 0` Proxy Edge-Case:** In Wave 1 (`144` calls), our runner passed `temperature: 0` to all models. OpenRouter silently stripped `temperature` before forwarding to OpenAI's `gpt-6.1-terra` endpoint, whereas `llmapi.ai` forwarded `temperature: 0` verbatim-causing upstream OpenAI to reject 36/36 calls with `HTTP 400`. Once we stripped `temperature` for `terra` (`Wave 2`, 72 calls), `llmapi.ai` went 36/36 at 0.91s TTFT. If you are building or migrating to an OpenAI-compatible proxy, normalize model-specific unsupported parameters (`temperature`, `top_p`) at the gateway edge.
3. **Dual-Gateway Quorum Architecture:** Because `llmapi.ai` leads on `gpt-6.1-terra` latency and cost (-13% on `claude-sonnet-5`) while OpenRouter has lower latency on `claude-sonnet-5`, we promoted `llmapi.ai` to primary provider in our multi-LLM review runner with automatic failover on `HTTP 402/429/5xx`. Across two live 6-model review panels, `llmapi.ai` served 6/6 slots with zero drops ($0.052 total).

*We are hosting an upcoming **Palo Alto AI Research Lab ONLINE Meetup** featuring 5-15 minute lightning talks from AI infrastructure and multi-agent engineers. Want to share a live benchmark or architecture demo? Reach out to grab a 10-minute slot.*
```
