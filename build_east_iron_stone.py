import json,math
from collections import Counter
from play import DATA
v=json.load(open(DATA/'script-output/astra/inspection.json'))
b=[]
def build(n,x,y,d=0): b.append(dict(op='build',name=n,at=[x,y],direction=d))
def ins(n,x,y,item):
 build(n,x,y); b.append(dict(op='inserter_filter',name=n,at=[x,y],item=item))
mined=[('medium-electric-pole',[35.5,-114.5]),('small-electric-pole',[57.5,-95.5])]
for x,y in [(33.5,-120.5),(36.5,-100.5),(42.5,-100.5),(48.5,-100.5),(54.5,-100.5),(49.5,-105.5)]:build('medium-electric-pole',x,y)
build('small-electric-pole',56.5,-105.5)
for x in [45.5,49.5,53.5,57.5]:build('electric-mining-drill',x,-107.5,0)
for x in range(35,57,3):build('stone-furnace',x,-101)
# Ore runs west, then south, then east along furnace north faces.
for x in range(33,58):build('transport-belt',x+.5,-109.5,8 if x==33 else 12)
for y in range(-109,-104):build('transport-belt',33.5,y+.5,8)
for x in range(33,56):build('transport-belt',x+.5,-103.5,4)
# Coal comes from existing north coal belt, using a separate lane throughout.
ins('long-handed-inserter',34.5,-121.5,'coal')
for x in range(31,35):build('transport-belt',x+.5,-119.5,8 if x==31 else 12)
for y in range(-119,-115):build('transport-belt',31.5,y+.5,8)
build('underground-belt',31.5,-114.5,8);build('underground-belt',31.5,-110.5,0)
for y in range(-110,-105):build('transport-belt',31.5,y+.5,8)
build('transport-belt',31.5,-104.5,4)
build('underground-belt',32.5,-104.5,4);build('underground-belt',34.5,-104.5,12)
for x in range(35,57):build('transport-belt',x+.5,-104.5,4)
for x in range(34,59):build('transport-belt',x+.5,-98.5,4)
for x in range(35,57,3):
 ins('inserter',x-.5,-102.5,'iron-ore')
 ins('long-handed-inserter',x+.5,-102.5,'coal')
 ins('inserter',x-.5,-99.5,'iron-plate')
# Check footprints against live infrastructure and planned objects.
boxes=[]
for a in b:
 if a['op']!='build':continue
 x,y=a['at'];h={'electric-mining-drill':1.35,'stone-furnace':.7}.get(a['name'],.4)
 box=(x-h,y-h,x+h,y+h)
 for e in v['entities']:
  if e['type'] in ['resource','corpse','entity-ghost','item-entity']:continue
  if any(e['name']==n and e['position']==dict(x=p[0],y=p[1]) for n,p in mined):continue
  z=e.get('bounding_box')
  if not z:continue
  l,r=z['left_top'],z['right_bottom']
  assert not(box[0]<r['x'] and box[2]>l['x'] and box[1]<r['y'] and box[3]>l['y']),(a,e['name'],e['position'])
 for z,p in boxes:assert not(box[0]<z[2] and box[2]>z[0] and box[1]<z[3] and box[3]>z[1]),(a,p)
 boxes.append((box,a))
c=Counter(a['name'] for a in b if a['op']=='build');print(c)
a=[dict(op='mine',name=n,at=p) for n,p in mined]
for n,k in [('medium-electric-pole',5),('electric-mining-drill',4),('transport-belt',math.ceil((c['transport-belt']+10)/2)),('underground-belt',2),('long-handed-inserter',9),('inserter',16)]:
 a.extend([dict(op='craft',recipe=n,count=k),dict(op='wait_crafting')])
a+=b+[dict(op='save')]
json.dump(a,open('plans/east-iron-four-drills-eight-stone.json','w'),indent=2)
