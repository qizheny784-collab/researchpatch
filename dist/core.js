(function (root) {
  'use strict';
  const statuses = {
    valid: ['已核查', 'green'], needs_check: ['待核查', 'amber'], proposed: ['候选', 'blue'],
    unknown: ['未验证', 'gray'], needs_rerun: ['需重算', 'amber'], needs_narrowing: ['需收窄', 'amber'],
    contradicted: ['存在反证', 'red'], withdrawn: ['已撤回', 'red'], superseded: ['历史版本', 'gray']
  };
  const relations = {depends_on:'依赖', supports:'支持', contradicts:'反驳', derived_from:'来源', constrains:'约束', checks:'检查', revises:'修订', motivates:'促成', informs:'提供依据', documents:'记录', limits:'限定', replaces:'替代'};
  const types = {question:'研究问题', literature:'文献', hypothesis:'假设', data:'数据', experiment:'实验', finding:'发现', result:'结果', claim:'论断', decision:'决策', policy:'策略', process:'过程', code:'代码', figure:'图表'};
  function normalize(input) {
    if (!input || !Array.isArray(input.nodes) || !Array.isArray(input.edges)) throw new Error('状态需要 nodes 与 edges 数组');
    if (input.nodes.length > 300 || input.edges.length > 2000) throw new Error('请导入不超过 300 个节点、2000 条边的项目或子图');
    const seen = new Set();
    const nodes = input.nodes.map(n => {
      if (!n || typeof n.id !== 'string' || !n.id.trim() || seen.has(n.id)) throw new Error('节点 ID 缺失或重复');
      seen.add(n.id);
      return {...n, text:String(n.text || n.id), type:String(n.type || 'claim'), status:String(n.status || 'unknown'), source_refs:Array.isArray(n.source_refs)?n.source_refs:[]};
    });
    const edgeIds=new Set();
    const edges=input.edges.map((e,i)=>{
      if(!e || !seen.has(e.from) || !seen.has(e.to)) throw new Error('关系引用了不存在的节点');
      const id=String(e.id || 'edge-'+i); if(edgeIds.has(id))throw new Error('关系 ID 重复');edgeIds.add(id);
      return {...e,id,relation:String(e.relation||'depends_on')};
    });
    return {...input,project_id:String(input.project_id||'imported-project'),nodes,edges,support_groups:Array.isArray(input.support_groups)?input.support_groups:[]};
  }
  function impact(graph, start, maxDepth=3) {
    const found=new Set([start]), depth=new Map([[start,0]]), queue=[start];
    while(queue.length){const id=queue.shift();if(depth.get(id)>=maxDepth)continue;
      graph.edges.filter(e=>e.from===id).forEach(e=>{if(!found.has(e.to)){found.add(e.to);depth.set(e.to,depth.get(id)+1);queue.push(e.to);}});
    }
    return found;
  }
  function neighborhood(graph, start, hops=1) {
    let set=new Set([start]);for(let i=0;i<hops;i++){const next=new Set(set);graph.edges.forEach(e=>{if(set.has(e.from)||set.has(e.to)){next.add(e.from);next.add(e.to);}});set=next;}return set;
  }
  function diff(before,after){
    const old=new Map(before.nodes.map(n=>[n.id,n])), current=new Map(after.nodes.map(n=>[n.id,n]));
    return {added:after.nodes.filter(n=>!old.has(n.id)),removed:before.nodes.filter(n=>!current.has(n.id)),changed:after.nodes.filter(n=>old.has(n.id)&&JSON.stringify(old.get(n.id))!==JSON.stringify(n)).map(n=>({before:old.get(n.id),after:n}))};
  }
  function audit(lossMember,lossNonmember,prior,threshold){
    if(!lossMember.length||!lossNonmember.length||prior<=0||prior>=1)throw new Error('需要两组分数与 0 到 1 之间的成员比例');
    const recall=lossMember.filter(x=>x<threshold).length/lossMember.length;
    const fpr=lossNonmember.filter(x=>x<threshold).length/lossNonmember.length;
    const tp=prior*recall,tn=(1-prior)*(1-fpr),fp=(1-prior)*fpr;
    return {accuracy:tp+tn,precision:tp+fp?tp/(tp+fp):null,recall,fpr,alwaysNonmember:1-prior,predictedNonmember:tn+prior*(1-recall)};
  }
  function auc(member,nonmember){let wins=0;member.forEach(m=>nonmember.forEach(n=>{wins+=m<n?1:m===n?.5:0;}));return wins/(member.length*nonmember.length);}
  const api={statuses,relations,types,normalize,impact,neighborhood,diff,audit,auc};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.RPCore=api;
})(typeof window!=='undefined'?window:globalThis);
