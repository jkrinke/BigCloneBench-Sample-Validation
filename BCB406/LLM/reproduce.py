#!/usr/bin/env python3
"""Reproduce the reported LLM comparison from the five archived logs."""

from __future__ import annotations

import argparse
import csv
import lzma
import re
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTEFACT = HERE.parent
COMPARISON = re.compile(r"^>>> (.+) vs\. (.+) with (.+)$")
RESULT_LABELS = {"0": "F", "100": "T"}


def parse_log(path: Path) -> tuple[list[tuple[str, str]], dict[tuple[str, str], str]]:
    with lzma.open(path, mode="rt", encoding="utf-8") as stream:
        lines = [line.rstrip("\n") for line in stream]

    order: list[tuple[str, str]] = []
    results: dict[tuple[str, str], str] = {}
    current: tuple[str, str] | None = None

    for index, line in enumerate(lines):
        if line == "### COMPARISON":
            if index + 1 >= len(lines):
                raise ValueError(f"Missing comparison after line {index + 1} in {path}")
            match = COMPARISON.fullmatch(lines[index + 1])
            if not match:
                raise ValueError(f"Malformed comparison at line {index + 2} in {path}")
            current = (match.group(1), match.group(2))
            if current in results or current in order:
                raise ValueError(f"Duplicate comparison {current} in {path}")
            order.append(current)
        elif line == "### RESULT":
            if current is None or index + 1 >= len(lines):
                raise ValueError(f"Result without a comparison at line {index + 1} in {path}")
            raw_result = lines[index + 1].strip()
            if raw_result not in RESULT_LABELS:
                raise ValueError(f"Unrecognised result {raw_result!r} for {current} in {path}")
            results[current] = RESULT_LABELS[raw_result]
            current = None

    if len(order) != 406 or len(results) != 406:
        raise ValueError(f"Expected 406 comparisons and results in {path}; found {len(order)} and {len(results)}")
    if set(order) != set(results):
        raise ValueError(f"Comparison/result mismatch in {path}")
    return order, results


def load_human_labels(path: Path) -> dict[tuple[str, str], str]:
    labels: dict[tuple[str, str], str] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.reader(stream):
            if len(row) <= 46 or row[16] not in {"T", "F"}:
                continue
            if not row[45].endswith(".java") or not row[46].endswith(".java"):
                continue
            pair = (row[45], row[46])
            if pair in labels:
                raise ValueError(f"Duplicate human-label pair {pair}")
            labels[pair] = row[16]
    if len(labels) != 406:
        raise ValueError(f"Expected 406 human labels; found {len(labels)}")
    return labels


def load_final_labels(path: Path) -> dict[tuple[str, str], str]:
    labels: dict[tuple[str, str], str] = {}
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            pair = (row["fileA"], row["fileB"])
            if row["Truth"] not in {"T", "F"}:
                raise ValueError(f"Unrecognised final label for {pair}")
            if pair in labels:
                raise ValueError(f"Duplicate final-label pair {pair}")
            labels[pair] = row["Truth"]
    if len(labels) != 406:
        raise ValueError(f"Expected 406 final labels; found {len(labels)}")
    return labels


def write_derived_table(
    path: Path,
    order: list[tuple[str, str]],
    runs: list[dict[tuple[str, str], str]],
    majority: dict[tuple[str, str], str],
    human: dict[tuple[str, str], str],
    final: dict[tuple[str, str], str],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "Functionality",
                "File A",
                "File B",
                "Run 1",
                "Run 2",
                "Run 3",
                "Run 4",
                "Run 5",
                "LLM majority",
                "Human consensus",
                "Human-LLM agreement",
                "Final after scrutiny",
                "Human label changed",
            ]
        )
        for pair in order:
            run_labels = [run[pair] for run in runs]
            writer.writerow(
                [
                    pair[0].split("_", 1)[0],
                    pair[0],
                    pair[1],
                    *run_labels,
                    majority[pair],
                    human[pair],
                    "T" if majority[pair] == human[pair] else "F",
                    final[pair],
                    "T" if final[pair] != human[pair] else "F",
                ]
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / "majority.csv",
        help="derived table to write (default: LLM/majority.csv)",
    )
    args = parser.parse_args()

    log_paths = sorted(HERE.glob("openai.*-gpt-4o.log.xz"))
    if len(log_paths) != 5:
        raise ValueError(f"Expected five archived logs; found {len(log_paths)}")

    parsed = [parse_log(path) for path in log_paths]
    order = parsed[0][0]
    if any(run_order != order for run_order, _ in parsed[1:]):
        raise ValueError("The comparison order differs between archived runs")
    runs = [results for _, results in parsed]

    human = load_human_labels(ARTEFACT / "Samples Investigation.csv")
    final = load_final_labels(ARTEFACT / "finaltruth.csv")
    expected_pairs = set(order)
    if set(human) != expected_pairs or set(final) != expected_pairs:
        raise ValueError("The log, human-label, and final-label pair sets differ")

    majority: dict[tuple[str, str], str] = {}
    for pair in order:
        counts = Counter(run[pair] for run in runs)
        majority[pair] = "T" if counts["T"] >= 3 else "F"

    run_counts = [Counter(run.values()) for run in runs]
    non_unanimous = [pair for pair in order if len({run[pair] for run in runs}) > 1]
    confusion = Counter((human[pair], majority[pair]) for pair in order)
    changed = [pair for pair in order if final[pair] != human[pair]]

    n = len(order)
    observed = (confusion[("T", "T")] + confusion[("F", "F")]) / n
    positive_share = (sum(value == "T" for value in human.values()) + sum(value == "T" for value in majority.values())) / (2 * n)
    chance_agreement = 2 * positive_share * (1 - positive_share)
    ac1 = (observed - chance_agreement) / (1 - chance_agreement)

    assert run_counts[:4] == [Counter({"F": 385, "T": 21})] * 4
    assert run_counts[4] == Counter({"F": 384, "T": 22})
    assert len(non_unanimous) == 1
    assert Counter(majority.values()) == Counter({"F": 385, "T": 21})
    assert Counter(human.values()) == Counter({"F": 379, "T": 27})
    assert confusion == Counter({("F", "F"): 376, ("T", "T"): 18, ("T", "F"): 9, ("F", "T"): 3})
    assert Counter(final.values()) == Counter({"F": 381, "T": 25})
    assert len(changed) == 2 and all(majority[pair] == final[pair] == "F" for pair in changed)

    write_derived_table(args.output, order, runs, majority, human, final)

    print("Archived runs:")
    for path, counts in zip(log_paths, run_counts, strict=True):
        print(f"  {path.name}: {counts['T']} similar, {counts['F']} not similar")
    pair = non_unanimous[0]
    print(f"Non-unanimous pair: {pair[0]} / {pair[1]} (four F, one T)")
    print("Human consensus vs LLM majority (human, LLM):")
    print(f"  T/T={confusion[('T', 'T')]}, T/F={confusion[('T', 'F')]}, F/T={confusion[('F', 'T')]}, F/F={confusion[('F', 'F')]}")
    print(f"Observed agreement: {observed:.6f}")
    print(f"Gwet's AC1: {ac1:.6f}")
    print(f"Changed after scrutiny: {len(changed)}")
    print(f"Derived table: {args.output}")


if __name__ == "__main__":
    main()
