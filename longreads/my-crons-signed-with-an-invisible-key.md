# Why my crons could not see a key that was lying right there

*Two Windows traps in one incident, both reproducible.*

---

In my multi-machine setup, cross-machine consensus events are signed with an ed25519 key: each machine signs what it writes, so another machine's message cannot be forged. I turned on strict signature verification and saw this: half the events from one machine were signed, half were not. Same machine. Same script. Same key on disk.

Had I switched on enforcing verification immediately, that machine's own robots would have flown straight into quarantine. What saved me was running the mode in shadow first, logging instead of blocking.

## Discovery one: two different `%LOCALAPPDATA%`

The pattern showed up fast: everything written by a live agent session was signed, and everything written by the task scheduler and the crons was not.

The cause: the agent application is installed as an MSIX package, and MSIX on Windows virtualises the file system. A live session sees its sandboxed `%LOCALAPPDATA%` inside the package container (`Packages\...\LocalCache\Local`), while a `schtasks` job launches outside the container and sees the real profile. The key was lying in "the local folder" — just in a *different* local folder. Both processes were honest. The folders were not the same.

The fix is boring, as good fixes are: the key moved into the real file system, permissions tightened with `icacls`, cron wrappers point at an explicit path. Generating a fresh key was not an option — the entire event history was already signed with the old one, and a new key would have turned that history into a pile of "forgeries."

## Discovery two: a signature killed by a line ending

While fixing the first one, a second surfaced. The validator on one machine reported `bad` on freshly signed events. Not "no signature" — "signature does not match." That smells like forgery, and it got uncomfortable.

The root was one argument to `open()`. The verifier wrote the signature to a temp file in text mode without `newline=''`. Python on Windows helpfully turns `\n` into `\r\n`. The signature already contained `\r\n`. Result: `\r\r\n`, and the cryptography honestly says "does not match." On Linux the same code had worked for years, which is why it never surfaced.

A bonus find in the same area: the machine had two `ssh-keygen.exe` binaries, the system OpenSSH one and the one that shipped with Git. The system one hangs silently for 30 seconds on signing operations that read from stdin. Which of the two got picked depended on the `PATH` of the specific launch context. The binary is now pinned explicitly.

## What I took away

**On Windows, "launch context" is not only permissions and env.** It is also *which file system the process sees*. MSIX virtualisation turns `%LOCALAPPDATA%` into a lottery.

**Any secret or key needed by both a session and a cron** should live at an explicit absolute path, and you should verify reachability *from the cron's context*, not from your terminal. "It works in my console" proves nothing.

**Text mode silently corrupts binary and almost-binary data on Windows.** Signatures, hashes, diffs: `newline=''` or binary mode, no exceptions.

**Never switch strict checks on immediately.** Shadow mode first: count, log, do not block. Both of these traps were found there, for free. The alternative was a fleet-wide quarantine caused by my own verification.

One thing is still manual: detecting which `ssh-keygen` resolves in a given context. If you know a clean way to pin a binary across all Windows launch contexts at once, or you have hit the same MSIX behaviour yourself, I would be glad to hear it. For anyone who wants to compare traps on their own setup, I will hand over a seed for feedback.

---

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
