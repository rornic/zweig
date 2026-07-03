---
name: zweig-refine
description: The cut-draft-repeat refinement loop, taken from Stefan Zweig's own described writing process. Apply once a first draft of any prose exists (technical documentation, PR descriptions, commit messages, code comments, briefs, Slack messages), to condense it before it ships.
---

# Zweig Refine

Refinement is a loop of real edits against a real file, not a pass reasoned about silently and never checked. See `EXAMPLE.md` for a worked transcript of the loop end to end.

Before the loop, read `../STYLE.md` in full. It defines both what to cut ("Skip these on the way in", "Punctuation") and what never to cut ("Cut slack, not substance"). Every pass below applies both: a rewording edit can introduce an em dash or a hedge word as easily as it can remove one.

## Set up the working draft

- If the draft already lives in a real file you're editing in place (a docs page, a README, a code comment in situ), work directly on that file. Skip straight to the loop.
- Otherwise (a commit message, PR description, Slack message, or any output with no backing file), write the current draft to `<scratchpad>/zweig-draft.md`, resolving your session's actual scratchpad path. Do every cut as an Edit against that file, and copy the converged text into the real output only once the loop and gate below are both done.
- If the draft is only part of a larger file (one comment in a source file, one section of a template), scope every edit to that region. Unrelated surrounding content doesn't count toward convergence either way.

## The loop

1. Read the working file in full.
2. Cut: make an Edit call for every sentence, bullet, or word that can be removed or reworded without losing precise meaning, including rewording that says the same thing in fewer or plainer words even if nothing is deleted. Throw ballast overboard, favoring fewer, denser points over breadth, and cut self-descriptive or boilerplate lines. In the same pass, fix any em dash, stray semicolon, hedge word, throat-clearing opener, or boilerplate transition, whether it was already there or one of your own edits just introduced it. See STYLE.md's "Cut slack, not substance" for what's off-limits. A cut only counts if it's a real Edit call, not reasoning about one without making it.
3. If step 2 made at least one edit and you're under 4 passes total, go back to step 1 for a new pass on the updated file. Otherwise, stop.

A pass that makes zero Edit calls is the only valid signal of convergence. There's no separate ledger to keep: the edit history on the working file is the record.

## Fresh-reader gate

Your own reread can't test whether a cut lost substance: you still remember what you removed, so you can't judge what a reader landing on the text cold would be missing.

Once the loop above stops (by convergence or by hitting the 4-pass cap), spawn one fresh subagent, not a fork, with no access to this conversation. Run it on a fast, cheap model such as haiku, since a short draft doesn't need a frontier model to answer two questions. Give it the draft text and those two questions: what's confusing, and what information it would need that isn't there.

It gets nothing else: no context on the original ask, no knowledge of what got cut, no access to this skill's instructions. Do this once, as a final gate, not on every pass.

Skip this gate only if the draft is a single line or a single sentence (a commit subject, a one-line Slack ping, a one-line code comment). Anything longer goes through the gate, including a short bulleted list.

- If the fresh reader is missing information it needed, a cut went too far into substance: restore it with one corrective edit, then stop. Don't re-run the gate.
- If the fresh reader has no substantive complaint, the draft is done.
