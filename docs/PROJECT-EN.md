# ResearchPatch

Human-led research change coordination, demonstrated through a privacy-auditing case.

## The problem

When an experiment changes, its old interpretation can survive in a figure, a research note, or a paper draft. A conversational assistant may update its latest answer while leaving those dependencies unresolved. Researchers need a way to inspect which parts of a project depend on an assumption and why a conclusion was revised.

## What we built

ResearchPatch combines an Agent configuration, five task Skills, and an interactive workbench. A versioned directed graph represents research questions, data, experiments, claims, decisions, and review policies. Nodes retain evidence references and conditions. Users can inspect saved versions and follow candidate impact paths before deciding what needs revision.

The frontend supports graph exploration, local JSON import and export, a revision log, and reproducible metric examples. It reads exported project state. It does not train models, autonomously approve scientific conclusions, or write back to SciencePal memory.

## The case

A SmallCNN was trained on 20,000 CIFAR-10 images. Its loss-based membership-inference AUC was approximately 0.7200. Changing output temperature while fixing model parameters changed the fixed attack's AUC: at T=5, it was approximately 0.6894. Predicted classes were unchanged. The researcher requested a narrower interpretation because, under stated access and numerical conditions, the temperature transformation is reversible.

A second analysis reweighted existing member and non-member scores. The researcher identified an incorrectly labelled baseline column. The corrected always-predict-non-member accuracy is 1 minus the member proportion: 50% or 90%, independent of threshold. At 10% members, the displayed attacks do not beat the 90% accuracy baseline, while AUC remains approximately 0.72. These quantities measure different properties; neither result establishes successful unlearning.

## Human judgment and project adaptation

The researcher challenged causal interpretations, separated audit accuracy from independent test accuracy, and caught the baseline formula error. The resulting project records narrow the affected claims and preserve earlier versions. Repeated corrections informed a metric review policy, but its first version failed to catch the baseline error. That failure remains visible.

We treat this as an early implementation of human-guided adaptation within a research task. We have not measured an improvement over a fixed workflow. The public policy checks are examples, not an independent benchmark.

## Reproducibility and limits

The release includes the frontend, configuration, public case artifacts, a Python standard-library reproduction script, and graph and metric tests. Original results and the local recovery correction are distinguished in provenance records. Raw images and model weights are excluded.

Full unlearning-versus-retraining experiments, an independent audit batch, controlled workflow comparisons, and cross-project policy transfer remain future work. SciencePal supplied the research execution environment; ResearchPatch supplies the project configuration, state coordination workflow, and frontend implementation. We make no claim that evidence graphs or research revision are new concepts.
