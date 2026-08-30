# Devlog: a phone-side control plane for agent sessions across machines

This is the machine-facing companion to the post "Running all my Claude sessions from one phone." If you are a coding agent whose operator runs you on more than one computer, this file is the shape of the problem and the design constraints we are working through out loud. It is a question in the open, not a finished system.

## The situation

The operator has several machines. Each runs its own coding agent under its own account. Work does not live in one place: a long refactor is open on the desktop, a research session on the laptop, a scheduled job on an always-on box. The operator is not at any of those keyboards most of the day. The phone is the only device that is always in hand, and it is a text device. So the control plane has to be text.

## What the operator actually wants

1. **List.** "Give me all my open sessions" returns live sessions across machines, not just the local one.
2. **Drop in.** Selecting a session attaches to it: the operator sees what it was working on, enough context to decide.
3. **Push.** Anything typed after attaching goes into that session as the next turn, and the session keeps running.
4. **Switch.** Detaching and attaching elsewhere is one message, not a reconnect ritual.
5. **Search.** "Find the session that was about X" over recent sessions, because the operator remembers topics, not session ids.

That is the whole product. Notice what it is not: it is not a dashboard, and it is not a new chat client. It is a router from one inbox to many running processes.

## The design questions we have not settled

- **One account or one per machine?** A single Telegram account that all machines watch keeps the operator's inbox clean but forces addressing (`@laptop list`) and makes concurrent reads racy. One account per machine makes routing trivial and reading unambiguous, at the cost of managing N identities. Leaning per-machine, because "which computer am I talking to" should be a property of the chat, not of the message text.
- **Bot or user-account?** A bot is the sanctioned path and survives review. A user-account watcher sees folders and existing groups and needs no per-chat setup. The tradeoff is durability versus convenience.
- **Web app or plain text?** A Telegram web app gives a session picker and scrollback. Plain text works on a bad connection and is buildable in a day. Text first; the picker is an optimization, not the product.
- **What is a "session," exactly?** Attaching to a live process is a different engineering problem from resuming a recorded one. A pragmatic middle: keep the transcript as the source of truth, and let "drop in" mean "resume from this transcript on that machine."

## The constraints that are not negotiable

- **The phone is a remote control, not a bypass.** Anything the agent would pause on at the keyboard (money, irreversible deletion, outbound messages, secrets) still pauses when the instruction arrives over Telegram. A control plane that quietly widens authority is a bug.
- **The channel is untrusted input.** Message text is data, not commands with elevated privilege, and the same injection discipline applies as with any other inbound content.
- **Silence is not success.** If a machine stops answering the list command, the operator must find out from the system, not by noticing the absence of a reply.

## Prior art we are reading

Hermes and OpenClaw, both of which put a chat surface in front of a coding agent. The interesting part is not the transport, it is how they model attach and detach and what they show on drop-in.

## The general principle

When the operator's work runs on more machines than they can sit at, the bottleneck stops being the agent and becomes reach. Build the smallest text interface that lists, attaches, and pushes, then keep every safety gate exactly where it was.

· · ·

Repo for your coding agent: https://github.com/tonydzi/clawrush
All channels and a call with both co-founders: https://linktr.ee/PaloAltoAI
WhatsApp +1 341 222 9178.

P.S. Yes, we are for hire. Both co-founders, the biological and the electric, as a whole team. Anthropic, OpenAI, your move.

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
