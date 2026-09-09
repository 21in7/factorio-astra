import json,math
from play import DATA
v=json.load(open(DATA/'script-output/astra/inspection.json'))
b=[]
def build(n,x,y,d=0):b.append({'op':'build','name':n,'at':[x,y],'direction':d})
for x,y in [(16.5,-138.5),(25.5,-130.5),(29.5,-130.5),(25.5,-126.5),(29.5,-126.5)]:build('medium-electric-pole',x,y)
for x in [14.5,18.5]:build('electric-mining-drill',x,-136.5,4)
for x in [24,28]:build('steel-furnace',x,-130)
# Separate ore paths preserve a dedicated drill for each furnace.
for y in [-136.5,-135.5]:build('transport-belt',16.5,y,8)
for x in range(16,25):build('transport-belt',x+.5,-134.5,8 if x==24 else 4)
for y in [-133.5,-132.5]:build('transport-belt',24.5,y,8)
for x in range(20,29):build('transport-belt',x+.5,-136.5,8 if x==28 else 4)
for y in [-135.5,-134.5,-133.5,-132.5]:build('transport-belt',28.5,y,8)
for x in range(21,28):build('transport-belt',x+.5,-124.5,12)
for x in [23.5,27.5]:build('transport-belt',x,-125.5,8)
for x in [23.5,27.5]:
 for p in [x,x+1]:build('iron-chest',p,-127.5);b.append({'op':'inventory_bar','name':'iron-chest','at':[p,-127.5],'bar':2})
 for p,y,d,item,n in [(x+1,-131.5,0,'iron-ore','inserter'),(x,-128.5,0,'iron-plate','inserter'),(x+1,-128.5,8,'coal','inserter'),(x,-126.5,0,'iron-plate','inserter'),(x+1,-125.5,8,'coal','long-handed-inserter')]:
  build(n,p,y,d);b.append({'op':'inserter_filter','name':n,'at':[p,y],'item':item})
# Existing entities and mutual planned footprints must be clear.
boxes=[]
for a in b:
 if a['op']!='build':continue
 n=a['name'];x,y=a['at'];h={'electric-mining-drill':1.35,'steel-furnace':.7}.get(n,.4)
 box=(x-h,y-h,x+h,y+h)
 for e in v['entities']:
  if e['type'] in ['resource','corpse','entity-ghost']:continue
  z=e.get('bounding_box')
  if not z:continue
  l=z['left_top'];r=z['right_bottom']
  assert not(box[0]<r['x'] and box[2]>l['x'] and box[1]<r['y'] and box[3]>l['y']),(a,e['name'],e['position'])
 for z,prev in boxes:assert not(box[0]<z[2] and box[2]>z[0] and box[1]<z[3] and box[3]>z[1]),(a,prev)
 boxes.append((box,a))
counts={}
for a in b:
 if a['op']=='build':counts[a['name']]=counts.get(a['name'],0)+1
print(counts)
a=[{'op':'take','name':'iron-chest','at':p,'item':'iron-plate','count':100}for p in [[12.5,12.5],[34.5,39.5]]]
for n,c in sorted(counts.items(), key=lambda kv: kv[0]=="inserter"):
 if n=='transport-belt':c=math.ceil(c/2)
 a.extend([{'op':'craft','recipe':n,'count':c},{'op':'wait_crafting'}])
a+=b+[{'op':'save'}]
json.dump(a,open('plans/north-iron-two-more.json','w'),indent=2)
