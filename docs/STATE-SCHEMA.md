# 项目状态协议

```json
{
  "project_id": "example",
  "revision": "1",
  "nodes": [{
    "id": "C1", "type": "claim", "text": "研究论断",
    "status": "needs_check", "scope": "适用范围",
    "source_refs": ["results/run-1.json"], "version": "v1",
    "updated_by": "researcher"
  }],
  "edges": [],
  "support_groups": []
}
```

边包含 `id, from, to, relation, basis, confirmed`。方向按项目记录保存，常见关系为 depends_on、supports、contradicts、derived_from、constrains。语义取决于 relation，不将所有边当作因果关系。

支持条件组可含 `id, claim_id, mode(all/any), member_ids, required_conditions`。工作台在节点详情展示相关条件组，不提供自动定理证明或科学真值推断。

状态包含 proposed、unknown、valid、needs_check、needs_rerun、needs_narrowing、contradicted、withdrawn、superseded。valid 只表示指定适用范围内已核查。

导入限制为 3 MB、300 节点与 2000 条边。工作台拒绝重复 ID 与悬空边；导入内容以文本渲染，不作为代码执行。导入和选择状态不写回平台，刷新前请导出要保留的状态。
