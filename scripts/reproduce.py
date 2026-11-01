"""Reproduce the prior-sensitivity correction with Python standard library."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'dist/assets/results/prior-scores.json').read_text(encoding='utf-8'))
m,n=data['member_loss'],data['nonmember_loss']
auc=sum(1 if a<b else .5 if a==b else 0 for a in m for b in n)/(len(m)*len(n))
print('Prior  Threshold  Attack acc  Always nonmember  Precision  Recall  FPR')
for pi in [.5,.1]:
    for t in [.01,.1,1.]:
        tpr=sum(x<t for x in m)/len(m);fpr=sum(x<t for x in n)/len(n)
        tp=pi*tpr;fp=(1-pi)*fpr;tn=(1-pi)*(1-fpr)
        precision=tp/(tp+fp) if tp+fp else 0
        print(f'{pi:5.2f}  {t:9.2f}  {tp+tn:10.4f}  {1-pi:16.4f}  {precision:9.4f}  {tpr:.4f}  {fpr:.4f}')
print(f'AUC = {auc:.6f}; fixed conditional score distributions, no new independent samples.')
