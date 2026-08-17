# A Fingerprint in Everything You Open-Source

*Most of the tracking already exists and is free. The part that does not exist is the part worth thinking hardest about.*

Morning thoughts.

I am producing a lot of content, skills and so on right now. Everything I make, I open-source. But to understand later whether anyone actually uses my products, it would be good to have some kind of traction signal.

To know: right, someone is using my product, even if they modified it a little.

So I am thinking about embedding a kind of altered fingerprint into everything I build: something like a mark saying "this was made by me". I would put it somewhere it is hard to remove, somewhere nobody refactors or changes anything.

That way it would be great if some popular product catches my eye one day and I see that it is popular, and my fingerprint means it is, loosely speaking, a product I once built.

I will research a bit more on how best to implement this. Make invisible genes of that sort in all the code I publish.

## Three quarters of this is already built, by GitHub, for free

Before writing any marker, it is worth knowing what the platform already tells you, because it is more than most people use.

**Forks and stars** are the obvious ones. Ours today: **87 repositories, 47 stars, 4 forks.** Both endpoints return the *names* of who starred and who forked at the same cost as the counts, which means "who uses this" is answerable, not just "how many".

**The network graph** shows every fork of a fork, including ones renamed and rewritten, as long as they were forked rather than copy-pasted.

**The dependents graph** is the strong one and almost nobody looks: if someone declares your package as a dependency, GitHub lists them. That covers the case the post is actually about — the product got popular and you had no idea.

**Code search** finds verbatim copies of a distinctive string across public repositories. Which is the honest, boring version of a fingerprint: pick one unusual identifier, keep it in the code, search for it periodically.

The uncovered case is real, though: someone copies the code, strips the attribution, renames things, and never forks. Nothing above finds that.

## Where the line runs, and it is not a technicality

There are two different things wearing the same word, and they have opposite properties.

**A visible, documented mark is attribution.** A distinctive constant, a signature in the docstring, a licence header, an unusual error string. It is discoverable, it is honest, and it works: you can code-search it later. Anyone who removes it is now visibly stripping attribution, which is a licence question with a clear answer.

**A hidden mark placed where nobody looks, designed to resist removal, is something else.** Not because of the tracking — because of the intent to survive a deliberate removal. Ship that in a repository somebody runs on their own machine and you have shipped a surprise. The first time a user finds it, the conversation is no longer about attribution, it is about what else you hid.

And the hard rule underneath: **a mark must never phone home.** A fingerprint that reports back turns an open-source library into telemetry the user did not agree to. Everything above — code search, dependents, forks — works passively, from your side, without a single byte leaving the user's machine.

## The version we would actually build

**License first, and put it where machines read it.** We learned this concretely: our public skill kit had a LICENSE file in the root and it counted for nothing, because the catalogues that list skills read the *frontmatter* of each file, not the repository root. We added `license: MIT` to all 101 skills for exactly that reason. Attribution that a machine cannot parse is decorative.

**One distinctive string, documented, per project.** Unusual enough to survive a rename and to be searchable. Written down in the README as "this is our marker", not hidden. That gives you the same detection with none of the ambush.

**Check quarterly, not continuously.** Stars, forks, dependents, code search. Four numbers, one sitting, and dated — otherwise you are comparing today's count to a number you half-remember.

And the uncomfortable part, which is the real answer to the post: **if the concern is that a product becomes popular without you, the fix is distribution, not detection.** A marker tells you afterwards that you missed it. Being the person people already associate with the thing means you do not find out by accident.

What do you use to tell whether anyone is running your open-source work? And is the number in front of you, or is it a feeling?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
