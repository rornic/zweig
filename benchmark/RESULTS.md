# Benchmark results: does zweig-write / zweig-refine actually help?

30 prompts (10 each across technical docs, short stories, PR bodies), each run three ways: plain Claude, Claude with zweig-write, and zweig-write refined through zweig-refine. Every metric checks an explicit rule from `skills/zweig-write/SKILL.md` directly against the text (word counts, punctuation frequency, sentence length) rather than an LLM judge scoring its own homework. Full methodology, scripts, and raw data: `script/`, `prompts.json`, `results/scores.csv`. Chart: `results/comparison.png`.

## Results

| metric | plain | zweig-write | zweig-refine |
|---|---|---|---|
| output tokens / response | 922 | 860 | 9,712 |
| em dashes / 1,000 words | 8.96 | 0.36 | 0.00 |
| colons / 1,000 words | 8.19 | 5.60 | 2.90 |
| semicolons / 1,000 words | 2.65 | 1.25 | 0.07 |
| words / sentence | 21.6 | 19.6 | 17.7 |
| p95 sentence length (words) | 48.1 | 40.2 | 37.6 |

A dashed reference line on the chart marks Stefan Zweig's own prose (a 1,046-word excerpt from *The World of Yesterday*), for scale, not as a target: an AI draft matching his p95 sentence length isn't the goal, seeing where the AI conditions land relative to a real writer's is.

## zweig-write is close to free

It costs fewer output tokens than a plain draft (860 vs. 922), because writing tighter the first time beats writing more and cutting later. It also does exactly what it says: em dashes drop 96% (8.96 to 0.36 per 1,000 words), colons and semicolons both roughly halve. If a skill this cheap reliably enforces the rules it claims to enforce, there's no case against leaving it on by default, which is exactly how it ships (loads automatically before any prose).

## zweig-refine costs 10x. It also does real work, not busywork

9,712 output tokens against zweig-write's 860. That's the number to sit with before reaching for it. But it isn't 10x the cost for 0x the result: colons keep dropping where write's single pass plateaus (5.60 to 2.90), semicolons nearly disappear (1.25 to 0.07), and the cut loop catches things a first pass structurally can't see. One technical doc had a template-y, repetitive bullet structure after zweig-write; refine's structural variance pass fixed it completely. That's the fresh-reader gate and the iterative cut loop doing their actual job, not token-burning for cosmetic churn.

## Use it wisely

zweig-write: leave it on, it's free and it works. zweig-refine: worth it for anything a reader will sit with, a runbook, a doc people will actually read closely, this post. Not worth it for a Slack message or a routine PR description, where a tight first draft already clears the bar. The 10x cost is real. So is what it buys.

## What this doesn't measure

Every metric here checks the skill's own explicit, mechanical rules (no em dashes, sentence length, hedge words). None of it checks whether the writing is actually good, correct, or something a reader would prefer, that's a different, harder benchmark. n=10 per theme, one run per condition, no repeat sampling: these are directional results, not statistically tight ones. And `repeated_sentence_rate` was cut from this benchmark entirely after an early version flagged a deliberate literary refrain in a short story as a defect: duplicate-phrase detection can't tell padding from a writer repeating a line on purpose.
