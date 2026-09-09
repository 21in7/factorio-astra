import json
a=[{'op':'wait_inventory','name':'iron-chest','at':[-96.5,-72.5],'inventory':'chest','item':'iron-plate','count':50},{'op':'take','name':'iron-chest','at':[-96.5,-72.5],'item':'iron-plate','count':50}]
for recipe,count in [('pipe',43),('chemical-plant',1),('pipe-to-ground',3),('transport-belt',4),('underground-belt',1),('inserter',2),('medium-electric-pole',2)]:a +=[{'op':'craft','recipe':recipe,'count':count},{'op':'wait_crafting'}]
a +=[{'op':'build','name':'medium-electric-pole','at':[-86.5,-76.5]},{'op':'build','name':'medium-electric-pole','at':[-85.5,-68.5]},{'op':'build','name':'chemical-plant','at':[-84.5,-72.5],'direction':0},{'op':'recipe','name':'chemical-plant','at':[-84.5,-72.5],'recipe':'sulfur'}]
# Extend existing petroleum line with two underground pairs.
for name,at,d in [('pipe',[-94.5,-88.5],0),('pipe-to-ground',[-93.5,-88.5],12),('pipe-to-ground',[-85.5,-88.5],4),('pipe',[-84.5,-88.5],0),('pipe-to-ground',[-84.5,-87.5],0),('pipe-to-ground',[-84.5,-77.5],8),('pipe',[-84.5,-76.5],0),('pipe',[-83.5,-76.5],0),('pipe',[-83.5,-75.5],0),('pipe',[-83.5,-74.5],0)]:a.append({'op':'build','name':name,'at':at,'direction':d})
# Branch water; reuse mined endpoint, keep eastbound water connection.
a.append({'op':'mine','name':'pipe-to-ground','at':[-82.5,-75.5]})
for name,at,d in [('pipe-to-ground',[-86.5,-75.5],4),('pipe',[-85.5,-75.5],0),('pipe-to-ground',[-84.5,-75.5],12),('pipe-to-ground',[-82.5,-75.5],4),('pipe',[-85.5,-74.5],0)]:a.append({'op':'build','name':name,'at':at,'direction':d})
a +=[{'op':'build','name':'inserter','at':[-84.5,-70.5],'direction':0},{'op':'inserter_filter','name':'inserter','at':[-84.5,-70.5],'item':'sulfur'}]
for name,at,d in [('transport-belt',[-84.5,-69.5],12),('transport-belt',[-85.5,-69.5],12),('underground-belt',[-86.5,-69.5],12),('underground-belt',[-89.5,-69.5],4),('transport-belt',[-90.5,-69.5],12),('transport-belt',[-91.5,-69.5],12)]:a.append({'op':'build','name':name,'at':at,'direction':d})
a +=[{'op':'build','name':'inserter','at':[-92.5,-69.5],'direction':4},{'op':'inserter_filter','name':'inserter','at':[-92.5,-69.5],'item':'sulfur'},{'op':'inventory_bar','name':'iron-chest','at':[-93.5,-69.5],'bar':2},{'op':'save'}]
json.dump(a,open('plans/remote-sulfur-auto.json','w'),indent=2)
