Investigation of 406 BigCloneBench `tagged-tagged` WT3/T4 Clone Pairs
=====================================================================


This directory provides the data for the investigation of 406 true clone pairs drawn from the `tagged-tagged` WT3/T4 pairs in the downloaded BigCloneBench release. In BigCloneBench's terminology, `tagged-tagged` denotes a pair of two methods that were each tagged as a true positive for the same functionality. The investigation did not sample the `sample-tagged` or `sample-sample` categories, where “sample” denotes an exemplar function.

A precision calculation for a proportion gave a minimum of 385 observations. The sample was allocated using the WT3/T4 population of each functionality reported in BigCloneBench's construction summary. Independently rounding the 43 proportional allocations produced 386 observations and left 20 small strata with an allocation of zero. Within each functionality, the eligible pairs were randomly ordered and the allocated number was selected from the beginning of that ordering. The first pair was selected from each zero-allocation stratum to provide coverage, producing the final sample of 406 pairs. The random seed was not recorded; the archived pair identifiers therefore document the realised sample, while the allocation remains exactly reproducible.

Population estimates use all 406 pairs and weight each functionality by its number of eligible `tagged-tagged` WT3/T4 pairs in the downloaded release. They must not be generalised directly to the two exemplar-containing pair categories or to a different BigCloneBench release.

- The `snippets.zip` file contains all the snippets used in the analysis.

- The file `Protocol.md` contains the protocol for the manual investigation of the 406 clone pairs.

- The final `finaltruth.csv` file contains the final truth table after the manual investigation and the checking of the results against the responses of the LLM.

- The `strata.csv` file records, for each functionality, the WT3/T4 population reported in BigCloneBench's construction summary, the eligible `tagged-tagged` population in the downloaded release, the initial rounded allocation, the final sample size, the coverage indicator, and the relevant label counts. The reported populations total 8,498,894; the eligible populations total 8,381,611.

- The `pair_categories.csv` file records the numbers of `sample-sample`, `sample-tagged`, and `tagged-tagged` pairs in the downloaded release, both overall and after applying the WT3/T4 selection filter.

- The `uncertainty.py` script reproduces the precision calculation, all functionality allocations, the corrected 386/406 agreement counts, descriptive pooled calculations, and the population-weighted estimates. Its design-based interval uses the usual stratified variance estimate where a stratum contains at least two observations and the maximum possible binary-outcome variance for singleton strata.

- The files `Samples Investigation.xxx` contain the investigation table. The `Judge #1` and `Judge #2` columns preserve the independent pair- and method-level judgements, the `Agreed` and `Final` columns record the human consensus, and `Final + LLM` records the later post-LLM labels. The CSV and Excel files were derived from the Numbers file.

- The folder `LLM` contains the responses of the five runs of the LLM. The LLM is GPT-4o (`gpt-4o-2024-08-06`) via the OpenAI API. Its `README.md` records the surviving configuration and limitations; `reproduce.py` derives the five-run majority labels, human--LLM comparison, and post-scrutiny changes from the archived logs without making an API request.
