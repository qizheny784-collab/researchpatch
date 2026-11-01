# 来源与处理记录

日期：2026-11-01。

前端案例来自用户在 SciencePal 上进行的机器遗忘隐私审计项目。旧沙盒文件通过用户提供的代理服务下载到本地，保留了原研究图、结果 JSON、样本分数和项目策略。

- `original-rev12.json`：从旧项目状态文件保留的原始图。
- `original-rev13.json`：从原服务返回的 HTML 中提取的内嵌状态，包含成员比例基线列的历史错误。
- `current.json`：rev13 的本地修订副本，明确标记 `+local-fix`；不声称已回写 SciencePal。
- `member-prior-corrected.json`：标准库根据恢复的 loss 分数直接复算。不是新训练或新的独立样本。
- `prior-scores.json`：仅成员与非成员 loss 数值，不含样本身份或原始图像。
- `policy-regression-original.json`：原项目的公开情景记录，包含已写出的结论字段，不作为独立盲测结果。

原始临时代理地址不作为长期依赖，也未嵌入前端运行流程。图中的来源文字可能包含原项目路径和文献简称；这些字符串不代表公开文献身份已经逐项重新核验。

参考资料：

- [SciencePal](https://sciencepal.ai/)
- [CIFAR-10 原始数据说明](https://www.cs.toronto.edu/~kriz/cifar.html)
- [EviGraph: Evidence-Guided Autonomous Research Agents](https://arxiv.org/abs/2608.04738)

所有实验数值以仓库中原始结果 JSON 为准。前端的差异、路径与候选影响计算属于本工作台行为，不替代实验和科学判断。
