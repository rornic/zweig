<div align="center">

<img src="assets/zweig.svg" width="420" alt="Portrait of Stefan Zweig drawn in Braille dots">

_"If I have mastered any kind of art, it is the art of leaving things out."_
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

One prompt, three runs: *"Write a PR description for a change that adds a token-bucket rate limiter to an internal API gateway, replacing a fixed-window limiter that was causing bursty 429s."*

<details>
<summary><b>Plain Claude</b> (303 words)</summary>

```markdown
## Replace fixed-window rate limiter with token-bucket in API gateway

### Summary

The gateway's fixed-window rate limiter resets its counter at fixed interval boundaries (e.g., every 60s), which allows clients to burst up to 2x their limit by sending requests at the tail of one window and the head of the next. Under load, this produced spiky, bursty `429` responses instead of a smooth throttling curve — clients would sail through for most of a window, then get slammed near the boundary.

This PR replaces the fixed-window limiter with a token-bucket implementation, which smooths request admission over time while still permitting short bursts up to the configured bucket size.

### Changes

- New `TokenBucketLimiter` implementing the existing `RateLimiter` interface, backed by a per-client bucket with configurable `capacity` and `refillRate` (tokens/sec).
- Bucket state stored in Redis with an atomic Lua script for check-and-decrement to avoid race conditions under concurrent requests to the same client key.
- Removed `FixedWindowLimiter` and its associated window-reset scheduler.
- Config: `rateLimit.window` / `rateLimit.maxRequests` replaced with `rateLimit.capacity` / `rateLimit.refillRate`; migration mapping added to config loader so existing deployments don't need a manual config rewrite (old keys log a deprecation warning and are converted).
- `Retry-After` header now computed from time-to-next-token rather than time-to-window-reset, giving clients more accurate backoff guidance.

### Testing

- Unit tests covering burst absorption, steady-state throttling, and concurrent-request race conditions on the Lua script.
- Load-tested against staging gateway at 3x normal traffic; confirmed 429 rate dropped from ~18% (bursty spikes) to ~4% (smooth, at configured limit) with no increase in overall rejected-request count.
- Verified config migration path against a copy of prod config.

### Rollout

Deploying behind the existing `rate-limiter-v2` feature flag, default off. Plan to enable for one low-traffic internal service first, monitor `429` and latency dashboards for 24h, then roll out broadly.
```

</details>

<details>
<summary><b>With zweig-write</b> (189 words)</summary>

```markdown
## Summary

- Replace the fixed-window rate limiter with a token-bucket limiter on the API gateway.
- Fixed-window resets allowed a client to burst up to 2x its limit across a window boundary (all of the previous window's quota at 23:59, all of the next window's at 00:00), which triggered clustered 429s downstream as those bursts hit backend services at once.
- Token bucket refills continuously, so allowed throughput smooths out and clients see 429s spread proportionally to sustained load instead of in spikes.
- Bucket capacity and refill rate are configured per client tier, matching the previous window size and request quota so default limits are unchanged.
- Existing 429 response headers (`Retry-After`, `X-RateLimit-Remaining`) are preserved; `X-RateLimit-Remaining` now reflects available tokens instead of window count.

## Test plan

- [ ] Unit tests for bucket refill math, including fractional token accrual and capacity clamping.
- [ ] Load test comparing 429 distribution under bursty traffic against the old limiter.
- [ ] Verify per-tier limits are unchanged for a client sending steady, non-bursty traffic.
- [ ] Confirm `Retry-After` and `X-RateLimit-Remaining` headers stay correct at the bucket boundary.
```

</details>

<details>
<summary><b>zweig-write, then zweig-refine</b> (166 words)</summary>

```markdown
## Summary

- Replace the API gateway's fixed-window rate limiter with a token bucket.
- Fixed-window resets let a client burst to 2x its limit, all of the previous window's quota at 23:59 and all of the next window's at 00:00, slamming backend services with clustered 429s.
- Token bucket refills continuously, so throughput smooths out and 429s scale with sustained load instead of spiking at boundaries.
- Bucket capacity and refill rate are set per client tier, matching the old window size and quota, so default limits are unchanged.
- Existing 429 headers (`Retry-After`, `X-RateLimit-Remaining`) are preserved. `X-RateLimit-Remaining` now reflects available tokens instead of window count.

## Test plan

- [ ] Unit tests for bucket refill math, including fractional token accrual and capacity clamping.
- [ ] Load test comparing 429 distribution under bursty traffic against the old limiter.
- [ ] Verify per-tier limits are unchanged under steady traffic.
- [ ] Confirm `Retry-After` and `X-RateLimit-Remaining` headers stay correct at the bucket boundary.
```

</details>

`zweig-write` produces a separate draft, not an edit of the plain one, so the two differ in detail as well as density. `zweig-refine` edits the `zweig-write` draft in place. For a full transcript of the refine loop, see [`EXAMPLE.md`](skills/zweig-refine/EXAMPLE.md).

## The skills

### `zweig-write`

Loads automatically before your agent drafts any prose (docs, PR descriptions, commit messages, code comments, Slack messages). Throat-clearing, hedges, restatement, boilerplate transitions, and decorative emoji never make it onto the page. Commands, flags, warnings, and failure modes always do.

### `zweig-refine`

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
