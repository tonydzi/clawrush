# My AI Read the Genius for Me

**Previously on this show:** I'm not a programmer, but I'm building a second brain and a swarm of AI automations. In past episodes I worked as a courier between two AIs and buried a motherboard. Today's episode is quieter, but possibly the most important one yet: it's about how access to other people's expertise just changed.

## Cold open

For weeks I had the same browser tabs open. Articles by one author from Habr (the big Russian engineering blog platform), I'll just call him Arthur: it recently turned out we're in the same community, he's an admin there, and he is scary smart. Deep engineering articles about building LLM workflows properly and economically.

I'd open those tabs, read, nod, and close them. Then open them again. I understood the general idea but couldn't implement any of it: between "I read it" and "it runs at my place" lies a chasm, and the bridge across it is called engineering brains, which I don't have.

## The conflict: the expertise exists, the access doesn't

The situation is almost comically typical. Concentrated expertise exists right next to you: a man has already solved the problems you keep hitting. It's even published, just take it. But there's a wall between it and you: to apply the knowledge, you need to be roughly as much of an expert as the author.

That wall used to have two honest workarounds: years of study, or hiring an engineer. I had neither.

## The twist: "Claude, read it for me"

In despair I did the thing that now seems obvious and a year ago would have sounded like science fiction. I told my Claude: "Please read everything Arthur writes. I've read and read, but I don't have the brains to implement it."

Claude read it. All of it. And came back with a verdict I won't forget: "This guy is a genius. He solves the problems we couldn't solve for a long time."

Sit with that sentence. My AI, which has been building this system with me for months and knows all our sore spots, recognized in someone else's articles ready answers to our unsolved problems. Not "interesting material," but "here's the fix for the thing we kept tripping over."

## The resolution: someone else's articles now run in my production

From there it moved fast. We took several ideas from Arthur's articles and shipped them. The most important one sounds boring and saves plenty: recurring service tasks should not call the LLM every time. Checks, gates, stop-conditions, routine triggers, all of that should be decided by plain deterministic code, free and instant. The smart model gets called only where judgment is genuinely needed: synthesis, evaluation, language.

We've already made several token-spend optimizations based on this, and it's just the start: at least four specific points from Arthur's materials deserve their own detailed breakdown. That will be a separate episode.

## What actually happened here

The real shift isn't about tokens. The nature of access to expertise changed.

The old chain looked like this: an expert writes → an expert reads → an expert implements. There was no room in it for a regular person. Now it's: an expert writes → my AI reads → it runs at my place. Claude became a translator from expert to human, and it doesn't translate words, it translates straight into action.

For authors like Arthur this is great news, by the way: their audience is no longer limited to people capable of understanding them. Their articles are now read by AIs too, and through AIs, by people like me. Write deep; the machines will parse it, the humans will ship it.

Thank you, Arthur. Your articles run in my production even though I still don't fully understand them. That's the best compliment a layman can pay an engineer.

## Cliffhanger

Coming up: the detailed breakdown, at least four techniques from Arthur's articles that we shipped, with before-and-after numbers. We'll see how much of a genius's work survives contact with a layman's production.

To be continued. As usual, fairly soon.

If you like what we do, follow on X https://x.com/Tony_Stef_ or Telegram @Tonyssd. Want me directly, WhatsApp +1 341 222 9178. Busy, six kids, but I will still reply.

Technical companion: [dev log](../devlog/my-ai-read-the-genius-for-me.md)
