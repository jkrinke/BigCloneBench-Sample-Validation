Usage of the LLM in the Literature Analysis
===========================================

This repository contains the results of using ChatGPT+ to generate literature review summaries and responses to specific questions based on a set of papers related to semantic code clone detection.
The papers were analyzed to determine how they used the BigCloneBench dataset and its subsets, and whether they validated or manually investigated the ground truth of BigCloneBench. The generated responses provide insights into the impact of the new finding that a significant portion of the WT3/T4 pairs in BigCloneBench are not clones.

The authors' involvement in critizing the BigCloneBench dataset and its use in previous work leads to a bias if the authors were to analyze the papers themselves.
We have therefore decided to rely on an LLM to not allow the author's bias to influence the results.
The LLM will provide a neutral and unbiased perspective on the papers and the new finding's impact on them.
However, the LLM or the prompt used to generate the responses may not capture all the nuances and details present in the papers and also may introduce biases of its own.

All the generated responses are available and have been carefully checked by both authors for inaccuracies and inconsistencies.

This folder contains the two prompts used in the investigation and the responses of the LLM. 

- The `analyze.py` file contains the Python script used to prompt the LLM.
- The `responses` folder contains the responses of the LLM for each of the 179 investigated papers.
- The `responses.csv` file contains the automatically extracted information from the individual responses.

