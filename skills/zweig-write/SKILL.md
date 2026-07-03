---
name: zweig-write
description: Write a first draft that's already dense, so the zweig-refine loop converges in as few passes as possible. Load before starting a first draft of any prose (technical documentation, PR descriptions, commit messages, code comments, briefs, Slack messages). Does not replace zweig-refine: hand the draft to that skill once it exists.
---

# Zweig Write

Write every sentence to survive the question zweig-refine asks later: cut this, does the reader lose something, or just words? A denser draft means that loop converges faster.

Hand every non-trivial draft to zweig-refine once it exists. This skill only front-loads the cutting: the loop and fresh-reader gate still run, because a drafting context can't see its own blind spots.

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

- No em dashes (—). Use a period, a comma, or parentheses first. A colon works too, but treat it as the last option, not the default.
- Semicolons are rare. Prefer a comma or two sentences unless the clauses are inseparable.
- One point per paragraph. At most one colon per paragraph, introducing that point. A paragraph that already has one doesn't get a second, split it instead.
