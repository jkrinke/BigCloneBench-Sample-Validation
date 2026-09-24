#!/usr/bin/env python3
"""Reproduce the sampling allocation and manual-validation estimates."""

import csv
from collections import Counter
from math import floor, sqrt
from pathlib import Path


Z_95 = 1.959963984540054
REPORTED_WT3_T4 = 8_498_894
TARGET_SAMPLE = 385


def sample_size(
    population: int,
    proportion: float = 0.5,
    margin: float = 0.05,
    z: float = 1.96,
):
    """Return the finite-population sample size for estimating a proportion."""
    numerator = population * z**2 * proportion * (1 - proportion)
    denominator = margin**2 * (population - 1) + z**2 * proportion * (1 - proportion)
    return numerator / denominator


def round_half_up(value: float):
    """Round a non-negative allocation to the nearest integer."""
    return floor(value + 0.5)


def wilson_interval(successes: int, total: int, z: float = Z_95):
    """Return a two-sided Wilson score interval for a proportion."""
    proportion = successes / total
    denominator = 1 + z**2 / total
    centre = (proportion + z**2 / (2 * total)) / denominator
    half_width = (
        z
        * sqrt(proportion * (1 - proportion) / total + z**2 / (4 * total**2))
        / denominator
    )
    return proportion, centre - half_width, centre + half_width


def design_estimate(rows, count_field, z: float = Z_95):
    """Return a weighted estimate and a conservative design-based interval.

    For strata with at least two observations, the variance uses the usual
    stratified simple-random-sampling estimator with a finite-population
    correction. A within-stratum variance cannot be estimated for a singleton
    stratum, so its contribution uses the maximum possible finite-population
    variance for a binary outcome.
    """
    population = sum(row["eligible_population"] for row in rows)
    estimate = 0.0
    variance = 0.0

    for row in rows:
        stratum_size = row["eligible_population"]
        sample = row["sample"]
        count = row[count_field]
        weight = stratum_size / population
        proportion = count / sample
        sampling_fraction = sample / stratum_size
        estimate += weight * proportion

        if sample > 1:
            sample_variance = sample / (sample - 1) * proportion * (1 - proportion)
        elif stratum_size > 1:
            sample_variance = stratum_size / (stratum_size - 1) * 0.25
        else:
            sample_variance = 0.0

        variance += weight**2 * (1 - sampling_fraction) * sample_variance / sample

    standard_error = sqrt(variance)
    lower = max(0.0, estimate - z * standard_error)
    upper = min(1.0, estimate + z * standard_error)
    return estimate, lower, upper


def agreement(labels):
    """Return observed agreement, Cohen's kappa, and Gwet's AC1."""
    total = len(labels)
    observed = sum(left == right for left, right in labels) / total
    left_positive = sum(left == "T" for left, _ in labels) / total
    right_positive = sum(right == "T" for _, right in labels) / total

    kappa_expected = (
        left_positive * right_positive
        + (1 - left_positive) * (1 - right_positive)
    )
    kappa = (observed - kappa_expected) / (1 - kappa_expected)

    mean_positive = (left_positive + right_positive) / 2
    ac1_expected = 2 * mean_positive * (1 - mean_positive)
    ac1 = (observed - ac1_expected) / (1 - ac1_expected)
    return observed, kappa_expected, kappa, ac1_expected, ac1


base = Path(__file__).parent

with (base / "strata.csv").open(newline="", encoding="utf-8") as handle:
    strata = []
    for record in csv.DictReader(handle):
        reported_population = int(record["Reported WT3/T4"])
        allocation = round_half_up(
            TARGET_SAMPLE * reported_population / REPORTED_WT3_T4
        )
        strata.append(
            {
                "functionality": int(record["Functionality"]),
                "reported_population": reported_population,
                "eligible_population": int(
                    record["Eligible tagged-tagged WT3/T4"]
                ),
                "allocation": int(record["Initial allocation"]),
                "sample": int(record["Sample"]),
                "coverage": int(record["Coverage addition"]),
                "human": int(record["Human consensus false"]),
                "unanimous": int(record["Unanimous false"]),
                "post_llm": int(record["Post-LLM false"]),
            }
        )
        assert allocation == int(record["Initial allocation"])

assert len(strata) == 43
assert sum(row["reported_population"] for row in strata) == REPORTED_WT3_T4
assert sum(row["eligible_population"] for row in strata) == 8_381_611
assert sum(row["allocation"] for row in strata) == 386
assert sum(row["coverage"] for row in strata) == 20
assert all(row["coverage"] == (row["allocation"] == 0) for row in strata)
assert all(row["sample"] == row["allocation"] + row["coverage"] for row in strata)
assert sum(row["sample"] for row in strata) == 406
assert sum(row["human"] for row in strata) == 379
assert sum(row["unanimous"] for row in strata) == 341
assert sum(row["post_llm"] for row in strata) == 381

