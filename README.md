How the Misuse of a Dataset Harmed Semantic Clone Detection
===========================================================

This repository contains supplementary material for the journal paper and the earlier IWSC 2022 paper. The [GitHub repository](https://github.com/jkrinke/BigCloneBench-Sample-Validation) is shared with the earlier IWSC 2022 paper and therefore also contains an `IWSC2022` directory. That directory preserves the 100-pair data for the earlier paper and is intentionally outside the scope of this journal-specific package and its [Zenodo record](https://doi.org/10.5281/zenodo.15356503).

We provide the following data as supplementary material:
- The aggregate results of the exploratory embedding analysis.
- The subset of 406 clone pairs used for the manual investigation.
- The protocol for the manual investigation.
- The results of the manual investigation.
- The LLM-based post-hoc comparison of the manual results.
- The code used for the LLM-based analysis of the literature review.
- The literature-review bibliography and aggregate classification and agreement results.

The journal supplementary material is separated into three folders:
- `Embeddings`: Contains the recorded aggregate embedding results and an explanation of their coverage.
- `BCB406`: Contains the data related to the 406 clone pairs used for the manual investigation.
- `Literature`: Contains the data related to the literature review.

Individual evaluative classifications of papers and identifiable literature LLM responses are retained internally and excluded from this release. The individual literature classifications and LLM responses are available from the authors on request. The literature README explains the rationale and the resulting limitation on independent recalculation.

The `IWSC2022` directory retains the earlier 100-pair investigation unchanged. Earlier Git revisions and Zenodo versions remain available as historical records.
