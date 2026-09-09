import json,math
routes=[]
for f,final in [('iron',4),('copper',8)]:
 r=json.load(open(f'plans/remote-ec-{f}-route.json'));nodes={}
 for e in r:
  p,t=tuple(e['from']),tuple(e['to']);d=e['dir']
  if e['ug']:nodes[p]=('underground-belt',d);nodes[t]=('underground-belt',(d+8)%16)
  else:
   if p not in nodes or nodes[p][0]=='transport-belt':nodes[p]=('transport-belt',d)
   nodes.setdefault(t,('transport-belt',d))
 nodes[tuple(r[-1]['to'])]=('transport-belt',final)
 routes.append([{'op':'build','name':n,'at':[x+.5,y+.5],'direction':d}for(x,y),(n,d)in nodes.items()])
n=sum(v['name']=='transport-belt'for r in routes for v in r);u=sum(v['name']=='underground-belt'for r in routes for v in r)//2
# Iron is taken from the new automatically supplied local chest.
a=[{'op':'wait_inventory','name':'iron-chest','at':[-96.5,-72.5],'inventory':'chest','item':'iron-plate','count':80},{'op':'take','name':'iron-chest','at':[-96.5,-72.5],'item':'iron-plate','count':80}]
for recipe,count in [('transport-belt',math.ceil((n+u*5)/2)),('underground-belt',u),('assembling-machine-2',2),('inserter',6),('medium-electric-pole',2),('iron-chest',1)]:a +=[{'op':'craft','recipe':recipe,'count':count},{'op':'wait_crafting'}]
a +=[{'op':'build','name':'medium-electric-pole','at':p}for p in[[-91.5,-60.5],[-91.5,-54.5]]]
for at,recipe in[([-89.5,-59.5],'copper-cable'),([-89.5,-55.5],'electronic-circuit')]:a +=[{'op':'build','name':'assembling-machine-2','at':at},{'op':'recipe','name':'assembling-machine-2','at':at,'recipe':recipe}]
for at,d,item in[([-94.5,-65.5],0,'iron-plate'),([-92.5,-64.5],12,'copper-plate')]:a +=[{'op':'build','name':'inserter','at':at,'direction':d},{'op':'inserter_filter','name':'inserter','at':at,'item':item}]
a +=routes[0]+routes[1]
for at,d,item in[([-89.5,-61.5],0,'copper-plate'),([-89.5,-57.5],0,'copper-cable'),([-91.5,-55.5],12,'iron-plate')]:a +=[{'op':'build','name':'inserter','at':at,'direction':d},{'op':'inserter_filter','name':'inserter','at':at,'item':item}]
a +=[{'op':'build','name':'iron-chest','at':[-89.5,-52.5]},{'op':'inventory_bar','name':'iron-chest','at':[-89.5,-52.5],'bar':2},{'op':'build','name':'inserter','at':[-89.5,-53.5],'direction':0},{'op':'inserter_filter','name':'inserter','at':[-89.5,-53.5],'item':'electronic-circuit'},{'op':'save'}]
json.dump(a,open('plans/remote-ec-cell-auto.json','w'),indent=2);print('normal',n,'ugpairs',u)
