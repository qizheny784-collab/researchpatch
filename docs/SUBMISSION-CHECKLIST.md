# Submission checklist

## Required delivery items

| Item | Current state | Final action |
| --- | --- | --- |
| Frontend | Implemented; previous Sites deployment succeeded | Publish and verify GitHub Pages after GitHub connection |
| Public source repository | Local source prepared; MIT license and Pages workflow included | Create public repository and verify anonymous access |
| Conversation 1 | Public replay opened and its final step inspected | [Original research](https://sciencepal.ai/share/717d7dac-9b48-4b09-883c-09e638aa90d5) |
| Conversation 2 | Public replay opened and its final step inspected | [Recovery and correction](https://sciencepal.ai/share/ad981f6e-4d0e-4d95-b4a2-33451c9670aa) |
| English recording | Script in VIDEO-SCRIPT-EN.md | Record approximately four minutes; upload to an accessible video host |
| Project introduction | English text in PROJECT-EN.md | Paste into the submission form; attach a report if the form requires one |

Do not submit localhost or an assumed GitHub Pages URL. Check each conversation share in a logged-out browser. A conversation URL copied from the address bar may not be a public share. Do not substitute this Codex development chat for the SciencePal research evidence.

On 1 November 2026, both supplied share pages loaded their read-only replay without a login prompt in the available browser. The original replay displayed 1,492 entries; the recovery replay displayed 251. Its final entry shows the baseline script edit, not a completed rerun. The local release supplies the corrected reproduction and must be identified as such. This check verifies access and the inspected endpoint, not every historical tool call or attachment.

## Conversation evidence to retain

Conversation 1 should show the research question, actual baseline and temperature experiment, a researcher correction, and the resulting change in scope or graph. Conversation 2 should show recovery limits, the incorrect baseline formula, and its correction where actually completed. The local frontend correction is documented as local work, not retroactively attributed to the agent's earlier run.

## Source release checks

- Include frontend, Agent and five Skills, reproducible scores and scripts, tests, license, provenance, and limitations.
- Exclude hosting identity, credentials, model checkpoints, raw datasets, and private conversation exports.
- Preserve historical erroneous results with a clear label; make the corrected version the default.
- GitHub Pages must deploy dist/ using the included workflow. Repository Settings → Pages → Source must be GitHub Actions.

## Claims to avoid

Do not claim that training information was deleted, that a lower fixed-attack AUC proves better privacy, that public policy examples are an independent evaluation, or that the project has demonstrated an RSI performance gain. The implemented contribution is human-led change coordination with inspectable graph versions and a reproducible case.
