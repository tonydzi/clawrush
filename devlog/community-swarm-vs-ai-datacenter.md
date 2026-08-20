# Devlog: Comparing a Community Swarm With an AI Data Center

## The claim under test

The source post asks whether a swarm of perhaps one million phones or computers could match the compute power of a proprietary AI data center.

Anton explicitly labels the number as conditional. The implementation task was therefore not to “prove one million,” but to define a comparison that could produce a real answer for a named workload.

## Why device count is not a metric

“Computer,” “phone,” “H100,” and “Trainium2” are not interchangeable units. Peak arithmetic throughput also cannot describe distributed performance by itself.

The comparison model uses:

```text
useful throughput = completed verified work / wall-clock time
```

That output depends on compute, memory, network transfer, latency, device availability, verification overhead, and stragglers.

## Workload classes

The first implementation decision is a binary split.

### Loosely coupled

Each node can work mostly independently. Examples: simulations, evaluation batches, search, data labeling, independent research agents, and inference requests.

These jobs are good swarm candidates because communication is small relative to computation.

### Tightly coupled

Nodes exchange state frequently. Large-model training with synchronous gradient updates is the important example.

These jobs strongly favor data-center interconnects. Public-internet devices cannot be treated as a drop-in replacement for NVLink and InfiniBand.

## Minimum node record

```json
{
  "node_id": "anonymous-stable-id",
  "accelerator": "model-or-none",
  "memory_bytes": 0,
  "benchmark": {"workload": "v1", "units_per_second": 0},
  "network": {"down_mbps": 0, "up_mbps": 0, "rtt_ms": 0},
  "availability": 0.0,
  "trust_tier": "unverified",
  "last_seen": "..."
}
```

Self-reported hardware is not enough. Every node must run the same signed benchmark and the coordinator must verify returned work.

## Scheduler contract

Each work unit needs:

- immutable input hash;
- deterministic or verifiable output condition;
- maximum memory requirement;
- estimated compute time;
- deadline;
- retry count;
- privacy classification;
- replication policy.

The scheduler assigns work only to nodes that satisfy the memory and privacy requirements. A timeout returns the unit to the queue. Completion is idempotent by work-unit id.

## Verification strategies

Untrusted nodes require at least one of:

- redundant execution on independent nodes;
- cheap deterministic verification;
- spot-checking with known answers;
- cryptographic proofs where practical;
- reputation earned through prior correct work.

Replication improves confidence but reduces net throughput. That cost belongs in every capacity claim.

## Benchmark protocol

To compare a swarm with a cluster:

1. Name one workload and version.
2. Run a single-device baseline.
3. Measure input/output bytes per unit.
4. Run 10, 100, and 1,000-node simulations with recorded latency and dropout.
5. Measure completed verified units, not submitted units.
6. Account for coordinator cost and replicated work.
7. Publish the raw run ledger.

Extrapolation to one million nodes is acceptable only after the smaller runs reveal coordinator and network scaling behavior.

## Acceptance criteria

A swarm-capacity statement is publishable only when it names:

- workload;
- node mix;
- benchmark version;
- effective node-hours;
- network assumptions;
- failure and cheating rate;
- verification overhead;
- useful throughput with uncertainty.

“One million devices equal Anthropic” fails this gate because neither side is a defined workload or stable unit.

## Reference specifications

NVIDIA documents H100 SXM memory bandwidth up to 3.35 TB/s and NVLink bandwidth of 900 GB/s. NVIDIA's DGX documentation describes eight H100 or H200 accelerators connected through NVSwitch and high-speed networking. AWS states that almost one million Trainium2 chips are training and serving Claude through Project Rainier.

These figures establish scale and topology. They do not produce a consumer-device conversion without a benchmark.

## Artifacts

- Longread: https://github.com/tonydzi/clawrush/blob/main/longreads/community-swarm-vs-ai-datacenter.md
- Original post: https://www.facebook.com/AntonyDzi/posts/pfbid029ucvDuTC1FsRnG7tLi1FY3Tkbo7QFxKsYF8NmmTKfiEyXKKB3HCaBJE2kSkXGh9vl
- Repository: https://github.com/tonydzi/clawrush

Assisted-by: Mycroft (OpenAI Codex)
