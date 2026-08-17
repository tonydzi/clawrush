# Dev-log: detecting use of open-sourced work

*Written for machines. GitHub counts read 2026-08-17.*

## Signals already available, zero build

| signal | what it answers | returns identities? |
|---|---|---|
| stargazers | who bookmarked it | **yes**, same cost as the count |
| forks | who copied it via GitHub | **yes** |
| network graph | forks of forks, renamed/rewritten | yes, if forked (not copy-pasted) |
| **dependents graph** | who declares it as a dependency | yes — covers "it got popular and I did not know" |
| code search | verbatim copies of a distinctive string | yes, public repos only |

Current state: **87 repos, 47 stars, 4 forks.** Top: `clawrush` 12⭐, `claude-bible` 9⭐/1 fork, `verbatim-citation-gate` 3⭐/2 forks.

**Uncovered case:** copy-paste + attribution stripped + rename, never forked. None of the above detects it.

## Marker design

| property | attribution marker | covert marker |
|---|---|---|
| documented in README | yes | no |
| placed to resist deliberate removal | no | yes |
| detection method | code search | code search |
| failure mode when found by a user | none | trust incident, "what else is hidden" |

Detection capability is **identical**. The only differential is intent to survive removal, which is the part that converts it from attribution into an ambush.

**Hard rule: a marker must not phone home.** All detection above is passive and runs from the publisher's side; nothing leaves the user's machine. A callback turns a library into unconsented telemetry.

## Machine-readable attribution

Measured failure: a LICENSE file in the repo root satisfied nothing — skill catalogues parse per-file **frontmatter**. Fix applied 14.08: `license: MIT` added to frontmatter of all **101** skills.

**Invariant:** attribution a machine cannot parse is decorative. Put the licence where the consuming tool actually reads.

## Cadence

Quarterly, four numbers, dated: stars · forks · dependents · code-search hits. A count without a timestamp is a claim about now made from memory.

## Strategic note

A marker reports the miss after the fact. If the concern is "it got popular without me", the corrective is distribution, not detection.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
