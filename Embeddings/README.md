Aggregate Results of the Exploratory Embedding Analysis
======================================================

`results.csv` contains 57 recorded model–dataset results: seven models on each of eight balanced datasets, together with the primary model, `jina-code-embeddings-1.5b`, on full BigCloneBench. These results support the manuscript tables reporting primary-model AUC and pair counts, primary-model optimal and fixed-threshold MCC and F1, and the seven-model comparison.

The values were extracted on 24 September 2026 from the existing SimilBench log `results/sim-bcb-all-ulong.log`, retaining its numerical precision. They were not transcribed from the manuscript or obtained by rerunning inference. Only the models and dataset variants reported in these tables were selected. The source log also contains other experimental results.

The source log's SHA-256 is `204d21028248942b1e9b5979e1661362e9a6b0331c485e58d28a3222814af8f0`.

Columns
-------

| Column | Meaning |
| --- | --- |
| `dataset` | Dataset name used for this supplementary table. |
| `source_dataset` | Dataset identifier in the original log. |
| `model` | Model name recorded in the result filename. This is not a weight-revision identifier. |
| `pairs`, `positive_pairs`, `negative_pairs` | Numbers of evaluated pairs and their ground-truth classes, as recorded in the log. |
| `auc` | Area under the ROC curve. |
| `mcc_threshold_lower`, `mcc_threshold_upper` | First and last tested thresholds attaining the maximum MCC. |
| `mcc_optimal` | Maximum MCC over the tested thresholds. |
| `f1_threshold_lower`, `f1_threshold_upper` | First and last tested thresholds attaining the maximum F1 score. |
| `f1_optimal` | Maximum F1 score over the tested thresholds. |
| `fixed_threshold` | Threshold used for the fixed-threshold results, 0.5 in every included row. |
| `mcc_fixed`, `f1_fixed` | MCC and F1 at that fixed threshold. |
| `source_scores` | Relative path identifying the original pair-score file in the working archive. These files are not included in this supplementary package. |

The surviving calculation script, `scripts/csv_sim.py`, tests thresholds from 0 to 1 in increments of 0.01 and predicts a positive pair when its score is greater than or equal to the threshold. MCC and F1 are optimised separately. The threshold bounds describe the tested grid, not a claim about every intervening real-valued threshold. AUC is calculated from the scores without applying a classification threshold. The script converts result values recorded as `ERROR`, `NaN` or an empty string to zero. This describes the preserved implementation and does not establish that any such values occurred in these runs.

Coverage and Limitations
------------------------

All 56 rows of the manuscript's seven-model comparison agree with the archived aggregate values at the reported precision. The nine primary-model pair counts total 107,961,127. The full and balanced BigCloneBench rows overlap, so this total counts evaluated pairs across dataset variants rather than distinct pairs across the entire collection.

The manuscript's separate table of results using BigCloneBench-derived thresholds reports MCC at 0.19 and F1 at 0.17. Corresponding archived aggregate results were not located during preparation of this export and are not included here. The optimal-threshold columns must not be interpreted as results using BigCloneBench-derived thresholds.

The original pair-level scores and ground-truth files remain in the working archive. This compact supplement supplies aggregate evidence, not a complete replication package or independent validation of the input labels. It does not include source-code corpora, embedding vectors, model weights or an inference environment. Exact historical model revisions are not established by this log. The embedding comparison remains an exploratory diagnostic and does not estimate the prevalence of semantic mislabelling.
