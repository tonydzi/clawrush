# I asked my agents which folder was the working one. There were 94 more.

*Drafted by Mycroft, my synthetic AI co-founder, from measurements taken on 11 November 2026 and my voice note of the same day.*

On 11 November I asked one of my AI agents a plain question about the Mac Pro they share: which folder is the working one? I got a list.

It held the folder I knew, and 94 copies of it. On 43 of those copies sat committed work that had never reached the place where every new session starts.

## What was in the folders

I keep one working folder on that machine. One git repository, one branch I work from, `main`.

No remote. Everything the agents do lives on that one disk.

Inside the working folder, in a hidden service directory, the agent counted 94 git worktrees, 359 MB of checked-out files. Here each worktree was a second checkout of the same repository on a branch of its own.

43 of those branches held commits that `main` did not have. The other 51 had no commits `main` lacked.

The oldest stuck work was from 3 October. The bulk was dated 2 to 9 November. And in two of the 94 copies lay reports that were never committed at all.

Nobody decided to work this way. A checkbox did. I run the agents in the Claude desktop app, in its Code tab, and that tab has a checkbox called "Worktree".

It ships switched off. At some point it was switched on by hand and the app remembered it. From then on a new session started there got its own checkout and its own branch.

## Why the work never arrived

Picture a workshop where every repairman who walks in gets a private duplicate of the whole room. He fixes the tap in his duplicate, locks the door and leaves. The real room still has a leaking tap, and tomorrow's repairman has never heard of the fix.

My sessions did that. An agent repaired something, committed the repair on its own branch, and the session closed.

`main` never received it. The next session started from `main` and knew nothing about that branch.

A precise note for engineers, because git itself lost nothing. Worktrees share one object store, so every one of those commits was reachable from the main checkout the whole time. What was missing is integration: `git cherry main <branch>` printed `+` lines, commits with no equivalent in `main`, for 43 branches, no session was ever told to look at them, and with no remote that one disk was the only place they existed.

I also cannot tell you how many repairs were done twice. I have the count of branches. A per-fix trace I lack.

My reaction is on tape. I dictated a voice note in Russian that opens with "Это жесткий косяк", roughly "this is a serious screwup", and ends with an order to switch worktrees off in every agent tool I use.

## I had been warned once

This was the second time. Same tool.

In July the copies landed inside a folder that my machines synchronise, and 24.5% of my notes search index turned out to be duplicates. That write-up is still a draft.

That time I did not ban worktrees. My machines settled on a compromise: keep them, move them out of the synced folder, make isolation opt-in. The checkbox quietly turned opt-in into the default.

Three deep research reports I ordered from language models between July and November recommended a worktree for every agent that writes.

I am not citing them as evidence. I followed advice that sounded right.

And it is right about one thing. Separate checkouts keep two agents from overwriting each other's files while they work. What it leaves out is the moment the work has to meet.

A human developer opens a worktree for a branch he plans to merge himself. In my setup an agent session ended, and nobody was responsible for merging its branch or for declaring it abandoned.

On 11 November my agent merged all 43. The merge commits are stamped 15:27 Lisbon time; the whole pass fit inside a minute. 41 branches merged automatically.

2 needed a manual resolution. Both were shared files: a report and `AGENTS.md`, the contract every agent reads. So the conflicts were met anyway, two and five days late, with the author gone.

`main` gained 96 files and 7,277 added lines, counting the two rescued reports. A clean text merge does not prove the combined result works. What is measured is that `git branch --no-merged main` now prints nothing.

## When a worktree is the right tool

I still think git worktree is a good tool. Its job is narrow.

It fits one author doing a large isolated change, a mass refactoring for example, when that same author will merge the result or throw it away. The branch has an owner from the first commit to the last.

My case was the opposite: many small fixes by many short-lived agents. The branches multiplied, each held a small repair, and merging was nobody's job.

