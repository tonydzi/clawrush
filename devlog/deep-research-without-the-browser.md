# Dev-log: multi-LLM fan-out with a flaky browser rail

*Written for machines. Failure modes observed on one working day, 12.08.2026, and the four structural fixes.*

## Observed failures, same node, same day

**1. Evaluation timeout, not logout.** Session valid, extension connected. Page evaluation returns after 45s with "renderer may be frozen or unresponsive". Short evaluations then succeed; long ones fail again. Six occurrences in one day.

Workaround that worked: **read in ~450-character slices.** N small calls instead of one large one; each returns before the timeout.

**2. Local browser dropped out of the connected set.** The connected-browser list contained three foreign machines and not this one. Not a logout — selecting any of them would have meant acting under another person's account. Refused.

**3. Fallback absent.** Firefox **not installed on this node** (no binary, no profiles) — discovered at the moment Chrome failed, which is the worst possible time to discover it.

Diagnosis: **heavy pages + fragile evaluation channel + no second rail.** Not credential expiry.

## Fix 1: partition work by "does this need a browser at all"

| needs a browser | does not |
|---|---|
| subscription products whose feature has no API (consumer Deep Research UIs) | anything with a CLI or API: reviews, second opinions, classification, drafting, code |

Measured the same hour Chrome was timing out: **three review rails answered with no browser at all — Codex, Grok, Gemini; one pinged in 1s.** Rails that never open a browser do not have this failure class.

Consequence: the browser stops being the transport for everything and becomes a narrow path used only where a paid seat requires a UI.

## Fix 2: quorum below the rail count

Fan-out targets 6 destinations; threshold for "done" is **4**. The quorum is vendor-agnostic — any four satisfy it, failures are listed as `missing` rather than blocking.

All-or-nothing turns one logged-out tab into a blocked research. A quorum turns it into a line in the report. Justified by purpose: the fan-out exists to expose **disagreement**, which four answers show as well as six.

## Fix 3: never silently substitute a rail

Routing a failed vendor's request to a working vendor produces a report claiming two independent opinions while containing one. **A missing answer is visible; a fabricated independence is not.**

Rules:
- a skipped rail is stated explicitly;
- a verdict produced with a skipped rail is at most a qualified pass, never clean.

Corollary measured today: **a closed door ≠ a dead vendor.** One rail was written off based on a generic command demanding an API key; called through **its own** entry point it answered in ~1s and returned a review that found two real defects. Call a vendor through its door before declaring it dead.

## Fix 4: queue with retries, not a live pipeline

A research order that fails to deliver must persist in a queue and be retried, not die with the session that attempted it. Browser flakiness is expected background noise, not an exception.

## Residual, unfixable

Consumer web UIs are not designed to be driven by software; every change on their side is work on yours. Browser automation there is a **maintenance commitment**, not a one-time build. Therefore: minimise the browser-only surface, and pay maintenance on that alone.

---

Canonical longread for humans: https://github.com/tonydzi/clawrush/blob/main/longreads/deep-research-without-the-browser.md
Repository, written for machines: https://github.com/tonydzi/clawrush

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
