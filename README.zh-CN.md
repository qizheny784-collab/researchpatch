# ResearchPatch

[English README](README.en.md) · [English project brief](docs/PROJECT-EN.md) · [English recording script](docs/VIDEO-SCRIPT-EN.md)

**研究员主导的科研变更协调工作台。**

研究对象、实验设置和评价口径不断变化，相关图表与论文论断却容易保留旧状态。ResearchPatch 用版本化研究图连接问题、证据、实验、论断和人的决策，让研究者查看变化可能影响什么、依据是什么，以及哪些内容仍未验证。

## 运行

无需安装前端依赖，也不依赖外部 CDN。可以直接打开 `dist/index.html`；推荐使用本地服务器：

```sh
python scripts/serve.py
# http://127.0.0.1:4173
```

Node.js 用于测试；Python 3 用于标准库复算和本地服务：

```sh
node --test tests/core.test.cjs
python scripts/reproduce.py
```

## 工作台功能

- 研究图：节点详情、原始来源、状态与适用条件；切换版本、搜索、缩放和候选影响路径。
- 变更审阅：人的纠正、修订前后、证据及保留内容。
- 实验与证据：温度负对照，以及基于既有分数的先验敏感性分析。
- 任务策略：策略形成、公开回归记录与真实漏检，不把规则记录当作独立评测。
- JSON 导入导出：导入内容在浏览器本地处理，不上传服务器。

网页不执行训练、不批准科研变更、不自动写入 SciencePal 记忆。此版本提供交互式研究状态浏览与案例复算；实际研究运行由配套 Agent/Skills 在 SciencePal 中完成。

## 实际案例

CIFAR-10 子集、SmallCNN、20,000 张训练样本。固定模型，改变输出温度；另用已有 200 个成员与 200 个非成员分数进行先验重加权。相关结果来自原研究文件，前端没有重新训练模型。

用户指出先验敏感性表的一列错误：原公式算的是“当前攻击预测为非成员的比例”。正确的“始终猜非成员”准确率为 `1 - member_prior`，所以分别为 50% 和 90%，与攻击阈值无关。本仓库复算并保留原始图版本与修订出处。

原策略 v1.0 没有拦住这次错误，这是项目局限之一。当前没有独立的固定流程对照、效率测量或未见任务迁移验证，不能据此声称 RSI 已显著提高研究质量。

## 目录

```text
dist/                 可直接部署的前端与公开案例文件
scripts/reproduce.py  标准库复算先验敏感性结果
scripts/serve.py      只服务 dist/ 的本地服务器
scripts/build_data.py 原案例来源文件可用时重建公开数据
tests/                指标、图导入、影响追踪与版本保留测试
agents/               ResearchPatch Agent 配置
skills/               五个项目 Skills
docs/                 状态协议、来源、验证边界及演示提纲
```

`build_data.py` 是原始开发资料的打包脚本，默认读取相邻恢复目录；第三方复现前端和指标无需运行它，仓库已包含公开状态和无样本身份的分数。重建自己的案例时可以替换输入并使用导入功能。

## GitHub Pages

仓库附 Pages 工作流。上传仓库后，在仓库 Settings → Pages 中将 Source 设为 GitHub Actions，推送 main 即可部署 `dist/`。站点本身无需密钥或后端。此说明不代表仓库已经发布。

## 研究与原创性边界

SciencePal 提供研究执行底座；本项目提供图状态协议、变更协调配置和前端实现。证据图与跨阶段修复有 EviGraph 等相邻工作，不主张这些概念首次出现。案例不是新的遗忘算法，也未证明训练信息已经删除。

见 [来源与处理记录](docs/PROVENANCE.md)、[验证边界](docs/VALIDATION.md)、[项目状态协议](docs/STATE-SCHEMA.md)。

## License

项目原创代码与配置采用 MIT License。CIFAR-10、Python/PyTorch 等第三方资源保留各自来源与条款；仓库不分发原始图像和模型权重。结果文件是具体实验记录，不作为第三方研究结论的再授权。
