import json,math
r=json.load(open('plans/remote-iron-route.json'));nodes={}
for e in r:
 p,t=tuple(e['from']),tuple(e['to']);d=e['dir']
 if e['ug']:nodes[p]=('underground-belt',d);nodes[t]=('underground-belt',(d+8)%16)
 else:
  if p not in nodes or nodes[p][0]=='transport-belt':nodes[p]=('transport-belt',d)
  nodes.setdefault(t,('transport-belt',d))
nodes[tuple(r[-1]['to'])]=('transport-belt',8)
nodes.update({(-95,-73):('underground-belt',8),(-95,-68):('underground-belt',0),(-95,-67):('transport-belt',12),(-96,-67):('transport-belt',12),(-97,-67):('transport-belt',8)})
normal=sum(n=='transport-belt'for n,d in nodes.values());ug=sum(n=='underground-belt'for n,d in nodes.values())//2
br=math.ceil((normal+ug*5)/2);a=[]
for recipe,count in [('transport-belt',br),('underground-belt',ug),('inserter',3),('medium-electric-pole',1)]:a +=[{'op':'craft','recipe':recipe,'count':count},{'op':'wait_crafting'}]
a +=[{'op':'build','name':'medium-electric-pole','at':[16.5,-119.5]},{'op':'build','name':'inserter','at':[19.5,-116.5],'direction':4},{'op':'inserter_filter','name':'inserter','at':[19.5,-116.5],'item':'iron-plate'}]
a +=[{'op':'build','name':n,'at':[x+.5,y+.5],'direction':d}for(x,y),(n,d)in nodes.items()]
a +=[{'op':'build','name':'inserter','at':[-96.5,-65.5],'direction':0},{'op':'inserter_filter','name':'inserter','at':[-96.5,-65.5],'item':'iron-plate'},{'op':'inventory_bar','name':'iron-chest','at':[-96.5,-72.5],'bar':2},{'op':'build','name':'inserter','at':[-95.5,-72.5],'direction':4},{'op':'inserter_filter','name':'inserter','at':[-95.5,-72.5],'item':'iron-plate'},{'op':'save'}]
json.dump(a,open('plans/remote-iron-auto-actions.json','w'),indent=2);print('normal',normal,'ugpairs',ug,'beltrecipes',br)
