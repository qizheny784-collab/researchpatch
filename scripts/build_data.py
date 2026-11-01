"""Prepare the bundled, provenance-labelled ResearchPatch case study."""
from pathlib import Path
import copy
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]
RECOVERY=ROOT.parent/'recovered-sciencepal'
CASE=RECOVERY/'essential/unlearning-privacy'
OUT=ROOT/'dist/assets'
RESULTS=OUT/'results'
RESULTS.mkdir(parents=True,exist_ok=True)

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))

before=read(CASE/'visualization/current.json')
latest_html=RECOVERY/'research-map-latest.html'
if latest_html.exists():
    found=re.search(r'<script id="state-data" type="application/json">(.*?)</script>',latest_html.read_text(encoding='utf-8'),re.S)
    if found: before= json.loads(found[1])
original12=read(CASE/'visualization/current.json')
latest=copy.deepcopy(before)
latest['revision']=str(before.get('revision','13'))+'+local-fix'
latest['display_notice']='原 SciencePal 研究图 + 用户指出后的本地复算修订。该修订未宣称已同步写回 SciencePal。'
for n in latest['nodes']:
    if n['id']=='ANALYSIS-MEMBER-PROP':
        n['text']='成员比例敏感性分析（既有分数重加权）：成员占比 50% 时始终猜非成员准确率为 50%，占比 10% 时为 90%，与阈值无关。原列误用了当前攻击预测为非成员的比例。固定两组条件分布，AUC 保持 0.720025。loss 阈值 0.1 时，攻击准确率分别为 0.7100 与 0.5060，不能据此说明隐私信息减少。'
        n['version']='v2-local-recomputed';n['updated_by']='用户纠正＋本地标准库复算'
        n['source_refs']=['assets/results/member-prior-corrected.json','assets/results/prior-scores.json']
        n['scope']='200 成员与 200 非成员的先验敏感性复算，不是新独立审计样本'
latest['nodes'].append({'id':'LOCAL-POLICY-LIMITATION','type':'finding','text':'策略局限：指标审查策略 v1.0 未拦住“始终猜非成员”列的公式或命名错误。用户指出后复算修正；不能仅展示规则成功情景，亦不能据此宣称策略可靠性或迁移提升。','status':'valid','scope':'本次实际纠正与策略边界','version':'v1-local','source_refs':['assets/results/member-prior-corrected.json','用户对话中的公式纠正'],'updated_by':'用户纠正记录＋本地整理'})
latest['edges'] += [{'id':'local-e-policy-failure','from':'LOCAL-POLICY-LIMITATION','to':'POLICY-METRIC-CHANGE','relation':'limits','basis':'策略存在记录，但未防止本次计算列错误','confirmed':True},{'id':'local-e-baseline-revision','from':'ANALYSIS-MEMBER-PROP','to':'LOCAL-POLICY-LIMITATION','relation':'informs','basis':'实际错误与后续复算作为局限记录','confirmed':True}]
scores=read(CASE/'experiments/morig_baseline/output/per_sample_scores.json')
member=scores['eval_member_loss'];nonmember=scores['eval_nonmember_loss']
rows=[]
for prior in [.5,.1]:
    for threshold in [.01,.1,1.]:
        tpr=sum(x<threshold for x in member)/len(member);fpr=sum(x<threshold for x in nonmember)/len(nonmember)
        tp=prior*tpr;fp=(1-prior)*fpr;tn=(1-prior)*(1-fpr)
        rows.append({'member_prior':prior,'loss_threshold':threshold,'attack_accuracy':tp+tn,'precision':tp/(tp+fp) if tp+fp else None,'recall':tpr,'fpr':fpr,'always_nonmember_accuracy':1-prior,'predicted_nonmember_fraction':tn+prior*(1-tpr)})
auc=sum(1 if m<n else .5 if m==n else 0 for m in member for n in nonmember)/(len(member)*len(nonmember))
corrected={'provenance':'Locally recomputed from recovered per-sample loss scores after a real user correction. Not a new model run or independent audit set.','n_member':len(member),'n_nonmember':len(nonmember),'auc':auc,'thresholds':'Illustrative fixed loss thresholds, not optimized on this evaluation set','rows':rows}
for name in ['morig_result.json','calib_neg_control.json','calib_bootstrap.json','class_auc.json']:
    shutil.copyfile(CASE/'experiments/morig_baseline/output'/name,RESULTS/name)
