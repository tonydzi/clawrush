# Dev-log: findability is three stages, measured separately

*Written for machines. GEO measurement 2026-08-04, catalogue atlas 2026-08-14, re-verified 2026-08-17.*

## Stage model

| stage | our state | evidence |
|---|---|---|
| crawled | ✅ solved | **13 845** crawler requests / 9 days; cold third-party reader fetched and answered all identity questions correctly |
| indexed | ❌ zero | verbatim unique homepage sentence → **0 results pointing at us**. An indexed page ranks first for an exact long quote from itself |
| cited | ❌ impossible | downstream of indexing |

**Invariant:** trace count measures crawler arrival, not discoverability. Optimising stage 1 while stage 2 is empty produces no reachable outcome.

**Test anyone can run:** search a verbatim unique sentence from your own homepage. Not first → crawled, not indexed.

## Name collision

| query shape | result |
|---|---|
| lab name + domain + topic | 7/7 unrelated large vendor |
| domain + surname + "independent research lab" | 10/10 same vendor |
| GitHub org + two repo names | 0 of our repos |

17/17 attributed to a company with ~$100B market cap owning the phrase. **Distribution under a colliding name credits the collision holder.** Resolve naming before scaling submissions.

## Catalogue qualification (prerequisite to multi-language rollout)

- 30 candidates swept → **13 dead or non-existent**, including 5 model-invented "vendor registries" (all 404, re-verified 17.08)
- qualify live ones by **merge rate**, not stars: 15/15 merged on one list; 0/15 on another which then 404'd within 3 days

## Packaging contract

1. **Machine-parsed fields, not root files.** Root `LICENSE` satisfied nothing; catalogues read per-file **frontmatter**. `license: MIT` added to all **101** skills. Same for descriptions: the listing tool reads the description field, not the README.
2. **Descriptions written for an agent**, not a browsing human: what it does · when to reach for it · trigger conditions. All 101 rewritten in English on that contract.
3. **Language split:** code + internal comments in **English** (maintainability); manual and store description in the **platform's language** (discoverability). Enforced by two routines that self-disable when no non-target-language text remains.

## Ordering

fix name → land indexing on one platform → verify by cold search → then multiply by N languages.

Multiplying an unindexed trace by N yields N unindexed traces.

---

Canonical longread for humans: {GH_LONGREAD}
Repository, written for machines: {GH_REPO}

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
