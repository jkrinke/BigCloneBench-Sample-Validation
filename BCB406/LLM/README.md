# Reproduction of the post-hoc LLM comparison

## Evidential role

The LLM comparison was performed after the two authors had reached human consensus on the 406 pair labels. It is a post-hoc challenge to those labels, not an independent source of ground truth and not part of the primary population estimate. The authors re-examined the 12 human--LLM disagreements with access to the model's explanations and changed two labels. The pre-LLM human estimate therefore remains the primary result; the post-LLM estimate is a sensitivity result.

## Surviving configuration record

| Item | Recorded information |
|---|---|
| Provider and interface | OpenAI API |
| Model | `gpt-4o-2024-08-06` |
| Model input | Two complete Java method snippets in a fixed order and the general functional-similarity definition |
| Information not supplied | BigCloneBench functionality tag, BigCloneBench pair label, and human judgements |
| Prompt | `prompt-template.txt`; every archived log also contains the complete instantiated prompt |
| Sampling settings | `temperature=0`, `top_p=0` (recorded in the manuscript, but not embedded in the surviving logs) |
| Runs | Five runs for every pair |
| Output labels | `YES-SIMILAR`, `NO-NOT-SIMILAR`, or `DONT-KNOW`, followed by an explanation |
| Parsed result codes | `100` for similar and `0` for not similar; the archived logs contain no `DONT-KNOW` or malformed result |
| Aggregation | Majority vote over five runs; a tie is impossible |
| Snippet order | Fixed, not counterbalanced |

The access dates, seed setting, output-token limit, retry policy, error-handling policy, and original API request script were not retained. The records of the exploratory model/prompt comparison and its selection criterion were also not retained. These details must not be reconstructed or presented as contemporaneously recorded controls.

The dated model identifier and archived configuration improve traceability but do not guarantee exact reproduction. Hosted proprietary models may become unavailable, and API output is not guaranteed to be deterministic even with temperature and top-p set to zero.

## Offline reproduction

From this directory, run:

```text
python3 reproduce.py
```

The script makes no network requests. It verifies that each compressed log contains 406 comparisons and 406 parsed results, checks that all five runs use the same pair order, calculates the majority label, joins it to the archived human-consensus and final labels, recomputes the human--LLM confusion matrix and Gwet's AC1, and writes `majority.csv`.

The reproduced results are:

- four runs contain 21 similar and 385 not-similar labels;
- the fifth contains 22 similar and 384 not-similar labels;
- 405 pairs receive the same label in all five runs, while one pair has a 4--1 majority;
- the majority label contains 21 similar and 385 not-similar pairs;
- the human consensus and LLM majority agree on 394 pairs and disagree on 12;
- the confusion matrix (human, LLM) is 18 true/true, 9 true/false, 3 false/true, and 376 false/false;
- scrutiny of the 12 disagreements changed two human labels, giving 25 similar and 381 not-similar final labels.

`SHA256SUMS` records checksums for the raw logs and the files used to derive these results. The population-weighted pre- and post-LLM estimates and intervals are reproduced separately by `../uncertainty.py`.
