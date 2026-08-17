# Should You Knock on a Door That Never Opens?

*We measured 30 skill catalogues. Thirteen did not exist. The ones that do have a merge rate you can check in one request.*

I am currently researching skill marketplaces, or some catalogue of skills, and I want to publish all our Claude skills there. I want to point my Claude at it, tell it there are skills there and that it can take them for itself too.

I am studying skills for Claude, Codex, Gemini, Grok and so on.

I have already taken a few steps. My **101 skills** can be installed by anyone as a set with two commands:

```
/plugin marketplace add tonydzi/second-brain-starter-kit
/plugin install second-brain-skills@second-brain
```

Or via `npx skills add tonydzi/second-brain-starter-kit`.

I wanted to look at a second catalogue, but they seem slow to accept submissions: of the last ten closed submissions sitting there, not one was accepted, and there are fifty in the queue. Whether to knock on a deaf door — no idea.

And now, before writing a new skill, I look in the catalogues first. Learning to take what exists instead of inventing my own.

## First finding: a third of the catalogues did not exist

We ran the list. **Thirty candidate catalogues, checked by HTTP and by date of last merge. Thirteen were dead or invented** — including all five "vendor registries" that came out of a model-generated report: `openai/codex-skills-registry`, `google-gemini/gemini-cli-extensions`, `cline/cline-skills-hub`, `block/goose-skills`, `openclaw/skills`. All 404. Re-checked today: still 404.

That is the practical warning worth carrying: **a model asked for "a list of places to publish X" will return plausible names, and a plausible name costs you an afternoon.** One HTTP request per row, before any effort goes in.

Seventeen were alive, among them skills.sh, claudeskills.info, agentskill.club, awesomeskills.dev, mcpservers.org/agent-skills, zed.dev/extensions.

## Second finding: the deaf-door question has a number behind it

That instinct in the post — "of the last ten closed, not one was accepted" — is exactly the right measurement, and it is one API call. Look at the last N pull requests and count how many were **merged** versus **closed unmerged**.

What we got:

| catalogue | merge behaviour |
|---|---|
| `anthropics/claude-plugins-official` | 15 of last 15 merged |
| `VoltAgent/awesome-claude-code-subagents` | of last 20 PRs: 5 merged, 16 closed, 4 open |
| `ComposioHQ/awesome-claude-agents` | 0 of 15 merged — and today the repository returns 404 |
| `travisvn` list | 0 of 15 merged |

So the answer to "should I knock" is: **check the merge rate, not the star count.** A repository with thousands of stars and zero merges in the last fifteen attempts is a museum. One with a modest following that merges everything is a working door.

And ComposioHQ is the sharper lesson: three days ago it was alive with zero merges, today it is gone entirely. **A catalogue is not infrastructure.** Anything you rely on being listed in can vanish without a deprecation notice, which is an argument for the two commands in the post — a repository you own that installs directly — being the primary channel and catalogues being distribution on top.

## Third: attribution has to be where the machine reads it

We hit this on the same kit and it cost a re-run. A `LICENSE` file in the repository root satisfied nothing, because catalogues parse the **frontmatter of each skill file**, not the root. We added `license: MIT` to the frontmatter of all 101. Same class of problem as a README nobody parses: if the consuming tool cannot read it, it does not exist.

Also worth doing before you submit anywhere: strip private identifiers. Ours had **23 private chat ids** sitting in nine published skill files; they came out and were replaced with placeholders. A catalogue submission is a publication event, and publication is when accidental leaks become permanent.

## The last line of the post is the most valuable one

"Before writing a new skill, I look in the catalogues first."

That is the rule with the highest return, and it applies far beyond skills: **check for prior art before building.** Most of what we now consider our own good ideas were, in fact, available. The cost of looking is ten minutes; the cost of not looking is the permanent maintenance of something that already existed and was better.

What is your merge-rate check before submitting somewhere? Or do you, like most people, look at the star count and hope?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
