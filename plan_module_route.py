import json,heapq,math
from play import DATA
s=json.loads((DATA/'script-output/astra/inspection.json').read_text()); scan=json.loads((DATA/'script-output/astra/scan.json').read_text())
land={(int(t['position']['x']),int(t['position']['y'])) for t in scan['tiles'] if 'water' not in t['name'] and t['name']!='out-of-map'}
free={(x,y) for x,y in land if -65<=x<=22 and -73<=y<=71}
for e in s['entities']:
 if e['type'] in ['entity-ghost','corpse','character','item-entity','resource']:continue
 b=e.get('bounding_box');
 if not b:continue
 l,r=b['left_top'],b['right_bottom']
 for x in range(math.floor(l['x']-.4),math.ceil(r['x']+.4)):
  for y in range(math.floor(l['y']-.4),math.ceil(r['y']+.4)):
   if l['x']<x+.9 and r['x']>x+.1 and l['y']<y+.9 and r['y']>y+.1:free.discard((x,y))
free.difference_update([(2, 18), (18, 66)])
D=[(0,-1),(1,0),(0,1),(-1,0)];start=(2,19,2,False);end=(18,67)
assert start[:2] in free and end in free
q=[(0,start)];dist={start:0};prev={}
while q:
 cost,n=heapq.heappop(q)
 if cost!=dist[n]:continue
 x,y,di,lock=n
 if (x,y)==end:break
 for d,(dx,dy) in enumerate(D):
  if lock and d!=di:continue
  choices=[(1,1,False)]
  if not lock and d==di:choices += [(k,8,True) for k in range(2,6)]
  for k,w,ug in choices:
   t=(x+dx*k,y+dy*k,d,ug)
   if t[:2] not in free:continue
   if ug and (x+dx*(k+1),y+dy*(k+1)) not in free:continue
   nc=cost+w
   if nc<dist.get(t,1e9):dist[t]=nc;prev[t]=(n,ug);heapq.heappush(q,(nc,t))
else:raise RuntimeError('no path')
route=[]
while n!=start:
 p,ug=prev[n];route.append({'from':list(p[:2]),'to':list(n[:2]),'dir':n[2]*4,'ug':ug});n=p
route.reverse();json.dump(route,open('plans/module-route.json','w'),indent=2)
print('steps',len(route),'underground pairs',sum(e['ug'] for e in route),'start',start,'end',end)
print([e for e in route if e['ug']])
