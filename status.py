#!/usr/bin/env python3
import json
from play import read
s=read()
def inv(xs):return {x['name']:x['count'] for x in xs} if isinstance(xs,list) else {}
r=s['research']
for action in [s.get('active') or {}]+[e.get('action',{}) for e in s['log']]:
 action.pop('path',None)
print(json.dumps({'tick':s['tick'],'position':s['position'],'health':s['health'],'inventory':inv(s['inventory']),'crafting':s.get('crafting'),'active':s.get('active'),'pending':len(s.get('queue',[])),'research':{'current':r.get('current'),'progress':r['progress'],'done':r['done']},'last':s['log'][-3:]},ensure_ascii=False))
for e in s['entities']:
 if e['type'] in ['mining-drill','furnace','lab','assembling-machine','boiler','generator']:
  v=e.get('inventories',{})
  names={'mining-drill':['fuel'],'furnace':['fuel','furnace_source','furnace_result'],'lab':['lab_input'],'assembling-machine':['assembling_machine_input','assembling_machine_output'],'boiler':['fuel'],'generator':[]}[e['type']]
  print(json.dumps({'name':e['name'],'at':e['position'],'id':e.get('id'),'status':e.get('status'),'energy':e.get('energy'),'recipe':e.get('recipe'),'inventories':{n:inv(v.get(n)) for n in names}},ensure_ascii=False))
