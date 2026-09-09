import json,math
r=json.load(open('plans/lds-steel-route.json'));nodes={}
for e in r:
 p=tuple(e['from']);t=tuple(e['to']);d=e['dir']
 if e['ug']:
  name='fast-underground-belt'if sum(abs(a-b)for a,b in zip(p,t))>5 else'underground-belt'
  nodes[p]=(name,d);nodes[t]=(name,(d+8)%16)
 else:
  if p not in nodes or nodes[p][0]=='transport-belt':nodes[p]=('transport-belt',d)
  nodes.setdefault(t,('transport-belt',d))
nodes[tuple(r[-1]['to'])]=('transport-belt',8)
normal=sum(n=='transport-belt'for n,d in nodes.values());yellow=sum(n=='underground-belt'for n,d in nodes.values())//2;red=sum(n=='fast-underground-belt'for n,d in nodes.values())//2
beltrecipes=math.ceil((normal+5*(yellow+red)-1)/2)
a=[{'op':'take','name':'iron-chest','at':p,'item':'iron-plate','count':100}for p in[[12.5,12.5],[4.5,16.5]]]
for name,num in [('transport-belt',beltrecipes),('underground-belt',yellow+red),('fast-underground-belt',red),('long-handed-inserter',1),('inserter',1),('medium-electric-pole',1)]:
 a +=[{'op':'craft','recipe':name,'count':num},{'op':'wait_crafting'}]
a += [{'op':'build','name':'medium-electric-pole','at':[-7.5,51.5]},{'op':'build','name':'long-handed-inserter','at':[-6.5,51.5],'direction':0},{'op':'inserter_filter','name':'long-handed-inserter','at':[-6.5,51.5],'item':'steel-plate'}]
a += [{'op':'build','name':n,'at':[x+.5,y+.5],'direction':d}for(x,y),(n,d)in nodes.items()]
a +=[{'op':'build','name':'inserter','at':[-120.5,-61.5],'direction':0},{'op':'inserter_filter','name':'inserter','at':[-120.5,-61.5],'item':'steel-plate'},{'op':'save'}]
json.dump(a,open('plans/lds-steel-auto-actions.json','w'),indent=2)
print(normal,yellow,red,beltrecipes,'builds',len(nodes))
