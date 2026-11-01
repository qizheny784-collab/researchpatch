# ResearchPatch

Human-led research change coordination with a reproducible privacy-audit case.

ResearchPatch links experiments, evidence, claims, and researcher decisions in a versioned directed graph. The workbench lets researchers inspect sources and conditions, review revisions, and explore candidate impact paths. SciencePal supplied the research execution environment; this repository contains the Agent and five Skills, frontend implementation, and public case artifacts.

## Run locally

No frontend dependencies or external CDN are required. Open `dist/index.html`, or run:

```sh
python scripts/serve.py
# http://127.0.0.1:4173
```

## Check and reproduce

```sh
node --test tests/core.test.cjs
python scripts/reproduce.py
```

Node.js 22 and Python 3 are sufficient for these commands. The reproduction script uses only the Python standard library. The optional PDF generation script additionally requires ReportLab and pypdf; it is not needed to run the site or reproduce the metrics.

## Deploy to GitHub Pages

The included workflow publishes `dist/` on pushes to `main`. In repository Settings → Pages, set Source to GitHub Actions. This configuration does not itself establish that a deployment has succeeded; inspect the Actions run and the returned Pages URL.

## Read the case

- [Project brief](docs/PROJECT-EN.md)
- [English recording script](docs/VIDEO-SCRIPT-EN.md)
- [Submission checklist and conversation shares](docs/SUBMISSION-CHECKLIST.md)
- [Provenance](docs/PROVENANCE.md), [validation limits](docs/VALIDATION.md), and [state schema](docs/STATE-SCHEMA.md) are currently in Chinese.

The frontend is currently in Chinese. Its metric examples include fixed-model temperature transformations and prior reweighting of existing member/non-member scores. The corrected always-predict-non-member accuracy is `1 - member_prior`, independent of threshold. Historical incorrect records remain clearly labelled.

The interface does not train models or write back to SciencePal. Candidate impact paths require human review. The original policy missed a baseline error; the record retains that failure. There is no controlled evidence yet of workflow efficiency gains, policy transfer, or successful unlearning.

## License

Original code and configuration: MIT. Raw datasets and model weights are excluded. Third-party resources retain their own terms.
