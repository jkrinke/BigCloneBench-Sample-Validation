Usage of the LLM in the Literature Analysis
===========================================

The LLM extracted information about how papers used BigCloneBench and supplied
provisional classifications for human review. It was an initial aid, not a
neutral or independent judge. The first author checked the extracted results;
the final classification used a second, unassisted human judgement and
consensus discussion.

Recorded configuration
----------------------

| Item | Recorded value |
| --- | --- |
| Provider and interface | OpenAI Assistants API |
| Model | The request script specifies the general `gpt-4o` alias; the OpenAI usage logs record the corresponding requests as `gpt-4o-2024-08-06` |
| Assistant instructions | Embedded in `analyze.py` |
| Paper input | One PDF attached to a new thread using file search |
| Prompts | `PROMPT.md`, followed by `PROMPT2.md`, in the same thread |
| Runs | One run per prompt and paper; no voting or tie rule |
| Sampling settings | `temperature=1e-14`, `top_p=1e-14`; no seed specified |
| Output limit | Not specified in the request |
| Timeout and failure handling | 300 seconds; a non-completed run terminates without an automatic retry |
| Output handling | Text responses and extracted tabular summaries are retained internally and omitted from this public release |

The access dates, OpenAI client-library version, seed and output-token limit
were not recorded. These omissions prevent exact API-output
reproduction. The realised prompts and script are provided here. The responses are preserved internally. The individual literature classifications and LLM responses are available from the authors on request.
The model output may vary despite the near-zero sampling settings and may
reflect limitations or biases in the model, prompt, file search or long-document
processing.

The 93.3% value used during this analysis, written as 93.35% in the preserved
prompt, is the unweighted human-consensus proportion of 379/406 available at
that stage. It is not the subsequently reported population-weighted estimate.

Files
-----

- `analyze.py`: the request and response-handling script.
- `PROMPT.md` and `PROMPT2.md`: the two prompts.
- `SHA256SUMS`: checksums for these records.

The historical script uploads a paper PDF to the API. It is preserved as a methodological record, without a claim of current API compatibility. No new API request is needed to inspect this material. Identifiable responses and evaluative classifications are omitted for the reasons explained in `../README.md`.
