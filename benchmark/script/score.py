#!/usr/bin/env python3
"""Score generated benchmark output against zweig-write's own checkable rules.

No LLM judging: every metric here maps to an explicit rule in
skills/zweig-write/SKILL.md, computed deterministically from the text itself.
"""

import argparse
import csv
import json
import re
import statistics
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_DIR = SCRIPT_DIR.parent

CODE_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_BLOCK_MARKER_RE = re.compile(r"^(#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s+)")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")
WORD_RE = re.compile(r"[A-Za-z']+")

# "Hedge words that carry no information" (SKILL.md), plus a small extension
# of standard hedge/weasel terms in the same spirit.
FILLER_PHRASES = [
    "approximately", "generally", "as needed", "or so",
    "somewhat", "fairly", "quite", "in order to", "basically", "essentially",
]

def strip_code(text: str) -> str:
    text = CODE_FENCE_RE.sub(" ", text)
    return INLINE_CODE_RE.sub(" ", text)


def close_markdown_blocks(text: str) -> str:
    """Force a sentence boundary at each markdown block (header, list item,
    blockquote line), since none of those reliably end in terminal
    punctuation. Without this, a header with no period fuses into the
    following paragraph as one "sentence" under SENTENCE_SPLIT_RE, wildly
    inflating words_per_sentence and p95_sentence_length on structured docs
    (PR bodies, runbooks) versus prose (short stories)."""
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        marker = MARKDOWN_BLOCK_MARKER_RE.match(stripped)
        content = stripped[marker.end():] if marker else stripped
        if content and content[-1] not in ".!?:;":
            content += "."
        lines.append(content)
    return "\n".join(lines)


def count_phrases(text: str, phrases: list[str]) -> int:
    lowered = text.lower()
    return sum(lowered.count(phrase) for phrase in phrases)


def p95(values: list[int]) -> float:
    """95th percentile of the document's own sentence lengths, not a fixed
    word-count cutoff: self-calibrating per document instead of an arbitrary
    "long sentence" threshold with no basis in SKILL.md or any distribution."""
    if not values:
        return 0.0
    if len(values) == 1:
        return float(values[0])
    return statistics.quantiles(values, n=100, method="inclusive")[94]


def output_tokens(md_path: Path) -> int | None:
    """Output tokens only, not total: input/cache tokens are mostly re-read
    skill/system-prompt overhead, not what an API bills per-generation on."""
    json_path = md_path.with_suffix(".json")
    if not json_path.is_file():
        return None
    record = json.loads(json_path.read_text())
    return record.get("token_usage", {}).get("output_tokens")


def score_text(raw_text: str) -> dict:
    prose = strip_code(raw_text)
    prose_word_count = max(len(WORD_RE.findall(prose)), 1)
    word_count_total = len(WORD_RE.findall(raw_text))

    sentences = [
        s for s in SENTENCE_SPLIT_RE.split(close_markdown_blocks(prose).strip()) if s.strip()
    ]
    sentence_count = max(len(sentences), 1)
    sentence_word_counts = [len(WORD_RE.findall(sentence)) for sentence in sentences]

    filler = count_phrases(prose, FILLER_PHRASES)
    em_dash = prose.count("—")
    colon = prose.count(":")
    semicolon = prose.count(";")

    def per_1000_words(n: int) -> float:
        return round(n * 1000 / prose_word_count, 2)

    return {
        "word_count": word_count_total,
        "words_per_sentence": round(prose_word_count / sentence_count, 2),
        "p95_sentence_length": round(p95(sentence_word_counts), 2),
        "filler_rate": per_1000_words(filler),
        "em_dash_rate": per_1000_words(em_dash),
        "colon_rate": per_1000_words(colon),
        "semicolon_rate": per_1000_words(semicolon),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(BENCHMARK_DIR / "out"))
    parser.add_argument("--results", default=str(BENCHMARK_DIR / "results" / "scores.csv"))
    args = parser.parse_args()

    out_root = Path(args.out)
    rows = []

    for md_path in sorted(out_root.glob("*/*/*.md")):
        condition = md_path.parents[1].name
        theme = md_path.parent.name
        idx = md_path.stem
        text = md_path.read_text()
        if not text.strip():
            print(f"skip  {condition}/{theme}/{idx}: empty file")
            continue
        row = {"theme": theme, "id": idx, "condition": condition}
        row.update(score_text(text))
        if tokens := output_tokens(md_path):
            row["output_tokens"] = tokens
        rows.append(row)

    if not rows:
        print("No generated .md files found under", out_root)
        return

    results_path = Path(args.results)
    results_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "theme", "id", "condition", "word_count", "output_tokens", "words_per_sentence",
        "p95_sentence_length", "filler_rate", "em_dash_rate", "colon_rate", "semicolon_rate",
    ]
    with results_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Scored {len(rows)} files -> {results_path}")


if __name__ == "__main__":
    main()
