import json
from play import DATA
v=json.load(open(DATA/'script-output/astra/inspection.json'))
b=[]
def build(n,x,y,d=0):b.append(dict(op='build',name=n,at=[x,y],direction=d))
def ins(n,x,y,d,item):
 build(n,x,y,d);b.append(dict(op='inserter_filter',name=n,at=[x,y],item=item))
for x,y in [(-82.5,-60.5),(-84.5,-53.5)]:build('medium-electric-pole',x,y)
build('assembling-machine-1',-84.5,-59.5)
b.append(dict(op='recipe',name='assembling-machine-1',at=[-84.5,-59.5],recipe='copper-cable'))
for y in range(-69,-62):build('transport-belt',-82.5,y+.5,12 if y==-63 else 8)
build('transport-belt',-83.5,-62.5,8)
for y in [-56.5,-55.5,-54.5]:build('transport-belt',-84.5,y,8)
ins('fast-inserter',-82.5,-69.5,0,'copper-plate')
ins('fast-inserter',-83.5,-61.5,0,'copper-plate')
ins('fast-inserter',-84.5,-57.5,0,'copper-cable')
for y in [-56.5,-55.5,-54.5]:ins('long-handed-inserter',-86.5,y,4,'copper-cable')
boxes=[]
for a in b:
 if a['op']!='build':continue
 x,y=a['at'];h=1.35 if a['name']=='assembling-machine-1' else .4;box=(x-h,y-h,x+h,y+h)
 for e in v['entities']:
  if e['type']in['resource','corpse','entity-ghost','item-entity']:continue
  z=e.get('bounding_box')
  if not z:continue
  l,r=z['left_top'],z['right_bottom'];assert not(box[0]<r['x']and box[2]>l['x']and box[1]<r['y']and box[3]>l['y']),(a,e['name'],e['position'])
 for z,p in boxes:assert not(box[0]<z[2]and box[2]>z[0]and box[1]<z[3]and box[3]>z[1]),(a,p)
 boxes.append((box,a))
a=[dict(op='take',name='assembling-machine-2',at=[-120.5,-59.5],inventory='assembling_machine_input',item='steel-plate',count=3)]
for n,c in [('assembling-machine-1',1),('medium-electric-pole',2),('transport-belt',6),('long-handed-inserter',3),('fast-inserter',2)]:a.extend([dict(op='craft',recipe=n,count=c),dict(op='wait_crafting')])
a+=b+[dict(op='save')]
json.dump(a,open('plans/remote-wire-second-auto.json','w'),indent=2)
print('checked',len(b),'actions')
