---
name: zweig-write
description: Write a first draft that's already dense. Load before drafting any prose: technical docs, PR descriptions, commit messages, code comments, briefs, Slack messages, even a single sentence. No triviality exception. zweig-refine is a separate, deeper cutting pass, run only on explicit request.
---

# Zweig Write

Write every sentence to survive the question zweig-refine asks later: cut this, does the reader lose something, or just words? A denser draft means that loop converges faster.

zweig-refine's loop and fresh-reader gate catch more than this skill can, since a drafting context can't see its own blind spots. Once a draft is ready, ask the user whether to run zweig-refine on it next, and run it only if they say yes.

## Before drafting

Warnings, gotchas, failure modes, exact flags, commands, paths, versions, error strings, ordering, and context a reader landing mid-document needs: all of it has to survive into the first draft. Density is not a license to omit any of it.

## While drafting, skip these on the way in

- Throat-clearing openers ("We wanted to let you know that...", "It's worth noting that...", "In terms of...").
- Restating what a heading, identifier, or the previous sentence already established.
- Hedge words that carry no information ("approximately", "generally", "as needed", "or so").
- The same point twice in different phrasing for emphasis.
- Boilerplate transitions ("Additionally,", "Furthermore,", "It should also be noted that").

One idea per sentence. Prefer fewer, denser points over broad coverage.

## Punctuation

- No em dashes (—). Use a period, a comma, or parentheses first.
- Colons are a last resort, not a default way to introduce an example or elaboration. Try a period or comma before reaching for one.
- Semicolons are rare. Prefer a comma or two sentences unless the clauses are inseparable.
- One point per paragraph.
