<div align="center">

<img src="assets/zweig.svg" width="420" alt="Portrait of Stefan Zweig drawn in Braille dots">

**_"If I have mastered any kind of art, it is the art of leaving things out."_**
<br><sub>Stefan Zweig, <i>The World of Yesterday</i></sub>

[![Release](https://img.shields.io/github/v/release/rornic/zweig?style=flat-square&color=2b2b2b)](https://github.com/rornic/zweig/releases)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-d97757?style=flat-square)](#install)
[![Codex](https://img.shields.io/badge/Codex-plugin-10a37f?style=flat-square)](#install)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

</div>

---

Your agent writes too much. Zweig makes it write like a novelist who threw away eight hundred of every thousand pages.

Two writing skills for Claude Code and Codex, built on Stefan Zweig's drafting process. Write dense, then cut to intensify.

## Before and after

A real run of `zweig-refine`, from [`EXAMPLE.md`](skills/zweig-refine/EXAMPLE.md).

**Before** (105 words)

> We wanted to let you know that, in terms of the deployment process, the new deployment process now requires that you first run the build step before you can proceed to run the actual deploy step, which is a change from how it used to work before this change was made. Additionally, it should also be noted that the build step, which is a new step, will take approximately five minutes or so to complete on average, and during this time you should just wait for it to finish before doing anything else, since trying to deploy before the build step has finished will simply result in an error message being shown to you.

**After** (25 words)

> Deployment now requires a build step (~5 min) before the deploy step. The deploy step is blocked with an error until the build finishes.

Every instruction survives. The last fix came from a blind reviewer who caught an ambiguity three self-review passes missed.

## The skills

### ✍️ `zweig-write`

Loads automatically before your agent drafts any prose (docs, PR descriptions, commit messages, code comments, Slack messages). Throat-clearing, hedges, restatement, and boilerplate transitions never make it onto the page. Commands, flags, warnings, and failure modes always do.

### ✂️ `zweig-refine`

1. **Cut.** Every removable word, phrase, or sentence goes, as a real edit against a real file.
2. **Repeat.** Reread and cut until a pass makes zero edits (4 passes max).
3. **Fresh-reader gate.** A separate subagent, blind to the conversation that produced the draft, reads only the final text and flags anything confusing or missing.

The gate exists because the context that made the cuts can't see its own blind spots.

`zweig-write` offers to run it once a draft is done. Or ask any time ("refine this", "tighten the README").

## Install

**Claude Code**

```
/plugin marketplace add rornic/zweig
/plugin install zweig@zweig
```

**Codex**

```
codex plugin marketplace add rornic/zweig
codex plugin add zweig@zweig
```

## The quote

The whole method, in Zweig's words, from *The World of Yesterday*.

<details>
<summary><b>Read the passage</b></summary>
<br>

> I have hardly finished writing the first rough draft of a book before I begin on what to me is the real work, condensing my material and finding the right way to put it. I go on working tirelessly like this from draft to draft. I am constantly throwing ballast overboard, intensifying and clarifying a book's inner architecture. Most writers cannot bring themselves to leave anything out, and having fallen rather in love with their subject hope to display a greater breadth and depth of knowledge than they really possess in every well-turned line, whereas my own ambition is always to know more than shows on the outside.
>
> Later, at the proof stages, I then repeat this process of intensifying and then enhancing the dramatic effect once, twice, or three times. In the end I find myself enjoying a kind of hunt for another sentence, or just a word, which can be cut without affecting my precise meaning and at the same time might speed up the tempo. I really get my greatest satisfaction in my work from leaving things out. I remember that once, when I rose from my desk feeling pleased with what I had done, my wife said I seemed to be in a cheerful mood today. "Yes," I replied proudly, "I've managed to cut a whole paragraph and make the action move faster." So if my books are sometimes praised for sweeping readers along at a swift pace, it does not come from any natural heated or agitated approach to the work of writing, but is entirely the result of my system of always cutting unnecessarily slack passages--anything at all that, like radio interference, might distract the reader's attention. If I have mastered any kind of art, it is the art of leaving things out. I do not mind throwing eight hundred of a thousand written pages into the waste-paper basket, leaving me with only two hundred to convey what I have sifted out as the essence of the work. So if anything at least partly accounts for the success of my books, it is my strict discipline in preferring to confine myself to short works of literate, concentrating on the heart of the matter.

</details>

## License

MIT
