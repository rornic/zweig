# Example: the loop in action

Companion to `SKILL.md` in this directory, which defines the loop, the fresh-reader exemption threshold, and the "never cut" list. This is a real transcript of that loop running end to end, kept here so the mechanism is verifiable, not just asserted.

## Starting draft

A deliberately padded paragraph, written to a real file:

> We wanted to let you know that, in terms of the deployment process, the new deployment process now requires that you first run the build step before you can proceed to run the actual deploy step, which is a change from how it used to work before this change was made. Additionally, it should also be noted that the build step, which is a new step, will take approximately five minutes or so to complete on average, and during this time you should just wait for it to finish before doing anything else, since trying to deploy before the build step has finished will simply result in an error message being shown to you.

105 words, one idea.

## Pass 1

Read the file, then cut every removable sentence and phrase with real Edit calls, targeting throat-clearing ("We wanted to let you know that"), restated framing ("which is a change from how it used to work before this change was made"), and hedge words ("approximately", "or so", "on average").

> Deployment now requires a build step before the deploy step. The build step takes about five minutes; deploying before it finishes will show an error message.

26 words. One edit made. The loop continues.

## Pass 2

Reread the updated file. "The build step" appears twice. The two sentences can merge without losing anything.

> Deployment now requires a build step (~5 min) before the deploy step. Deploying before the build finishes shows an error.

One more edit, so the loop runs again.

## Pass 3

Reread again. Every remaining word carries information. The ordering, the timing, and the failure mode are all substance the "never cut from technical writing" list protects. No edit is made this pass.

**Zero edits on this pass is the convergence signal.** The loop stops here, not because a self-report said so, but because the transcript shows no Edit call happened.

## Fresh-reader gate

The draft is two sentences, so it's not exempt. A subagent is spawned with nothing but the pass-3 text, no memory of the original 105 words, no knowledge of what got cut. It's asked what's confusing and what information it would need.

It flagged something real: "shows an error" is ambiguous. Does the deploy get blocked, or does it just warn and continue? Three self-review passes missed this, because the self-reviewer already knew the intended meaning and read past the ambiguity every time. A reader meeting the text cold couldn't.

## Corrective edit

One edit, addressing the flagged gap, then stop, with no re-running the loop or the gate:

> Deployment now requires a build step (~5 min) before the deploy step. The deploy step is blocked with an error until the build finishes.

## Why this matters

The gate caught a real gap that survived every self-review pass. The context that made the cuts is structurally unable to notice what a fresh reader would miss, no matter how carefully it's asked to imagine one.