shutil.copyfile(CASE/'design/metric_change_regression_check.json',RESULTS/'policy-regression-original.json')
shutil.copyfile(CASE/'design/metric-change-review-policy.md',OUT/'metric-change-review-policy.md')
(RESULTS/'member-prior-corrected.json').write_text(json.dumps(corrected,ensure_ascii=False,indent=2),encoding='utf-8')
(RESULTS/'prior-scores.json').write_text(json.dumps({'member_loss':member,'nonmember_loss':nonmember,'note':'Scores only, no raw images or sample identities; existing CIFAR-10 audit samples.'},ensure_ascii=False),encoding='utf-8')
(OUT/'current.json').write_text(json.dumps(latest,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'original-rev13.json').write_text(json.dumps(before,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'original-rev12.json').write_text(json.dumps(original12,ensure_ascii=False,indent=2),encoding='utf-8')
data={'snapshots':[{'label':'原始研究记录 · rev12','state':original12},{'label':'原始研究记录 · rev13（含历史错误）','state':before},{'label':'rev13 ＋ 本地复算修订','state':latest}],
 'focusIds':['RQ1','DATA-CIFAR10','MODEL-ORIG','EXP-MORIG-BASELINE','ANALYSIS-CALIB-NEGCTRL','ANALYSIS-CALIB-REVERSIBLE','ANALYSIS-ACC-CLARIFY','ANALYSIS-MEMBER-PROP','SCOPE-OUTPUT-TRANSFORM','POLICY-METRIC-CHANGE','POLICY-FORMATION','LOCAL-POLICY-LIMITATION'],
 'temperature':read(RESULTS/'calib_neg_control.json'),'scores':{'member':member,'nonmember':nonmember},
 'patches':[
 {'title':'收窄温度变换的科学解释','label':'原研究记录','trigger':'研究员要求核查可逆性与解释范围','before':'固定攻击 AUC 下降，容易被表述为隐私风险减少或遗忘有效。','after':'限定为本批样本和固定攻击对输出表示敏感；已知温度与完整正概率下映射可逆，不能推断训练信息被删除。','evidence':'温度负对照、可逆性核对与研究图记录','preserved':'原模型参数和实际实验数值','node':'ANALYSIS-CALIB-REVERSIBLE'},
 {'title':'澄清审计集与独立测试集口径','label':'原研究记录','trigger':'研究员要求区分两个准确率的计算对象','before':'混合审计集准确率 0.8275 与独立测试集准确率 0.6927 容易被混用。','after':'分别注明样本来源；不把不同口径的差异归因于模型变化。','evidence':'原模型结果与 bootstrap 分析文件','preserved':'两组原始数值及其实际计算范围','node':'ANALYSIS-ACC-CLARIFY'},
 {'title':'修正“始终猜非成员”的基线列','label':'本地复算修订','local':True,'trigger':'用户指出基线不应随攻击阈值变化','before':'50% 成员：0.390 / 0.245 / 0.168；10% 成员：0.542 / 0.413 / 0.302，被误写为始终猜非成员准确率。','after':'正确值分别固定为 0.50 和 0.90。旧列保留为“当前攻击预测为非成员的比例”；记录策略 v1.0 未拦住此错误。','evidence':'400 条已有 loss 分数的标准库复算','preserved':'原实验、原始 rev13、模型与历史错误记录','node':'ANALYSIS-MEMBER-PROP'}]}
payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
(ROOT/'dist/data.js').write_text('/* Actual case data; see docs/PROVENANCE.md. */\nwindow.RP_DATA = '+payload+';\n',encoding='utf-8')
manifest={str(p.relative_to(ROOT/'dist')).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in OUT.rglob('*') if p.is_file()}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'nodes':len(latest['nodes']),'edges':len(latest['edges']),'auc':auc,'rows':len(rows),'output':str(OUT)},ensure_ascii=False))
