# RE-E2E data

The published dataset, **RE-E2E: A dataset for benchmarking end-to-end software requirements engineering tasks.**, is archived on [Zenodo](https://zenodo.org/records/22815961) (version v1, published September 17, 2026).

- **Dataset DOI**: [10.5281/zenodo.22815961](https://doi.org/10.5281/zenodo.22815961)
- **Download**: [data.zip](https://zenodo.org/records/22815961/files/data.zip?download=1)
- **Paper**: [Agent4RE (ACM)](https://dl.acm.org/doi/10.1145/3843779.3844634)

This directory contains the data retained for the RE-E2E benchmark:

- `project_summary_llm_processed/`: 29 concise project descriptions used as model inputs.
- `requirement_specifications_ieee_1998/`: 29 human-written SRS documents normalized to IEEE 830-1998 sections.
- `requirement_specifications_ieee_2018/`: 18 human-written SRS documents normalized to IEEE 29148-2018 sections.

Each requirement specification is stored as CSV with its section hierarchy and normalized textual content. Generated model completions and judge outputs are intentionally excluded.

## Citation

If you use RE-E2E, please cite the Agent4RE paper by Yongjian Tang, Linhan Li, and Thomas Runkler (POVC '26, 2026), as requested by the Zenodo record. The full BibTeX entry is in the [repository citation section](../README.md#citation), and machine-readable metadata is in [CITATION.cff](../CITATION.cff).

## License

The [Zenodo record](https://zenodo.org/records/22815961) lists [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) as the dataset license. The repository's [MIT License](../LICENSE) applies to source code and documentation, not to the dataset files.

