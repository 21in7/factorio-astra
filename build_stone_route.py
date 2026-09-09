import json
from play import send
r=json.load(open('plans/stone-route.json'));spec={}
for e in r:
 f=tuple(e['from']);t=tuple(e['to']);d=e['dir']
 if e['ug']:
  spec[f]=('underground-belt',d);spec[t]=('underground-belt',(d+8)%16)
 elif f not in spec:spec[f]=('transport-belt',d)
spec[tuple(r[-1]['to'])]=('transport-belt',0)
a=[{'op':'take','name':'iron-chest','at':[55.5,-113.5],'inventory':'chest','item':'iron-plate','count':400},{'op':'craft','recipe':'transport-belt','count':100},{'op':'craft','recipe':'underground-belt','count':2},{'op':'craft','recipe':'inserter','count':2},{'op':'wait_crafting'}]
a += [{'op':'build','name':name,'at':[x+.5,y+.5],'direction':d} for (x,y),(name,d) in spec.items()]
a += [{'op':'build','name':'inserter','at':[11.5,66.5],'direction':8},{'op':'build','name':'inserter','at':[-44.5,-68.5],'direction':4},{'op':'inventory_bar','name':'iron-chest','at':[11.5,65.5],'bar':5},{'op':'save'}]
json.dump(a,open('plans/stone-route-actions.json','w'),indent=2);print('builds',len(spec),flush=True);send(a)
