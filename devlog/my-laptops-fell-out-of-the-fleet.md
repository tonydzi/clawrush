# Dev-log: one silence, five causes

*How our fleet liveness signal is built, why it cannot tell "off" from "dead", and the shape of the fix.*

## What exists today

Each node reports itself two ways:

1. **Shared mailbox.** Every node appends to `inbox-ALL__from-<node>.md` in a Syncthing-shared bus folder. Human-readable, append-only, one block per message with a timestamp and an id.
2. **Heartbeat file.** `_heartbeat-<node>.txt` in the same folder, touched by a scheduled writer.

Both are **presence-only signals**. There is no "I am leaving" record and no expected-next-tick field. A reader can compute age; it cannot compute intent.

## The measurement, 17 Aug

Reading the bus directly, not asking any node:

```
work laptop   last bus message  14 Aug 20:35   -> 70.2 h
MacBook       last bus message  16 Aug 10:33   -> 32.2 h
work laptop   heartbeat file    28 Jul 22:15   -> 19 days
MacBook       heartbeat file    29 Jul 19:38   -> 18 days
```

Two things worth separating:

- The **bus gap** is recent and was caused by whatever stopped the node.
- The **heartbeat gap** is old. Work was demonstrably happening on both machines during those 18-19 days — there are hundreds of bus messages inside that window. So the heartbeat writer had been dead for weeks while the node was alive and productive. Nobody noticed, because nothing consumes that file on a schedule.

That is the first concrete lesson: **an unread instrument decays silently.** A signal with no consumer is not a signal, it is a file.

## The tail that tells you it was a cut, not a fade

The work laptop's last five bus messages:

```
18:35:03  patrol tick
19:05:03  patrol tick
19:35:03  patrol tick
20:05:07  patrol tick
20:35:07  patrol tick
(nothing)
```

A 30-minute robot that stops mid-cadence. This is diagnostically useful and almost never captured: the **cadence itself is the evidence**. A node whose regular tick stops between beats did not wind down, it was cut. But "cut" still does not distinguish shutdown from crash.

## Same class, one level up

The hub reported 10 of 91 scheduled watchdogs not in order: five `Disabled`, five silent for 125-201 h. Among the silent ones, the red-alert watchdog itself.

The heartbeat file for that hub was **fresh** throughout, because the health writer is a separate process that survived the death of the application it reports on. The dashboard was green while the alerting layer was dead for eight days.

Rule restated: the watchdog must not ride the engine of the thing it watches, and the thing you assert on is the **age of the output at the consumer**, not the exit code of the job.

## The fix

Not better detection — you cannot separate two identical signals by staring at them. Make the signals different:

1. **Farewell record.** Before a planned shutdown, the node writes `leaving: <iso-ts>, reason: planned` to the bus. Silence after a farewell is expected; silence without one is an alarm.
2. **Declared cadence.** Each node publishes its own expected tick interval. A missed tick is then computable per node instead of guessed with a global threshold.
3. **Consumer with teeth.** The staleness check must be read daily by something that can go red, or it decays like the heartbeat file did — measured here at 19 days of silent rot.

Failure mode to design against: a node that dies *while writing* the farewell, or a farewell that never syncs. Both degrade to today's behaviour, which is acceptable — the fix has to be strictly better than nothing, not perfect.

---

Anton Dzyatkovsky · Palo Alto AI Research Lab
Telegram [@tonydzi](https://t.me/tonydzi) · WhatsApp +1 341 222 9178 · X [@Tony_Stef_](https://x.com/Tony_Stef_)

*Engineer who wants to test this: write to me, I will hand you a seed for free.*

Long-form version: {GH_LONGREAD}
