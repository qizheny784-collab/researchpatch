# ResearchPatch — recording script

Target length: 4 minutes, at a calm pace. Record the existing artifacts. Do not present saved results as a live training run. The interface is currently in Chinese; the narration below is entirely in English.

## 0:00–0:30 | Open the research graph

Research rarely follows the original plan. A dataset changes, an experiment fails, or a result turns out to mean less than we thought. The difficult part is keeping the rest of the project consistent.

This is ResearchPatch, a research change workbench built around a real privacy-auditing study. It connects experiments, evidence, claims, and researcher decisions in a versioned graph.

## 0:30–1:10 | Select a claim, show its sources, then switch graph versions

Here, each node represents part of the research. I can open a claim, inspect its evidence and conditions, and follow the relationships to other parts of the project. The impact view highlights connected items that may need review. A connection alone does not decide whether a claim is true.

The saved versions preserve earlier interpretations. The latest local revision includes a correction made during recovery. We label that separately from the original SciencePal history.

## 1:10–1:55 | Open Results and show the temperature table

Our case uses a SmallCNN trained on twenty thousand CIFAR-10 images. The original loss-based membership attack had an AUC of about zero point seven two.

We kept the model parameters fixed and changed the output temperature. The predicted classes stayed the same, while the fixed attack's AUC changed. At temperature five, the loss-based AUC was about zero point six nine.

That result does not demonstrate successful unlearning. With a known temperature and complete probability outputs, the transformation can be reversed, subject to numerical precision. We narrowed the claim to sensitivity of the fixed attack evaluation.

## 1:55–2:45 | Change the member proportion and loss threshold

The next example contains a mistake we kept in the project history. A column labelled “always predict non-member” actually measured how often the attack predicted non-members.

I flagged the formula. The correct baseline is simply one minus the member proportion. With ten percent members, it is ninety percent at every threshold. The displayed attack accuracies remain below that baseline, although AUC is still about zero point seven two.

Accuracy depends on the class balance and the chosen threshold. AUC measures ranking across thresholds. This is a reweighting of existing samples, so it is not a new independent audit or evidence of improved privacy.

## 2:45–3:30 | Open Changes, then Policy

ResearchPatch records what changed and which explanations need revision. The researcher challenged the interpretation; the agent adjusted the analysis, and the project state retained both the correction and its source.

Repeated corrections also led to a project-specific metric review policy: check what changed, which population was measured, and how far the result supports the claim.

The first policy missed the baseline error. We show that failure alongside its successful checks. This is an early example of human-guided adaptation within a project. We have not yet established an efficiency gain or generalization to unseen projects.

## 3:30–4:05 | Show source files, reproduction instructions, and closing graph

SciencePal provided the research execution environment. This project adds the agent and skill configuration, the versioned graph workflow, and this interactive frontend.

The release includes the public case files, a standard-library reproduction script, and tests for the corrected metrics and graph behavior. It excludes model weights and raw training images.

The next evaluation would compare this workflow against a fixed process under the same budget. For now, the demo shows a concrete research revision: a human catches an error, the analysis changes, and the graph and project memory preserve why.

## Recording checklist

- Start on the graph, with the browser zoom readable and notifications closed.
- Pre-open Results, Changes, Policy, the source repository, and the two real conversation shares in separate tabs.
- Demonstrate a constant 90% baseline while changing thresholds; then switch to 50% members.
- Show the policy's missed error. Do not claim independent policy validation.
- Say “source repository” only after GitHub publication succeeds. If it is still pending, say “source package.”
- Finish with the actual working deployment address. Do not display an invented Pages URL.
