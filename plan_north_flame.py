import json,math,heapq
from play import DATA
s=json.loads((DATA/'script-output/astra/inspection.json').read_text());scan=json.loads((DATA/'script-output/astra/scan.json').read_text())
free={(int(t['position']['x']),int(t['position']['y'])) for t in scan['tiles'] if 'water' not in t['name'] and t['name']!='out-of-map' and -100<=t['position']['x']<=20 and -151<=t['position']['y']<=-87}
for e in s['entities']:
 if e['type'] in ['entity-ghost','corpse','character','item-entity','resource','unit']:continue
 b=e.get('bounding_box')
 if not b:continue
 l,r=b['left_top'],b['right_bottom'];pad=.4
 if e['type'] in ['pipe','pipe-to-ground','storage-tank','assembling-machine','oil-refinery','chemical-plant','pump'] and e['name'] in ['pipe','pipe-to-ground','storage-tank','oil-refinery','chemical-plant','pump']:
  pad=1.05
  if e['position']=={'x':-91.5,'y':-89.5}:pad=.4
 for x in range(math.floor(l['x']-pad),math.ceil(r['x']+pad)):
  for y in range(math.floor(l['y']-pad),math.ceil(r['y']+pad)):
   if l['x']-pad<x+.5<r['x']+pad and l['y']-pad<y+.5<r['y']+pad:free.discard((x,y))
for e in scan['entities']:
 if e['type'] in ['tree','simple-entity']:
  x,y=math.floor(e['position']['x']),math.floor(e['position']['y'])
  for dx in [-1,0,1]:
   for dy in [-1,0,1]:free.discard((x+dx,y+dy))
# Reserve the north-facing turret footprint.
for x in [12,13]:
 for y in [-141,-140,-139]:free.discard((x,y))
D=[(0,-1),(1,0),(0,1),(-1,0)];start=(-91,-90,1,False);end=(11,-139)
assert start[:2] in free,('start blocked',start)
assert end in free,('end blocked',end)
q=[(0,start)];dist={start:0};prev={}
while q:
 c,n=heapq.heappop(q)
 if c!=dist[n]:continue
 x,y,di,lock=n
 if (x,y)==end:break
 for d,(dx,dy) in enumerate(D):
  if lock and d!=di:continue
  if d==(di+2)%4:continue
  choices=[(1,1,False)]
  if not lock and d==di:choices += [(k,6,True) for k in range(2,11)]
  for k,w,ug in choices:
   t=(x+dx*k,y+dy*k,d,ug)
   if t[:2] not in free:continue
   if ug and (x+dx*(k+1),y+dy*(k+1)) not in free:continue
   nc=c+w
   if nc<dist.get(t,1e9):dist[t]=nc;prev[t]=(n,ug);heapq.heappush(q,(nc,t))
else:raise Exception('no path')
edges=[]
while n!=start:
 p,ug=prev[n];edges.append((p,n,ug));n=p
edges.reverse();nodes={start[:2]:('pipe',0)}
for p,n,ug in edges:
 if ug:nodes[p[:2]]=('pipe-to-ground',(n[2]*4+8)%16);nodes[n[:2]]=('pipe-to-ground',n[2]*4)
 else:nodes.setdefault(n[:2],('pipe',0))
assert len(nodes)==len(set(nodes))
acts=[{'op':'build','name':name,'at':[x+.5,y+.5],'direction':d} for (x,y),(name,d) in nodes.items()]
ug=sum(a['name']=='pipe-to-ground' for a in acts);pipes=len(acts)-ug
print('pipes',pipes,'ug',ug,'Fe cost',pipes+ug//2*15);print(json.dumps(acts))
json.dump(acts,open('plans/north-flame-pipeline.json','w'),indent=2)
json.dump([{'op':'craft','recipe':'pipe-to-ground','count':ug//2},{'op':'wait_crafting'},{'op':'craft','recipe':'pipe','count':pipes},{'op':'wait_crafting'}]+acts+[{'op':'build','name':'flamethrower-turret','at':[13,-139.5],'direction':0},{'op':'save'}],open('plans/north-flame-actions.json','w'),indent=2)
