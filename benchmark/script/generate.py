#!/usr/bin/env python3
"""Generate plain and zweig-write drafts, then refine each zweig-write draft."""

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_DIR = SCRIPT_DIR.parent

CONDITIONS = {
    "claude-plain": ["--safe-mode"],
    "claude-zweig-write": [
        "--append-system-prompt",
        "Use the zweig-write skill while drafting this. Your final response must contain the deliverable "
        "text ONLY: no preamble sentence describing the drafting process or mentioning zweig-write.",
    ],
}

REFINE_CONDITION = "claude-zweig-refine"
REFINE_FLAGS = [
    "--append-system-prompt",
    "Use the zweig-refine skill on the supplied draft. Your final response must contain the refined "
    "deliverable text ONLY: no preamble sentence describing refinement or mentioning zweig-refine, the "
    "fresh-reader gate, or any subagent.",
]

BASE_FLAGS = [
    "--output-format", "json",
    "--permission-mode", "bypassPermissions",
    "--no-session-persistence",
]


def index_by_theme(prompts: list[dict]) -> list[dict]:
    """Assign each prompt a 0-based index within its theme, computed on the
    full unfiltered list so numbering stays stable across filtered runs."""
    counters: dict[str, int] = {}
    indexed = []
    for item in prompts:
        theme = item["theme"]
        idx = counters.get(theme, 0)
        counters[theme] = idx + 1
        indexed.append({**item, "idx": idx})
    return indexed


def prompt_with_length_target(item: dict) -> str:
    minimum, maximum = item["target_words"]
    return (
        f"{item['prompt']}\n\n"
        f"Aim for {minimum}–{maximum} words. Be concise, but do not omit information needed to fulfil "
        "the request."
    )


META_MARKERS = ("zweig-write", "zweig-refine", "fresh-reader", "subagent")


def strip_meta_commentary(text: str) -> tuple[str, bool]:
    """Drop a leading paragraph narrating the zweig-write/zweig-refine process
    instead of being the deliverable itself. The model sometimes adds this
    despite being told not to (see benchmark plan verification notes); this is
    the safety net, not the primary fix."""
    paragraphs = text.split("\n\n", 1)
    if len(paragraphs) == 2 and any(m in paragraphs[0].lower() for m in META_MARKERS):
        return paragraphs[1].lstrip("\n"), True
    return text, False


def is_broken_response(text: str) -> bool:
    """Catch the rarer failure where the whole response is a stray process
    note (e.g. a misfired subagent narrating itself) with no deliverable at
    all, not just a leading paragraph strip_meta_commentary can lop off."""
    return len(text.split()) < 50 and any(m in text.lower() for m in META_MARKERS)


def run_condition(prompt: str, model: str, flags: list[str], timeout: int) -> dict:
    cmd = ["claude", "-p", prompt, "--model", model, *BASE_FLAGS, *flags]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:500]}")
    return json.loads(proc.stdout)


