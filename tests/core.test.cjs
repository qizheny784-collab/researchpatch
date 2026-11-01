const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const C=require('../dist/core.js');
const scores=JSON.parse(fs.readFileSync(path.join(__dirname,'../dist/assets/results/prior-scores.json'),'utf8'));

test('always-nonmember baseline is independent of the attack threshold',()=>{
  for(const p of [.5,.1])for(const t of [.01,.1,1])assert.equal(C.audit(scores.member_loss,scores.nonmember_loss,p,t).alwaysNonmember,1-p);
});
test('reproduces the corrected 10% prior example',()=>{
  const r=C.audit(scores.member_loss,scores.nonmember_loss,.1,.1);
  assert.ok(Math.abs(r.accuracy-.506)<1e-12);assert.ok(Math.abs(r.predictedNonmember-.413)<1e-12);
  assert.equal(r.alwaysNonmember,.9);assert.notEqual(r.predictedNonmember,r.alwaysNonmember);
});
test('AUC matches the recovered original scores, including ties',()=>{
  assert.ok(Math.abs(C.auc(scores.member_loss,scores.nonmember_loss)-.720025)<1e-12);
  assert.equal(C.auc([1],[1]),.5);
});
test('graph import rejects duplicate IDs and dangling edges',()=>{
  assert.throws(()=>C.normalize({nodes:[{id:'a'},{id:'a'}],edges:[]}));
  assert.throws(()=>C.normalize({nodes:[{id:'a'}],edges:[{from:'a',to:'b'}]}));
});
test('candidate impact search is bounded, cycle-safe and preserves unrelated nodes',()=>{
  const g=C.normalize({nodes:['a','b','c','d'].map(id=>({id})),edges:[{from:'a',to:'b'},{from:'b',to:'c'},{from:'c',to:'a'}]});
  assert.deepEqual([...C.impact(g,'a',1)],['a','b']);assert.equal(C.impact(g,'a',10).has('d'),false);
});
test('version comparison distinguishes added nodes from modified claims',()=>{
  const a=C.normalize({nodes:[{id:'a',text:'old'}],edges:[]});
  const b=C.normalize({nodes:[{id:'a',text:'revised'},{id:'b'}],edges:[]});
  const d=C.diff(a,b);assert.equal(d.changed.length,1);assert.equal(d.added.length,1);
});
test('case data has valid snapshots, and raw historical error remains in the source',()=>{
  const context={window:{}};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../dist/data.js'),'utf8'),context);
  const s=context.window.RP_DATA.snapshots;s.forEach(x=>C.normalize(x.state));
  assert.ok(s[1].state.nodes.find(n=>n.id==='ANALYSIS-MEMBER-PROP').text.includes('0.390'));
  assert.ok(s[2].state.nodes.find(n=>n.id==='ANALYSIS-MEMBER-PROP').text.includes('90%'));
});
