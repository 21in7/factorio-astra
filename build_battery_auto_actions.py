import json,math
routes=[]
for name,final in [('battery-copper',12),('battery-frame',0)]:
 r=json.load(open(f'plans/{name}-route.json'));nodes={}
 for e in r:
  p,t=tuple(e['from']),tuple(e['to']);d=e['dir']
  if e['ug']:nodes[p]=('underground-belt',d);nodes[t]=('underground-belt',(d+8)%16)
  else:
   if p not in nodes or nodes[p][0]=='transport-belt':nodes[p]=('transport-belt',d)
   nodes.setdefault(t,('transport-belt',d))
 nodes[tuple(r[-1]['to'])]=('transport-belt',final)
 routes.append([{'op':'build','name':n,'at':[x+.5,y+.5],'direction':d}for(x,y),(n,d)in nodes.items()])
normal=sum(a['name']=='transport-belt'for r in routes for a in r);ug=sum(a['name']=='underground-belt'for r in routes for a in r)//2
beltcount=math.ceil((normal+ug*5-1)/2)
a=[{'op':'take','name':'iron-chest','at':p,'item':'iron-plate','count':100}for p in[[12.5,12.5],[4.5,16.5]]]
for recipe,count in [('transport-belt',beltcount),('underground-belt',ug),('long-handed-inserter',1),('inserter',3),('medium-electric-pole',2)]:a +=[{'op':'craft','recipe':recipe,'count':count},{'op':'wait_crafting'}]
a +=[{'op':'build','name':'medium-electric-pole','at':[-92.5,-66.5]},{'op':'build','name':'long-handed-inserter','at':[-91.5,-68.5],'direction':0},{'op':'inserter_filter','name':'long-handed-inserter','at':[-91.5,-68.5],'item':'copper-plate'}]+routes[0]+[{'op':'build','name':'inserter','at':[-94.5,-63.5],'direction':4},{'op':'inserter_filter','name':'inserter','at':[-94.5,-63.5],'item':'copper-plate'},{'op':'put','name':'chemical-plant','at':[-96.5,-63.5],'inventory':'assembling_machine_input','item':'iron-plate','count':50}]
a +=[{'op':'build','name':'medium-electric-pole','at':[-94.5,-58.5]},{'op':'build','name':'inserter','at':[-96.5,-59.5],'direction':0},{'op':'inserter_filter','name':'inserter','at':[-96.5,-59.5],'item':'battery'}]+routes[1]+[{'op':'build','name':'inserter','at':[-116.5,-67.5],'direction':12},{'op':'inserter_filter','name':'inserter','at':[-116.5,-67.5],'item':'battery'},{'op':'save'}]
json.dump(a,open('plans/battery-copper-and-frame-auto.json','w'),indent=2);print('normal',normal,'ugpairs',ug,'beltrecipes',beltcount)
