---
name: zweig-write
description: Write a first draft that's already dense, so the zweig-refine loop converges in as few passes as possible. Load before starting a first draft of any prose (technical documentation, PR descriptions, commit messages, code comments, briefs, Slack messages). Does not replace zweig-refine: hand the draft to that skill once it exists.
---

# Zweig Write

Write every sentence to survive the question zweig-refine asks later: cut this, does the reader lose something, or just words? A denser draft means that loop converges faster.

Hand every non-trivial draft to zweig-refine once it exists. This skill only front-loads the cutting: the loop and fresh-reader gate still run, because a drafting context can't see its own blind spots.

## Before drafting

Read `../STYLE.md` in full. Its "Skip these on the way in" and "Punctuation" rules govern every sentence you write. Its "Cut slack, not substance" section is what you're writing *for*: warnings, gotchas, failure modes, exact flags, commands, paths, versions, error strings, ordering, and context a reader landing mid-document needs all have to survive into the first draft. Density is not a license to omit any of it.
