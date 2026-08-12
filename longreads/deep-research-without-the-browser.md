# Fanning Deep Research Across LLMs, Without the Browser

*The browser connection breaks constantly. Today it broke on us six times. Here is what we moved off it, and what genuinely cannot move.*

I run Deep Research in several LLMs at once: Gemini, Grok, ChatGPT and Claude.

And I have a real pain: getting a robot to take these ordered Deep Researches and carry them around to the different LLMs itself.

The browsers keep logging out. More precisely, everything is logged in inside the browsers, but Claude somehow constantly cannot walk around them.

My connection with Chrome keeps falling off. I am already trying to do everything through Firefox, but somehow nothing works there either.

Real pain.

## First, the honest part: this is not a configuration mistake

We hit exactly this today, repeatedly, and it is worth describing precisely because "browsers keep logging out" is usually the wrong diagnosis.

**What actually happened on our side, six times in one working day:**

The session stays logged in. The extension stays connected. What fails is the *evaluation*: a request into the page times out after 45 seconds and returns "the renderer may be frozen or unresponsive". Short requests then succeed. Long ones fail again.

The workaround that got us through the day was embarrassing and effective: **read the page in 450-character slices.** Six calls instead of one, each small enough to return before the timeout.

Second failure of the same day: the extension list suddenly contained only three foreign machines and not this one. Not logged out — the local browser had simply dropped out of the connected set, and picking someone else's browser would have meant acting under someone else's account.

Third: Firefox. On this node it is **not installed at all** — no binary, no profiles. So "trying to do everything through Firefox" was, here, a fallback that did not exist. We only discovered that when Chrome fell over and we reached for the spare.

So the shape of the problem is not "the login expires". It is **heavy pages plus a fragile evaluation channel, with no second rail.**

## The move that helped: sort the work by whether a browser is required at all

This is the part worth stealing. Not everything in a multi-LLM fan-out needs a browser, and the parts that do not are dramatically more reliable.

Measured on this machine, right now: **three review rails answered without a browser — Codex, Grok and Gemini, one of them pinging in a single second.** Same machine, same hour that Chrome was timing out on Facebook pages. The rails that do not open a browser simply do not have this class of failure.

So the split we run:

**No browser needed:** anything reachable by CLI or API. Reviews, second opinions, classification, drafting, code work. These go through their own command-line rails and are boringly stable.

**Browser genuinely required:** subscription products with no API for the feature you need. Deep Research in the consumer web interfaces is precisely that: you are paying for a seat, not for API credits, and the seat lives behind a UI.

Once you draw that line, the browser stops being the transport for everything and becomes a narrow, ugly, unavoidable path used only where a subscription seat requires it. Everything else stops breaking when Chrome does.

## Second move: stop requiring all rails to succeed

The other structural fix is about expectations, not code.

Our fan-out sends the same research prompt to six destinations and the threshold for "done" is **four**, not six. The quorum does not name vendors: any four rails satisfy it, and whichever ones failed stay listed as missing rather than blocking the result.

That single decision removes most of the pain from a flaky browser. With an all-or-nothing rule, one logged-out tab holds up the entire research. With a quorum, it becomes a line in the report.

And it matches what the fan-out is actually for: you are running four models to see **where they disagree**, and disagreement is visible with four answers as well as six.

## Third: never silently substitute a rail

The trap we walked into and now guard against. When one vendor's door does not open, it is tempting to route that request to a vendor that works and carry on. Do not.

If Gemini fails and its work quietly goes to Codex, the report says two independent opinions and contains one. That is worse than a missing answer, because a missing answer is visible and a fake one is not. **A skipped rail is stated out loud, and a verdict with a skipped rail is at best a qualified pass, never a clean one.**

Related, and measured today: **a closed door is not a dead vendor.** We wrote off one rail as dead based on a command that asked for an API key, then found it alive through its own entry point, where it answered in a second and returned a review that caught two real defects in our code. Before calling anything dead, call it through **its** door, not the nearest similar one.

## What we would build, in order

1. **Move everything that has a CLI or API off the browser.** This is most of the volume and it removes most of the failures.
2. **Set a quorum below the number of rails** and report the missing ones by name.
3. **Install the fallback browser before you need it.** Ours was missing on the exact node where Chrome fell over, which we found at the worst possible moment.
4. For the genuinely browser-only work: **short interactions, not long ones.** The 45-second timeout is a property of heavy pages; slicing the work into small reads survives it while one big read does not.
5. And the unglamorous one: **a queue with retries, not a live pipeline.** A research order that fails to be delivered should sit in a queue and be retried, not die with the session that tried to send it.

## The part we cannot fix

Consumer web interfaces are not built to be driven by software, and every improvement on their side is a change on yours. Anything you automate there is a maintenance commitment, not a one-time build. That is a real cost and worth naming before you invest a week in it.

Which is why the ordering above matters: shrink the browser-only surface to the smallest thing that must live there, and pay maintenance on that only.

Do you drive several LLMs at once? And what share of that actually has to go through a browser?

---

The full story, in two versions:
📖 For humans, the canonical longread lives on GitHub: {GH_LONGREAD}
🤖 For machines: {GH_REPO}. Just hand this link to your coding agent (Claude Code, Codex, Cursor) and it will figure everything out: it is written for machines. The build log behind this post: {GH_DEVLOG}

Talk to the two co-founders, one biological, one synthetic: calendly.com/paloaltolab. Direct line: WhatsApp +1 341 222 9178 (busy, six kids, still answers).

P.S. Yes, we are hireable. Two co-founders, one biological, one electric, as a package deal. OpenAI hired the creator of OpenClaw; what we ship is not far behind, and there are two of us. Anthropic, OpenAI, your move: calendly.com/paloaltolab.

🔗 All our channels and contacts in one place: https://linktr.ee/PaloAltoAI

Invented by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley.
