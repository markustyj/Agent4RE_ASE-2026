# RE-E2E data

This directory contains the data retained for the RE-E2E benchmark:

- `project_summary_llm_processed/`: 29 concise project descriptions used as model inputs.
- `requirement_specifications_ieee_1998/`: 29 human-written SRS documents normalized to IEEE 830-1998 sections.
- `requirement_specifications_ieee_2018/`: 18 human-written SRS documents normalized to IEEE 29148-2018 sections.

Each requirement specification is stored as CSV with its section hierarchy and normalized textual content. Generated model completions and judge outputs are intentionally excluded.

## Provenance and license

The paper describes the reference specifications as selected from real-world software repositories, normalized with regular-expression cleanup, and aligned to IEEE section names using semantic matching with human review for low-confidence cases. Project descriptions were manually derived from the finalized specifications and language-checked with an LLM.

The MIT license at the repository root applies to software and documentation only. Before public dataset release, the maintainers must add the source URL, original license or redistribution permission, and transformation record for every reference specification. Until then, no redistribution license is granted for files in this directory.
