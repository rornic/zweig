---
name: zweig-refine
description: The cut-draft-repeat refinement loop from Stefan Zweig's own writing process. Run only when explicitly asked to refine, tighten, or cut a draft. zweig-write already front-loads density for every draft. Applies regardless of draft length, except the structural variance pass and fresh-reader gate, each of which has its own short-draft exception handled inside the skill.
---

# Zweig Refine

Refinement is a loop of real edits against a real file, not a pass reasoned about silently and never checked. See `EXAMPLE.md` for a worked transcript of the loop end to end.

## Set up the working draft

- If the draft already lives in a real file you're editing in place (a docs page, a README, a code comment in situ), work directly on that file. Skip straight to the loop.
- Otherwise (a commit message, PR description, Slack message, or any output with no backing file), write the current draft to `<scratchpad>/zweig-draft.md`, resolving your session's actual scratchpad path. Do every cut as an Edit against that file, and copy the converged text into the real output only once the loop and gate below are both done.
- If the draft is only part of a larger file (one comment in a source file, one section of a template), scope every edit to that region. Unrelated surrounding content doesn't count toward convergence either way.

## The loop

1. Read the working file in full.
2. Cut: make an Edit call for every sentence, bullet, or word that can be removed or reworded without losing precise meaning, including rewording that says the same thing in fewer or plainer words even if nothing is deleted. Throw ballast overboard, favoring fewer, denser points over breadth, and cut self-descriptive or boilerplate lines. In the same pass, fix any em dash, stray semicolon, hedge word, throat-clearing opener, or boilerplate transition, whether it was already there or one of your own edits just introduced it (see "Skip on the way in" and "Punctuation" below). See "Cut slack, not substance" for what's off-limits. A cut only counts if it's a real Edit call, not reasoning about one without making it.
3. If step 2 made at least one edit and you're under 4 passes total, go back to step 1 for a new pass on the updated file. Otherwise, stop and move to the structural variance pass below.

A pass that makes zero Edit calls is the only valid signal of convergence. There's no separate ledger to keep: the edit history on the working file is the record.

## Skip on the way in

- Throat-clearing openers ("We wanted to let you know that...", "It's worth noting that...", "In terms of...").
- Restating what a heading, identifier, or the previous sentence already established.
- Hedge words that carry no information ("approximately", "generally", "as needed", "or so").
- The same point twice in different phrasing for emphasis.
- Boilerplate transitions ("Additionally,", "Furthermore,", "It should also be noted that").

## Punctuation

- No em dashes (—). Use a period, a comma, or parentheses first.
- Colons are a last resort, not a default way to introduce an example or elaboration. Try a period or comma before reaching for one.
- Semicolons are rare. Prefer a comma or two sentences unless the clauses are inseparable.
- One point per paragraph.

## Structural variance pass

Run this once, after the cut loop converges and before the fresh-reader gate. Skip it for a single paragraph or fewer than three parallel sections. There's nothing to vary against.

The cut loop tests each sentence in isolation, so a draft can converge while every paragraph still opens the same way, runs the same length, and follows the same claim-then-mechanism-then-payoff order. That repetition only shows up scanning the whole draft at once, not sentence by sentence.

Reread the draft as a sequence. Vary at least one paragraph or list item that repeats the same opening or length as its neighbors. Merge two points into one paragraph, front a clause instead of leading with the topic sentence, or drop the topic sentence and let the claim land mid-paragraph. Change enough that the sequence stops reading like a fill-in-the-blank template. Don't rewrite every instance. That reintroduces the same problem in a new shape.

Don't loop this against the cut loop. Fixing rhythm can add back a word the cut loop already removed, and re-running the cut loop on top of a structural edit risks flattening the variation back out.

## Fresh-reader gate

Your own reread can't test whether a cut lost substance: you still remember what you removed, so you can't judge what a reader landing on the text cold would be missing.

Once the loop above stops (by convergence or by hitting the 4-pass cap), spawn one fresh subagent, not a fork, with no access to this conversation. Run it on a fast, cheap model such as haiku, since a short draft doesn't need a frontier model to answer two questions. Give it the draft text and those two questions: what's confusing, and what information it would need that isn't there.

It gets nothing else: no context on the original ask, no knowledge of what got cut, no access to this skill's instructions. Do this once, as a final gate, not on every pass.

Skip this gate only if the draft is a single line or a single sentence (a commit subject, a one-line Slack ping, a one-line code comment). Anything longer goes through the gate, including a short bulleted list.

- If the fresh reader is missing information it needed, a cut went too far into substance: restore it with one corrective edit, then stop. Don't re-run the gate.
- If the fresh reader has no substantive complaint, the draft is done.

## Cut slack, not substance

The test for each candidate cut: remove or reword it, does the precise meaning survive? In prose, usually yes. In technical writing, the word you want to cut is sometimes the whole point.

Never cut from technical writing:

- warnings, gotchas, failure modes, and the reasoning behind a non-obvious decision
- exact flags, commands, paths, version numbers, error strings
- ordering and prerequisites
- context a reader landing mid-document needs. Reference docs reward restating. Prose punishes it.

When unsure whether something is slack or substance, keep it. A wasted sentence costs a reader seconds. A cut warning costs a support ticket.

From Stefan Zweig's The World of Yesterday:

```
I have hardly finished writing the first rough draft of a book before I begin on what to me is the real work, condensing my material and finding the right way to put it. I go on working tirelessly like this from draft to draft. I am constantly throwing ballast overboard, intensifying and clarifying a book's inner architecture. Most writers cannot bring themselves to leave anything out, and having fallen rather in love with their subject hope to display a greater breadth and depth of knowledge than they really possess in every well-turned line, whereas my own ambition is always to know more than shows on the outside.

Later, at the proof stages, I then repeat this process of intensifying and then enhancing the dramatic effect once, twice, or three times. In the end I find myself enjoying a kind of hunt for another sentence, or just a word, which can be cut without affecting my precise meaning and at the same time might speed up the tempo. I really get my greatest satisfaction in my work from leaving things out. I remember that once, when I rose from my desk feeling pleased with what I had done, my wife said I seemed to be in a cheerful mood today. "Yes," I replied proudly, "I've managed to cut a whole paragraph and make the action move faster." So if my books are sometimes praised for sweeping readers along at a swift pace, it does not come from any natural heated or agitated approach to the work of writing, but is entirely the result of my system of always cutting unnecessarily slack passages--anything at all that, like radio interference, might distract the reader's attention. If I have mastered any kind of art, it is the art of leaving things out. I do not mind throwing eight hundred of a thousand written pages into the waste-paper basket, leaving me with only two hundred to convey what I have sifted out as the essence of the work. So if anything at least partly accounts for the success of my books, it is my strict discipline in preferring to confine myself to short works of literate, concentrating on the heart of the matter.
```
