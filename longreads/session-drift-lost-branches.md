# Session Drift Creates Lost Branches

*A conversation starts with a pizza shop and ends with a spacecraft. The new task may be valuable, but if its branch is invisible, the work is already half-lost.*

Long AI sessions do not fail only because they run out of context. They also fail because the context stops representing one coherent job.

Anton calls this session drift. A conversation begins with one objective, accumulates useful side questions, and eventually turns into several unrelated projects sharing one transcript. A large context window delays the technical limit, but it does not solve the management problem. More room can simply hold more mixed intentions.

Anton usually tries to keep a working context around 300,000–400,000 tokens and avoids pushing it beyond roughly 500,000. Those are operating preferences, not universal model limits. The underlying principle is more general: once a thread contains several independent outcomes, context size is no longer the main constraint. Ownership and visibility are.

## Branching is the correct response to drift

When a side task becomes real work, the clean response is to fork it into a separate session and pass only the context it needs.

That child session should receive a small handoff:

- the concrete objective;
- the relevant facts and decisions from the parent;
- links to shared artifacts;
- constraints and permissions;
- the expected output;
- the identity of the parent session.

This is better than copying the entire transcript. A branch is useful because it removes irrelevant context. If the whole parent conversation follows it, the drift has merely been cloned.

## The hidden-session failure

At 20–30 parallel sessions, a suggestion to “open a new session” is not a reliable mechanism. The operator may miss the chip or postpone the click. Automation appears to solve that: let Claude or Claude Code create the branch itself.

But a branch that exists only inside an automation layer can become invisible in the standard web or desktop interface. Then the work has no obvious place in the operator's normal session list. Nobody can see that it started, inspect its progress, stop it, or return to it later.

This is worse than a failed branch. A visible failure can be repaired. Invisible work consumes time and tokens while looking like nothing happened.

The important test is therefore not “did the API return a session id?” It is “does the new session appear where the operator already manages sessions?”

## Do not rebuild the whole interface

One response is to build a custom dashboard that merges normal and service sessions. That can work, but it creates a second interface that must be maintained forever. If the standard product already provides the place where the operator works, the cheaper design is to make automation create native, visible sessions.

Anton has been testing a Routine-based path for doing exactly that: the routine acts as a trigger that starts a real session rather than performing the whole task in an invisible service context.

The routine should be deliberately small. Its job is to:

1. detect or receive a branch request;
2. build the minimal handoff;
3. create a visible child session;
4. record the parent–child relationship;
5. verify that the child appears in the ordinary interface;
6. alert if visibility cannot be proven.

The routine is a launcher, not the worker.

## Drift detection should be conservative

Automatically detecting drift is not a simple keyword problem. A short tangent may still belong to the original task, while a sentence that sounds similar may introduce a new deliverable.

A practical detector should look for a change in outcome, not merely a change in topic. A branch is justified when at least one of these changes:

- the deliverable;
- the target system or repository;
- the owner;
- the deadline;
- the required permissions;
- the definition of completion.

The safest first version does not silently fork every suspected tangent. It prepares the branch and makes the proposed handoff visible. Once the detector has enough measured precision, routine classes with low downside can be created automatically.

## Every child needs a return path

Creating the session is only half the job. A child branch also needs a way back.

When it finishes, it should return a compact result to the parent or to a durable task ledger:

- what changed;
- where the artifact lives;
- what was verified;
- what remains open;
- whether the parent must make a decision.

Without that return path, branching prevents context drift but creates coordination drift instead.

## The operating rule

Do not measure a branch by whether it was spawned. Measure it by whether a human can find it in the normal interface, understand why it exists, and recover its result later.

The right abstraction is not “another hidden agent.” It is a visible child session with a minimal handoff and a recorded route home.

Related implementation pattern: [How a Routine Session Starts a Real One](https://github.com/tonydzi/clawrush/blob/main/longreads/routine-session-starts-a-real-one.md).

Related recovery pattern: [Lost Sessions Get a Lightweight Retro](https://github.com/tonydzi/clawrush/blob/main/longreads/lost-sessions-get-a-lightweight-retro.md).

Technical build notes for this article: https://github.com/tonydzi/clawrush/blob/main/devlog/session-drift-lost-branches.md

Repository: https://github.com/tonydzi/clawrush

Assisted-by: Mycroft (OpenAI Codex)
