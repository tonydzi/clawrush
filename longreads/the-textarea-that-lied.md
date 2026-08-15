# The textarea that lied: how my agent lost nights on "sent" prompts

*Every check green. The action impossible.*

---

My agent spends nights distributing research prompts across three LLM web interfaces: paste the text, hit send, collect the report half an hour later. Sounds trivial.

One morning I found three runs in the ledger marked "started" and exactly one that had actually run. The other two had stood all night with the prompt sitting in the input field. The send button was never pressed, because it did not exist.

## How the agent pastes text

Keyboard emulation is out from the start: the prompt has newlines, and every Enter in a chat composer means sending a truncated fragment early. The research quota burns on half a prompt. Been there.

So pasting goes through JS: find the composer, put the text in programmatically, verify it landed, and only then press Send. The verification is threefold: length, first 40 characters, last 40. We named the rule *probe before burn* — until the text is proven to be in the field in full, the button stays untouched.

## Where we got fooled

On one of the sites the selector found an honest `textarea`. We wrote the value through the native setter, dispatched an `InputEvent`, read it back: length matched, head and tail in place. `ok: true`. Press Enter. Nothing. Look for a Submit button. There is no button.

Three hours of debugging later the picture came together. The site's frontend had moved to ProseMirror, a contenteditable editor, and the visible `textarea` stayed in the DOM as a hidden mirror for its own purposes. The mirror accepts a value. The mirror returns the value. But the React application's state only updates from the real editor. The form believes the field is empty, so it simply does not render the send button.

Our verifier was honestly checking the contents of the wrong element. A perfect false positive: all checks green, action impossible.

## The fix

The answer is in how ProseMirror accepts text natively: through a paste event. A synthetic paste with a DataTransfer:

    const dt = new DataTransfer();
    dt.setData('text/plain', prompt);
    editor.dispatchEvent(new ClipboardEvent('paste', {
      clipboardData: dt, bubbles: true, cancelable: true
    }));

ProseMirror runs it through its normal pipeline, updates its model, React learns about the content, the Submit button appears. The paste cascade now targets the contenteditable editor first, with the `textarea` kept as the last fallback in case some older markup still lives somewhere.

The second half of the fix matters more than the first: the "sent" check is now separate from the "pasted" check. Pasting is confirmed by reading `innerText` of the real editor; starting is confirmed by the URL changing to a chat address plus a live progress indicator. Until both facts hold, the ledger status is not "started" but "submitted, awaiting proof." That one line is what now saves the nights.

## Conclusions that outlive the specific site

**Verify the element the application reads, not the one your selector found.** The `innerText` of a contenteditable and the `value` of its mirror can live entirely separate lives.

**"A value is in the field" and "the form knows about the value" are two different facts.** A framework sits between them.

**Paste is not send, and send is not start.** Three states, three separate proofs.

**Expensive operations belong behind a deterministic gate.** Ours was research quota. An LLM agent must never be allowed to conclude "eh, it probably went through."

The UI of these sites will drift again and the cascade will survive it: one method breaks, the next one runs, and the gate refuses to burn quota on an empty field. If you have caught the same kind of mirror in Quill, Lexical or Slate, write it up — I am collecting them. And for anyone who wants the cascade itself, I will hand over a seed for feedback.

---

Conceived by Mycroft and Tony, Palo Alto AI Research Lab. Proudly made in Silicon Valley 🌉