with (base / "pair_categories.csv").open(newline="", encoding="utf-8") as handle:
    categories = list(csv.DictReader(handle))

category_counts = {
    row["Pair type"]: (int(row["All true pairs"]), int(row["WT3/T4 filter"]))
    for row in categories
}
assert category_counts["Total"] == (8_584_153, 8_422_357)
assert category_counts["tagged-tagged"] == (8_541_772, 8_381_611)

with (base / "Samples Investigation.csv").open(
    newline="", encoding="utf-8-sig"
) as handle:
    sample_rows = [
        row
        for row in csv.reader(handle)
        if len(row) >= 50 and row[49].isdigit() and row[47] and row[48]
    ]

assert len(sample_rows) == 406
pair_ids = {tuple(sorted((row[47], row[48]))) for row in sample_rows}
assert len(pair_ids) == 406

coverage_functions = {
    row["functionality"] for row in strata if row["coverage"] == 1
}
base_rows = [row for row in sample_rows if int(row[49]) not in coverage_functions]
assert len(base_rows) == 386

base_decisions = Counter(row[10] for row in base_rows)
full_decisions = Counter(row[10] for row in sample_rows)
assert base_decisions == Counter({"F": 329, "#": 38, "T": 19})
assert full_decisions == Counter({"F": 341, "#": 42, "T": 23})

base_human_false = sum(
    row["human"] for row in strata if row["coverage"] == 0
)
base_unanimous_false = sum(
    row["unanimous"] for row in strata if row["coverage"] == 0
)
assert base_human_false == 364
assert base_unanimous_false == 329

required = sample_size(REPORTED_WT3_T4)
assert 384 < required < 385

print("Sampling reconstruction")
print(f"Reported WT3/T4 population used for allocation,{REPORTED_WT3_T4}")
print(f"Calculated minimum before upward rounding,{required:.3f}")
print(f"Minimum sample size,{TARGET_SAMPLE}")
print(f"Sum of independently rounded allocations,{sum(r['allocation'] for r in strata)}")
print(f"Zero allocations,{sum(r['coverage'] for r in strata)}")
print(f"Final sample size,{sum(r['sample'] for r in strata)}")
print(f"Eligible tagged-tagged WT3/T4 population,{sum(r['eligible_population'] for r in strata)}")

print()
print("Pair categories in the downloaded release")
print("Pair type,All true pairs,WT3/T4 filter")
for pair_type in ("sample-sample", "sample-tagged", "tagged-tagged", "Total"):
    all_pairs, wt_pairs = category_counts[pair_type]
    print(f"{pair_type},{all_pairs},{wt_pairs}")

print()
print("Initial human agreement")
print("Sample,Total,Agreed true,Agreed false,Disagreements,Observed,Kappa expected,Kappa,AC1 expected,AC1")
for label, rows in (("Initial allocation", base_rows), ("Full sample", sample_rows)):
    decisions = Counter(row[10] for row in rows)
    statistics = agreement([(row[0], row[5]) for row in rows])
    print(
        f"{label},{len(rows)},{decisions['T']},{decisions['F']},{decisions['#']},"
        + ",".join(f"{value:.3f}" for value in statistics)
    )

print()
print("Descriptive pooled calculations for the corrected 386-pair allocation")
print("Analysis,Count,Total,Estimate,Lower 95% CI,Upper 95% CI")
for label, count in (
    ("Human consensus", base_human_false),
    ("Unanimous before adjudication", base_unanimous_false),
):
    estimate, lower, upper = wilson_interval(count, 386)
    print(
        f"{label},{count},386,"
        f"{100 * estimate:.1f}%,{100 * lower:.1f}%,{100 * upper:.1f}%"
    )

print()
print("Population-weighted calculations for the 406 tagged-tagged pairs")
print("Analysis,Count,Total,Estimate,Lower 95% CI,Upper 95% CI")
for label, field, count in (
    ("Human consensus", "human", 379),
    ("Unanimous before adjudication", "unanimous", 341),
    ("Post-LLM labels", "post_llm", 381),
):
    estimate, lower, upper = design_estimate(strata, field)
    print(
        f"{label},{count},406,"
        f"{100 * estimate:.1f}%,{100 * lower:.1f}%,{100 * upper:.1f}%"
    )
