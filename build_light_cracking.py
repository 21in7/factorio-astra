import json
from collections import Counter
from play import DATA
s=json.load(open(DATA/'script-output/astra/inspection.json'))
b=[]
def B(n,p,d=0):b.append({'op':'build','name':n,'at':p,'direction':d})
B('chemical-plant',[-104.5,-98.5],4)
b.append({'op':'recipe','name':'chemical-plant','at':[-104.5,-98.5],'recipe':'light-oil-cracking'})
for p in[[-91.5,-102.5],[-99.5,-102.5],[-107.5,-100.5]]:B('medium-electric-pole',p)
# Light oil from the tank's northwest outlet, to east/lower inlet.
for p in[[-100.5,-95.5],[-101.5,-95.5],[-101.5,-96.5],[-101.5,-97.5],[-102.5,-97.5]]:B('pipe',p)
# Water from the refinery inlet; underground crosses oil networks without joining.
for p in[[-99.5,-82.5],[-100.5,-82.5],[-100.5,-93.5],[-100.5,-101.5],[-101.5,-101.5],[-101.5,-100.5],[-101.5,-99.5],[-102.5,-99.5]]:B('pipe',p)
for p,d in[([-100.5,-83.5],8),([-100.5,-92.5],0),([-100.5,-94.5],8),([-100.5,-100.5],0)]:B('pipe-to-ground',p,d)
# Gas output west, routed north and then east to existing gas pipe93.5,-100.5.
for p in[[-106.5,-99.5],[-106.5,-104.5],[-94.5,-104.5],[-94.5,-103.5],[-94.5,-102.5],[-94.5,-101.5],[-94.5,-100.5]]:B('pipe',p)
for p,d in[([-106.5,-100.5],8),([-106.5,-103.5],0),([-105.5,-104.5],12),([-95.5,-104.5],4)]:B('pipe-to-ground',p,d)
boxes=[]
for a in b:
 if a['op']!='build':continue
 p=a['at'];h=1.3 if a['name']=='chemical-plant'else .4
 box=(p[0]-h,p[1]-h,p[0]+h,p[1]+h)
 for e in s['entities']:
  if e['type']in['entity-ghost','resource','corpse','character','item-on-ground']:continue
  z=e.get('bounding_box')
  if z:
   l,r=z['left_top'],z['right_bottom'];assert not(box[0]<r['x']and box[2]>l['x']and box[1]<r['y']and box[3]>l['y']),(a,e['name'],e['position'])
 for z,o in boxes:assert not(box[0]<z[2]and box[2]>z[0]and box[1]<z[3]and box[3]>z[1]),(a,o)
 boxes.append((box,a))
c=Counter(a['name']for a in b if a['op']=='build');print(c)
a=[{'op':'take','name':'iron-chest','at':[-96.5,-72.5],'item':'iron-plate','count':100}]
for r,n in[('pipe',c['pipe']+c['pipe-to-ground']//2*10+5),('pipe-to-ground',c['pipe-to-ground']//2),('chemical-plant',1),('medium-electric-pole',3)]:a +=[{'op':'craft','recipe':r,'count':n},{'op':'wait_crafting'}]
a+=b+[{'op':'save'}];json.dump(a,open('plans/light-oil-cracking-auto.json','w'),indent=2)
