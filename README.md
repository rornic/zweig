# zweig

Writing skills for Claude Code and Codex CLI, based on Stefan Zweig's drafting process described in The World of Yesterday. Write dense, then cut to intensify.

## What's included

- **zweig-write**: drafts prose that's already dense, so zweig-refine below needs fewer passes.
- **zweig-refine**: the cut-draft-repeat loop. Reads a working draft, cuts slack without cutting substance, repeats until a pass makes zero edits (capped at 4 passes), then runs a fresh-reader gate: a separate subagent, blind to the conversation that produced the draft, checks the draft text itself for confusion or missing information.

Neither needs a slash command. `zweig-write` loads automatically before drafting any prose, then asks whether to run `zweig-refine` on the result. `zweig-refine` also runs any other time you ask for it directly. See [`skills/zweig-refine/EXAMPLE.md`](skills/zweig-refine/EXAMPLE.md) for a worked transcript of the refine loop end to end.

## Install

Claude Code:

```
/plugin marketplace add rornic/zweig
/plugin install zweig@zweig
```

Codex CLI (requires Codex CLI >= 0.142.0):

```
codex plugin marketplace add rornic/zweig
```

Then install `zweig` from the plugins list (`/plugins` in the CLI, or the Plugins panel in the app).

## The quote

From Stefan Zweig's The World of Yesterday:

> I have hardly finished writing the first rough draft of a book before I begin on what to me is the real work, condensing my material and finding the right way to put it. I go on working tirelessly like this from draft to draft. I am constantly throwing ballast overboard, intensifying and clarifying a book's inner architecture. Most writers cannot bring themselves to leave anything out, and having fallen rather in love with their subject hope to display a greater breadth and depth of knowledge than they really possess in every well-turned line, whereas my own ambition is always to know more than shows on the outside.
>
> Later, at the proof stages, I then repeat this process of intensifying and then enhancing the dramatic effect once, twice, or three times. In the end I find myself enjoying a kind of hunt for another sentence, or just a word, which can be cut without affecting my precise meaning and at the same time might speed up the tempo. I really get my greatest satisfaction in my work from leaving things out. I remember that once, when I rose from my desk feeling pleased with what I had done, my wife said I seemed to be in a cheerful mood today. "Yes," I replied proudly, "I've managed to cut a whole paragraph and make the action move faster." So if my books are sometimes praised for sweeping readers along at a swift pace, it does not come from any natural heated or agitated approach to the work of writing, but is entirely the result of my system of always cutting unnecessarily slack passages--anything at all that, like radio interference, might distract the reader's attention. If I have mastered any kind of art, it is the art of leaving things out. I do not mind throwing eight hundred of a thousand written pages into the waste-paper basket, leaving me with only two hundred to convey what I have sifted out as the essence of the work. So if anything at least partly accounts for the success of my books, it is my strict discipline in preferring to confine myself to short works of literate, concentrating on the heart of the matter.

## License

MIT
