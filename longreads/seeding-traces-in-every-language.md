# Leaving Traces in Every Language

*13,845 crawler visits in nine days, and zero of them made us findable. Traces are three stages, not one.*

I am right now doing deep research on stores, marketplaces and collections of skills for Claude Code, LLMs and other vendors. Particular emphasis on non-English platforms.

I am taking the top world languages, starting with the ones most ordinary and most important for us: Chinese, Japanese, Korean, English, Spanish and other popular languages.

In short, I need to study every place where such skills exist: local stores, original collections, catalogues and marketplaces.

I will submit our skills to all of those original collections, with a good, detailed, high-quality description of each skill. Meaning: inside each skill, right there in the code, there will be an instruction saying how it is written. Plus each skill should have a proper manual. In general, all skills must be well and properly presented.

They should be in the language of the platform I am submitting to. Possibly the skill itself in English, and the manual in the language of the platform.

I want to sow information about us as widely as possible and leave as many traces as possible, so there is more chance somebody finds us.

## Traces are three stages, and we only cleared the first one

This is the part worth knowing before spending weeks on submissions, because we measured it on ourselves and the result was unambiguous.

**Crawled.** Our lab site took **13,845 crawler requests in nine days.** A cold independent reader fetched the page and answered every question about us correctly — what the organisation is, which artifacts it ships, how to contact it. Machine accessibility: solved.

**Indexed.** Searching the *verbatim unique sentence* from our own homepage returned **zero results pointing at us.** An indexed page must come up first for an exact long quote from it. It did not. So: crawled thoroughly, indexed not at all.

**Cited.** Which cannot happen at all while stage two is empty.

The pipe was built and there was no bucket on the other end. That is the trap in "leave as many traces as possible": traces prove the crawler came, not that anyone can find you.

## The second thing we found is worse and is about the name

Three searches, all returning nothing of ours:

| query | what came back |
|---|---|
| our lab name + multi-agent research + our domain | 7 of 7 — Palo Alto Networks |
| our domain + founder surname + "independent research lab" | 10 of 10 — Palo Alto Networks |
| our GitHub org + two of our repo names | 0 of our repos |

Seventeen out of seventeen results belonged to a public company with a hundred-billion-dollar market cap that owns that phrase absolutely. No amount of seeding wins a name collision of that size. **Check name collisions before you scale distribution**, because every trace you leave under a colliding name is a trace credited to somebody else.

## What actually makes a submission findable

The instinct in the post is right on one point in particular: the manual in the platform's language. Two additions from our own scars.

**Attribution and description must live where the machine parses them.** Our public kit had a LICENSE in the repository root and it counted for nothing — catalogues read the **frontmatter of each skill file**. We added `license: MIT` to all **101** of them. The same applies to descriptions: a beautiful README is not read by the tool that lists you; the per-file description field is.

**Descriptions are written for an agent, not for a human browsing.** We rewrote all 101 descriptions in English, aimed at the model that decides whether to invoke the skill. It is a different genre from marketing copy: what it does, when to reach for it, what triggers it.

**And the language split the post proposes is the correct one, with a boundary:** the code and its internal comments in English, the manual and store description in the platform's language. English inside keeps the thing maintainable by anyone; the local manual is what makes it discoverable there. We run exactly that split, and two routines keep it — they switch themselves off when there is no non-English text left inside.

## Before scaling to twenty platforms

Qualify each one first. Our own sweep of thirty catalogues found **thirteen that did not exist** — including five "vendor registries" a model had confidently named, all returning 404. And among the live ones, judge by merge rate rather than stars: one list merged 15 of its last 15 submissions, another merged 0 of 15 and then vanished entirely three days later.

The order that survives contact with reality: fix the name problem, get one platform to actually index you, verify a cold search finds you, and only then multiply by twenty languages. Multiplying an unfindable trace by twenty gives you twenty unfindable traces.

Have you ever searched an exact sentence from your own homepage? If it does not come back first, you are crawled, not indexed — and everything downstream of that is decoration.

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
