import json
from play import DATA
v=json.load(open(DATA/'script-output/astra/inspection.json'))
b=[]
def build(n,x,y,d=0):b.append(dict(op='build',name=n,at=[x,y],direction=d))
def ins(n,x,y,d,item):
 build(n,x,y,d);b.append(dict(op='inserter_filter',name=n,at=[x,y],item=item))
for x,y in [(42.5,-96.5),(50.5,-96.5),(58.5,-96.5),(63.5,-103.5),(63.5,-106.5),(63.5,-111.5),(63.5,-119.5)]:build('medium-electric-pole',x,y)
build('assembling-machine-1',63.5,-116.5)
b.append(dict(op='recipe',name='assembling-machine-1',at=[63.5,-116.5],recipe='firearm-magazine'))
for y in [-112.5,-113.5]:build('transport-belt',63.5,y,0)
for y in [-116.5,-117.5]:build('transport-belt',66.5,y,0)
for y in range(-114,-107):build('transport-belt',64.5,y+.5,8)
ins('long-handed-inserter',61.5,-112.5,12,'iron-plate')
ins('inserter',63.5,-114.5,8,'iron-plate')
ins('inserter',65.5,-116.5,12,'firearm-magazine')
ins('inserter',64.5,-114.5,0,'firearm-magazine')
ins('inserter',66.5,-118.5,8,'firearm-magazine')
ins('inserter',65.5,-107.5,12,'firearm-magazine')
boxes=[]
for a in b:
 if a['op']!='build':continue
 x,y=a['at'];h=1.35 if a['name']=='assembling-machine-1'else .4;box=(x-h,y-h,x+h,y+h)
 for e in v['entities']:
  if e['type']in['resource','corpse','entity-ghost','item-entity']:continue
  z=e.get('bounding_box')
  if not z:continue
  l,r=z['left_top'],z['right_bottom'];assert not(box[0]<r['x']and box[2]>l['x']and box[1]<r['y']and box[3]>l['y']),(a,e['name'],e['position'])
 for z,p in boxes:assert not(box[0]<z[2]and box[2]>z[0]and box[1]<z[3]and box[3]>z[1]),(a,p)
 boxes.append((box,a))
a=[]
for n,c in [('medium-electric-pole',7),('assembling-machine-1',1),('transport-belt',6),('long-handed-inserter',1),('inserter',5)]:a.extend([dict(op='craft',recipe=n,count=c),dict(op='wait_crafting')])
a+=b+[dict(op='save')];json.dump(a,open('plans/east-ammo-auto.json','w'),indent=2);print('checked',len(b))
