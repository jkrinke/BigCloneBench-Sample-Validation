Investigation of 179 Papers Using BigCloneBench
===============================================

- The `Papers.csv` file contains bibliographic details for the 179 papers that use BigCloneBench as a dataset. It does not include individual evaluative classifications.
- The `LLM` folder contains the historical request script, prompts and surviving configuration record. Identifiable per-paper responses and classifications are retained internally and are not included in this release.

Aggregate Results and Scope
---------------------------

The final human consensus identified 128 of the 179 papers (71.5%) as having claims potentially affected by WT3/T4 mislabelling, while 51 were not classified as affected. This assessment concerns particular benchmark-based claims, not the overall quality of the papers or the conduct of their authors. A negative classification does not establish that the paper's measurements are unaffected.

The AI classified 174 papers as affected, the assisted human reviewer classified 137, and the unassisted human reviewer classified 125. One assisted-human judgement was uncertain. The following aggregate agreement results are reported in the manuscript:

| Comparison | Papers | Agreement | Cohen's Kappa | Gwet's AC1 |
| --- | --- | --- | --- | --- |
| AI vs assisted human | 178 | 77.5% | 0.085 | 0.710 |
| AI vs unassisted human | 179 | 71.5% | 0.089 | 0.607 |
| Assisted vs unassisted human | 178 | 87.1% | 0.672 | 0.788 |
| AI vs consensus | 179 | 73.2% | 0.097 | 0.636 |
| Assisted human vs consensus | 178 | 91.0% | 0.766 | 0.854 |
| Unassisted human vs consensus | 179 | 96.1% | 0.906 | 0.933 |

Comparisons involving the assisted reviewer exclude the uncertain judgement. The public supplementary material reports these aggregate results without distributing identifiable evaluative labels or LLM assessments, which could be interpreted as broader judgements about individual papers. The underlying records are preserved internally. The individual literature classifications and LLM responses are available from the authors on request. Consequently, these agreement statistics cannot be independently recalculated from the public files alone.

Collection and Screening
------------------------

The database searches used the term `BigCloneBench` in the broadest available search field: full text and metadata in IEEE Xplore, the full-text collection in the ACM Digital Library, all fields in Scopus and Web of Science, and anywhere in Wiley Online Library. The collection was updated to cover records indexed by 20 March 2025.

The searches returned 547 records: 157 from IEEE Xplore, 96 from the ACM Digital Library, 229 from Scopus, 60 from Web of Science, and 5 from Wiley Online Library. Removing 226 duplicates left 321 records. Sixteen were excluded before analysis: 2 retracted papers, 4 non-English papers, 3 inaccessible papers, 5 irrelevant records, the authors' earlier paper, and the original BigCloneBench paper. Two papers known to use BigCloneBench but not indexed by these searches were then added, giving 307 downloaded papers. LLM-assisted screening excluded 19 surveys and 109 papers that did not use BigCloneBench as a dataset, leaving the 179 papers in `Papers.csv`.

The bibliography records corpus membership only. Individual provisional and consensus classifications are not part of the public export.