def token_usage(response: dict) -> dict:
    """Token counts, not $: cost-per-token drifts with pricing changes, token
    counts for a given prompt/condition pair don't."""
    usage = response.get("usage", {})
    input_tokens = usage.get("input_tokens", 0)
    cache_creation = usage.get("cache_creation_input_tokens", 0)
    cache_read = usage.get("cache_read_input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    return {
        "input_tokens": input_tokens,
        "cache_creation_input_tokens": cache_creation,
        "cache_read_input_tokens": cache_read,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + cache_creation + cache_read + output_tokens,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompts", default=str(BENCHMARK_DIR / "prompts.json"))
    parser.add_argument("--out", default=str(BENCHMARK_DIR / "out"))
    parser.add_argument("--model", default="sonnet")
    parser.add_argument("--themes", help="comma-separated theme filter")
    parser.add_argument("--ids", help="comma-separated prompt id filter")
    parser.add_argument("--limit", type=int, help="max prompts to run, applied after filtering")
    parser.add_argument("--force", action="store_true", help="regenerate even if output already exists")
    parser.add_argument("--timeout", type=int, default=300, help="per-call timeout in seconds")
    args = parser.parse_args()

    prompts = index_by_theme(json.loads(Path(args.prompts).read_text()))

    if args.themes:
        wanted = set(args.themes.split(","))
        prompts = [p for p in prompts if p["theme"] in wanted]
    if args.ids:
        wanted = set(args.ids.split(","))
        prompts = [p for p in prompts if p["id"] in wanted]
    if args.limit:
        prompts = prompts[: args.limit]

    if not prompts:
        print("No prompts matched the given filters.", file=sys.stderr)
        sys.exit(1)

    out_root = Path(args.out)
    tokens_by_condition = {condition: 0 for condition in [*CONDITIONS, REFINE_CONDITION]}

    for condition in CONDITIONS:
        for item in prompts:
            theme_dir = out_root / condition / item["theme"]
            theme_dir.mkdir(parents=True, exist_ok=True)
            md_path = theme_dir / f"{item['idx']}.md"
            json_path = theme_dir / f"{item['idx']}.json"
            label = f"{condition}/{item['theme']}/{item['idx']} ({item['id']})"

            if md_path.exists() and json_path.exists() and not args.force:
                print(f"skip  {label}")
                continue

            print(f"run   {label}...", end=" ", flush=True)
            try:
                generation_prompt = prompt_with_length_target(item)
                response = run_condition(generation_prompt, args.model, CONDITIONS[condition], args.timeout)
            except Exception as exc:
                print(f"FAILED: {exc}")
                continue

            if response.get("is_error"):
                print(f"FAILED: {response.get('result')}")
                continue

            result_text, stripped = strip_meta_commentary(response.get("result", ""))
            if is_broken_response(result_text):
                print(f"FAILED: response has no deliverable, just a process note: {result_text[:200]!r}")
                continue
            usage = token_usage(response)
            record = {
                "id": item["id"],
                "theme": item["theme"],
                "condition": condition,
                "prompt": generation_prompt,
                "target_words": item["target_words"],
                "meta_commentary_stripped": stripped,
                "token_usage": usage,
                "response": response,
            }
            json_path.write_text(json.dumps(record, indent=2))
            md_path.write_text(result_text)
            tokens_by_condition[condition] += usage["total_tokens"]
            note = " [stripped meta-commentary]" if stripped else ""
            print(f"ok ({usage['output_tokens']} out / {usage['total_tokens']} total tok){note}")

    for item in prompts:
        source_path = out_root / "claude-zweig-write" / item["theme"] / f"{item['idx']}.md"
        theme_dir = out_root / REFINE_CONDITION / item["theme"]
        theme_dir.mkdir(parents=True, exist_ok=True)
        md_path = theme_dir / f"{item['idx']}.md"
        json_path = theme_dir / f"{item['idx']}.json"
        label = f"{REFINE_CONDITION}/{item['theme']}/{item['idx']} ({item['id']})"

        if md_path.exists() and json_path.exists() and not args.force:
            print(f"skip  {label}")
            continue
        if not source_path.is_file():
            print(f"skip  {label}: missing zweig-write draft")
            continue

        generation_prompt = prompt_with_length_target(item)
        refine_prompt = (
            f"Original request:\n{generation_prompt}\n\n"
            f"Draft to refine:\n{source_path.read_text()}"
        )
        print(f"run   {label}...", end=" ", flush=True)
        try:
            response = run_condition(refine_prompt, args.model, REFINE_FLAGS, args.timeout)
        except Exception as exc:
            print(f"FAILED: {exc}")
            continue

        if response.get("is_error"):
            print(f"FAILED: {response.get('result')}")
            continue

        result_text, stripped = strip_meta_commentary(response.get("result", ""))
        if is_broken_response(result_text):
            print(f"FAILED: response has no deliverable, just a process note: {result_text[:200]!r}")
            continue
        usage = token_usage(response)
        record = {
            "id": item["id"],
            "theme": item["theme"],
            "condition": REFINE_CONDITION,
            "prompt": generation_prompt,
            "target_words": item["target_words"],
            "source_condition": "claude-zweig-write",
            "meta_commentary_stripped": stripped,
            "token_usage": usage,
            "response": response,
        }
        json_path.write_text(json.dumps(record, indent=2))
        md_path.write_text(result_text)
        tokens_by_condition[REFINE_CONDITION] += usage["total_tokens"]
        note = " [stripped meta-commentary]" if stripped else ""
        print(f"ok ({usage['output_tokens']} out / {usage['total_tokens']} total tok){note}")

    print("\nTotal tokens this run:")
    for condition, total in tokens_by_condition.items():
        print(f"  {condition}: {total:,} tok")


if __name__ == "__main__":
    main()