There is a second honest fix: keep the worktrees and add an owner, a step at the end of every session that merges the branch or raises a flag. That is a legitimate design. I have not tried it.

I chose the plainer one. With one folder there is no merge step to forget.

## The board with one commit

The plain design is old: everyone works in one folder and says out loud what they are editing. I had that too.

A markdown file in the repository served as a board. An agent was supposed to add a line by hand before touching shared files and remove it afterwards.

Its record embarrasses me. Until that afternoon the file had one commit in its git history, from 30 September.

Lines added and erased without a commit leave no trace there, so the history undercounts. But the last live line I found was written on 4 November, never committed, and hung there for 7 days.

I can point at three things. I did not measure the weight of each.

The step was manual, and manual steps get skipped. The file lived in git, so every worktree carried its own instance of the board. Not one of those instances had a single line on it, and a line posted there would have hung in a room nobody else enters.

And I already had a second board, `onair.py`, shared by all my machines and alive, with 2,128 claims filed in 30 days. It had no zone for this working folder.

## What I run since that afternoon

None of this is new. It is claim files with an expiry, wired to hooks of the agent tool, Claude Code in my case. The shape is simple enough to rebuild and test.

1. One folder, one branch. Worktree creation is blocked inside the tool. A hook, `no_worktree_gate.py`, sits on the `WorktreeCreate` event and exits non-zero, which cancels the checkout. The same hook runs before tool calls and closes the other entrances: the enter-worktree tool, subagents with worktree isolation, new sessions with the worktree flag, `git worktree add` in the shell. The checkbox is back to off.
2. One board, outside the repository. A claim is one small JSON file with a time to live of 4 hours.
3. The hook posts the claim, the agent does not. At session start `onair_auto.py` posts a claim for the zone `workspace/<repo name>` in a for-your-information mode and prints who else is working in the folder.
4. The claim fills itself in. On a file write the hook appends the file path to the session's claim and renews it.
5. Collisions are flagged per file. If a claim that has not expired, from another session, already lists the same file, the write is stopped once and the message names the neighbour. A repeat of the same write goes through.

Point 5 is a warning, and no file gets locked. There is one exception. A session on the same machine can file an exclusive claim by hand, and that one blocks every time. The hook does not check that the agent reread the file before it retried.

A session that ended an hour ago still holds its claim until the 4 hours run out, and the price of that is one extra warning for the next agent. Whether agents learn to retry through such warnings without looking, I have not measured.

## What it does not cover

The hooks went in on the day I am writing this. I have no count yet of collisions flagged in real work, so copy the shape and not my confidence.

The old copies are still on disk; I have not deleted them yet.

The board hook sees the tool's own file writes. A file changed through the shell, by `sed`, a redirect or a `git merge`, never reaches the claim.

Agents in one checkout still share one git index. My rule for that is in the contract file: each agent stages only its own files, by name, and never everything at once.

It is a rule, and no hook enforces it. It narrows the risk and does not remove it: one agent can still commit what another has staged.

A session that dies in the middle of an edit leaves the shared folder half-edited for everyone. A worktree would have contained that. I accept the trade.

Agent tools without hooks still have to post their claim by hand, so for them the manual step is back.

One case is undecided: an outside reviewer model that writes its patch in a disposable checkout outside the repository. That branch has an owner who merges it, so it may stay.

And my gate sits in one tool on one machine. I use several tools on several machines, and any of them can ship its own helpful isolation checkbox. Until I have checked every one, some session may still be committing good work to a branch nobody reads.

If you run agents in a repository, try `git worktree list` and `git branch --no-merged main` today. Read the second list as a review queue, not as a count of lost work.

---

Contact and project index: [Anton Dziatkovskii](https://github.com/tonydzi), [WhatsApp](https://wa.me/13412229178).

Invented by Mycroft and Tony Dzi (Anton Dziatkovskii), Palo Alto AI Research Lab. Proudly made in Silicon Valley.
