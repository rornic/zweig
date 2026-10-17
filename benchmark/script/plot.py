#!/usr/bin/env python3
"""Plot mean zweig-write rule-adherence metrics per theme and condition.

Blue is plain Claude, orange is zweig-write, green is zweig-refine. A dashed
violet line marks Stefan Zweig's own reference text on ratio-metric panels
only (word count and token count aren't comparable to a full memoir).
"""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SCRIPT_DIR = Path(__file__).resolve().parent
BENCHMARK_DIR = SCRIPT_DIR.parent

METRICS = [
    ("word_count", "Word count (log scale)"),
    ("output_tokens", "Output tokens / response (log scale)"),
    ("words_per_sentence", "Words / sentence"),
    ("p95_sentence_length", "p95 sentence length (words)"),
    ("filler_rate", "Filler words / 1,000 words"),
    ("em_dash_rate", "Em dashes / 1,000 words"),
    ("colon_rate", "Colons / 1,000 words"),
    ("semicolon_rate", "Semicolons / 1,000 words"),
]

CONDITION_COLOR = {
    "claude-plain": "#2a78d6",
    "claude-zweig-write": "#eb6834",
    "claude-zweig-refine": "#438a5e",
}
# Not a bar condition: a single-document style reference, shown as a dashed
# line on ratio metrics only. word_count/output_tokens aren't comparable
# (a full memoir vs. one short generation), so it's excluded from those.
REFERENCE_CONDITION = "stefan-zweig"
REFERENCE_LABEL = "stefan zweig (reference)"
REFERENCE_COLOR = "#4a3aa7"
COUNT_METRICS = {"word_count", "output_tokens"}
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e2e0da"


def load_scores(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open()))
    if not rows:
        raise SystemExit(f"No rows in {path}")
    return rows


def paired_rows(rows: list[dict], conditions: list[str]) -> list[dict]:
    grouped: dict[tuple[str, str], dict[str, dict]] = defaultdict(dict)
    for row in rows:
        if row["condition"] in conditions:
            grouped[(row["theme"], row["id"])][row["condition"]] = row
    return [
        grouped_pair[condition]
        for grouped_pair in grouped.values()
        if all(condition in grouped_pair for condition in conditions)
        for condition in conditions
    ]


def reference_values(rows: list[dict]) -> dict:
    """Mean of each ratio metric across all reference-condition rows (one
    today; averages cleanly if more reference texts are added later)."""
    matching = [row for row in rows if row["condition"] == REFERENCE_CONDITION]
    values = {}
    for metric, _ in METRICS:
        if metric in COUNT_METRICS:
            continue
        vals = [float(row[metric]) for row in matching if row.get(metric)]
        if vals:
            values[metric] = sum(vals) / len(vals)
    return values


def aggregate(rows: list[dict]):
    agg = {m: defaultdict(lambda: defaultdict(list)) for m, _ in METRICS}
    themes: list[str] = []
    for row in rows:
        theme = row["theme"]
        if theme not in themes:
            themes.append(theme)
        for metric, _ in METRICS:
            if row.get(metric):
                agg[metric][theme][row["condition"]].append(float(row[metric]))
    means = {
        metric: {
            theme: {cond: sum(vals) / len(vals) for cond, vals in conds.items()}
            for theme, conds in theme_map.items()
        }
        for metric, theme_map in agg.items()
    }
    return means, sorted(themes)


def plot(
    means: dict,
    themes: list[str],
    conditions: list[str],
    reference: dict,
    out_path: Path,
    title: str,
    model: str,
) -> None:
    condition_label = {
        "claude-plain": model,
        "claude-zweig-write": f"{model} w/ zweig-write",
        "claude-zweig-refine": f"{model} w/ zweig-refine",
    }
    fig, axes = plt.subplots(3, 3, figsize=(15, 11), facecolor=SURFACE)
    fig.suptitle(
        title,
        color=TEXT_PRIMARY, fontsize=13, fontweight="bold",
    )

    bar_width = 0.25
    x = range(len(themes))

    for ax, (metric, label) in zip(axes.flat, METRICS):
        ax.set_facecolor(SURFACE)
        alpha = 1.0

        for i, cond in enumerate(conditions):
            offset = (i - (len(conditions) - 1) / 2) * bar_width
            values_by_theme = [means[metric].get(theme, {}).get(cond) for theme in themes]
            positions = [xi + offset for xi, value in zip(x, values_by_theme) if value is not None]
            values = [value for value in values_by_theme if value is not None]
            if not values:
                continue
            bars = ax.bar(
                positions, values, width=bar_width,
                color=CONDITION_COLOR[cond], alpha=alpha,
                label=condition_label[cond], edgecolor=SURFACE, linewidth=0.5,
            )
            if metric in {"em_dash_rate", "filler_rate"}:
                for bar, value in zip(bars, values):
                    if value == 0:
                        ax.annotate(
                            "0", (bar.get_x() + bar.get_width() / 2, 0),
                            xytext=(0, 3), textcoords="offset points",
                            ha="center", va="bottom", color=CONDITION_COLOR[cond], fontsize=8,
                        )

        if metric in reference:
            ax.axhline(
                reference[metric], color=REFERENCE_COLOR, linestyle="--",
                linewidth=1.3, zorder=3,
            )

        ax.set_title(label, color=TEXT_PRIMARY, fontsize=10)
        if metric in COUNT_METRICS:
            ax.set_yscale("log")
        ax.set_xticks(list(x))
        ax.set_xticklabels(themes, color=TEXT_SECONDARY, fontsize=8, rotation=15)
        ax.tick_params(axis="y", colors=TEXT_SECONDARY, labelsize=8)
        ax.grid(axis="y", color=GRID, linewidth=0.7, zorder=0)
        ax.set_axisbelow(True)
        for spine in ("top", "right", "left"):
            ax.spines[spine].set_visible(False)
        ax.spines["bottom"].set_color(GRID)

    for unused_ax in axes.flat[len(METRICS):]:
        unused_ax.axis("off")

    handles, labels = axes.flat[0].get_legend_handles_labels()
    if reference:
        handles.append(Line2D([0], [0], color=REFERENCE_COLOR, linestyle="--", linewidth=1.3))
        labels.append(REFERENCE_LABEL)
    fig.legend(handles, labels, loc="upper right", frameon=False, labelcolor=TEXT_PRIMARY, fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=200, facecolor=SURFACE)
    print(f"wrote {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", default=str(BENCHMARK_DIR / "results" / "scores.csv"))
    parser.add_argument("--model", default="sonnet", help="model name used in the legend")
    parser.add_argument("--out", default=str(BENCHMARK_DIR / "results" / "comparison.png"))
    args = parser.parse_args()

    rows = load_scores(Path(args.scores))
    conditions = ["claude-plain", "claude-zweig-write", "claude-zweig-refine"]
    matched = paired_rows(rows, conditions)
    if not matched:
        raise SystemExit("No rows with all three conditions present for the same prompt.")
    means, themes = aggregate(matched)
    reference = reference_values(rows)
    plot(
        means, themes, conditions, reference, Path(args.out),
        "plain vs zweig-write vs zweig-refine", args.model,
    )


if __name__ == "__main__":
    main()
