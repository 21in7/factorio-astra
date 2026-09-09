import json,math,heapq
from collections import Counter
from play import DATA
s=json.load(open(DATA/'script-output/astra/inspection.json'));scan=json.load(open(DATA/'script-output/astra/scan.json'))
land={(math.floor(t['position']['x']),math.floor(t['position']['y']))for t in scan['tiles']if 'water'not in t['name']and t['name']!='out-of-map'}
b=[]
def B(n,p,d=0):b.append({'op':'build','name':n,'at':p,'direction':d})
def I(n,p,d,item):B(n,p,d);b.append({'op':'inserter_filter','name':n,'at':p,'item':item})
s['entities']=[e for e in s['entities'] if not(e['name']=='medium-electric-pole'and e['position']=={'x':-100.5,'y':-62.5})]
B('medium-electric-pole',[-101.5,-62.5])
B('medium-electric-pole',[-97.5,-53.5])
I('inserter',[-91.5,-59.5],4,'copper-cable')
I('inserter',[-98.5,-62.5],0,'copper-cable')
I('inserter',[-99.5,-53.5],8,'electronic-circuit')
I('inserter',[-100.5,-62.5],0,'electronic-circuit')
I('inserter',[-88.5,-67.5],4,'plastic-bar')
I('long-handed-inserter',[-99.5,-65.5],0,'plastic-bar')
b.append({'op':'inserter_filter','name':'inserter','at':[-99.5,-62.5],'item':'plastic-bar'})
b.append({'op':'inventory_bar','name':'iron-chest','at':[-99.5,-63.5],'bar':2})
# Check planned footprints against all existing physical entities and each other.
boxes=[]
for a in b:
 if a['op']!='build':continue
 x,y=a['at'];h=1.4 if a['name']=='assembling-machine-1'else .4;box=(x-h,y-h,x+h,y+h)
 for e in s['entities']:
  if e['type']in['entity-ghost','corpse','character','resource','item-entity']:continue
  z=e.get('bounding_box')
  if not z:continue
  l,r=z['left_top'],z['right_bottom'];assert not(box[0]<r['x'] and box[2]>l['x'] and box[1]<r['y'] and box[3]>l['y']),(a,e['name'],e['position'])
 for z,old in boxes:assert not(box[0]<z[2]and box[2]>z[0]and box[1]<z[3]and box[3]>z[1]),(a,old)
 boxes.append((box,a))
free=set(land)
for e in s['entities']:
 if e['type']in['entity-ghost','corpse','character','resource','item-entity']:continue
 z=e.get('bounding_box')
 if not z:continue
 l,r=z['left_top'],z['right_bottom']
 boxes.append(((l['x'],l['y'],r['x'],r['y']),e))
for (lx,ly,rx,ry),_ in boxes:
 for x in range(math.floor(lx-.4),math.ceil(rx+.4)):
  for y in range(math.floor(ly-.4),math.ceil(ry+.4)):
   if lx<x+.9 and rx>x+.1 and ly<y+.9 and ry>y+.1:free.discard((x,y))
for e in s['entities']:
 if e['type']=='transport-belt'or(e['type']=='underground-belt'and e.get('belt_to_ground_type')=='output'):
  dx,dy={0:(0,-1),4:(1,0),8:(0,1),12:(-1,0)}.get(e.get('direction'),(0,0));free.discard((math.floor(e['position']['x'])+dx,math.floor(e['position']['y'])+dy))
 if e['type']=='inserter'and e.get('drop_position'):
  p=e['drop_position'];free.discard((math.floor(p['x']),math.floor(p['y'])))
D=[(0,-1),(1,0),(0,1),(-1,0)]
def route(start,end,ed):
 assert start[:2]in free and end in free,('endpoint blocked',start,end)
 q=[(0,start)];costs={start:0};prev={}
 while q:
  cost,n=heapq.heappop(q)
  if cost!=costs[n]:continue
  x,y,di,lock=n
  if (x,y)==end and not lock and di!=(ed+2)%4:break
  for d,(dx,dy)in enumerate(D):
   if (lock and d!=di)or d==(di+2)%4:continue
   choices=[(1,1,False)]
   if not lock and d==di:choices +=[(k,8,True)for k in range(2,6)]
   for k,w,ug in choices:
    t=(x+dx*k,y+dy*k,d,ug)
    if t[:2]not in free:continue
    if ug and (x+dx*(k+1),y+dy*(k+1))not in free:continue
    z=n;rep=False
    while True:
     if z[:2]==t[:2]:rep=True;break
     if z not in prev:break
     z=prev[z][0]
    if rep:continue
    nc=cost+w
    if nc<costs.get(t,1e9):costs[t]=nc;prev[t]=(n,ug);heapq.heappush(q,(nc,t))
 else:raise RuntimeError('route unavailable')
 r=[]
 while n!=start:
  p,ug=prev[n];r.append({'from':p[:2],'to':n[:2],'dir':n[2]*4,'ug':ug});n=p
 r.reverse();nodes={}
 for e in r:
  p,t=tuple(e['from']),tuple(e['to']);d=e['dir']
  if e['ug']:nodes[p]=('underground-belt',d);nodes[t]=('underground-belt',(d+8)%16)
  else:
   if p not in nodes or nodes[p][0]=='transport-belt':nodes[p]=('transport-belt',d)
   nodes.setdefault(t,('transport-belt',d))
 nodes[end]=('transport-belt',ed*4)
 for(x,y),(name,d)in nodes.items():B(name,[x+.5,y+.5],d);free.discard((x,y))
 return r
r2=route((-100,-55,0,False),(-101,-64),2)
r1=route((-93,-60,3,False),(-99,-64),2)
r3=route((-90,-68,3,False),(-100,-68),2)
counts=Counter(a['name']for a in b if a['op']=='build');print(dict(counts));print('UG', [e for r in[r1,r2,r3]for e in r if e['ug']])
a=[{'op':'wait_inventory','name':'iron-chest','at':[-96.5,-72.5],'inventory':'chest','item':'iron-plate','count':100},{'op':'take','name':'iron-chest','at':[-96.5,-72.5],'item':'iron-plate','count':100},{'op':'wait_inventory','name':'iron-chest','at':[-96.5,-72.5],'inventory':'chest','item':'iron-plate','count':100},{'op':'take','name':'iron-chest','at':[-96.5,-72.5],'item':'iron-plate','count':100},{'op':'mine','name':'medium-electric-pole','at':[-100.5,-62.5]}]
u=counts.get('underground-belt',0)//2
recipes=[('transport-belt',math.ceil((counts['transport-belt']+u*5)/2)),('underground-belt',u),('medium-electric-pole',1),('long-handed-inserter',counts['long-handed-inserter']),('inserter',counts['inserter'])]
for r,c in recipes:
 if c:a +=[{'op':'craft','recipe':r,'count':c},{'op':'wait_crafting'}]
a+=b+[{'op':'save'}]
json.dump(a,open('plans/remote-red-raw-auto.json','w'),indent=2)
json.dump({'cable':r1,'ec':r2,'plastic':r3},open('plans/remote-red-raw-routes.json','w'),indent=2)
