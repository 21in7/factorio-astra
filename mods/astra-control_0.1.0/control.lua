local plan_store=require("plans")
local status_names={}
for name,value in pairs(defines.entity_status) do status_names[value]=name end
local function dist(a,b) return ((a.x-b.x)^2+(a.y-b.y)^2)^0.5 end
local function pos(a) return {x=a.x or a[1],y=a.y or a[2]} end
local function state() storage.astra=storage.astra or {queue={},log={}}; return storage.astra end
local function log(v) local s=state(); v.tick=game.tick; s.log[#s.log+1]=v; if #s.log>30 then table.remove(s.log,1) end; helpers.write_file('astra/audit.jsonl',helpers.table_to_json(v)..'\n',true) end
local function contents(inv) return inv and inv.valid and inv.get_contents() or {} end
local function entity(p,a)
 if a.id then for _,e in pairs(p.surface.find_entities_filtered{position=p.position,radius=100}) do if e.unit_number==a.id then return e end end end
 if a.at then local q=pos(a.at); local es=p.surface.find_entities_filtered{position=q,radius=a.radius or 0.2,name=a.name}; for _,e in pairs(es) do if e.type~='character' and e.type~='corpse' then return e end end end
end
local function observe(p,r)
 local s=state(); local out={controller_plan_version=plan_store._version,selected_gun_index=p.character and p.character.selected_gun_index,tick=game.tick,position=p.position,health=p.character and p.character.health or 0,alive=p.character~=nil,combat=s.combat,attack_alert=s.attack_alert,losses=s.losses,inventory=contents(p.get_main_inventory()),cursor=p.cursor_stack and p.cursor_stack.valid_for_read and {name=p.cursor_stack.name,count=p.cursor_stack.count} or nil,crafting=p.crafting_queue,queue=s.queue,active=s.active,log=s.log,entities={},resources={},research={current=p.force.current_research and p.force.current_research.name,progress=p.force.research_progress,available={},done={}},reach={build=p.build_distance,entity=p.reach_distance,resource=p.resource_reach_distance}}
 for n,t in pairs(p.force.technologies) do if t.researched then out.research.done[#out.research.done+1]=n elseif t.enabled then local ready=true;for _,pr in pairs(t.prerequisites) do if not pr.researched then ready=false end end;if ready then out.research.available[#out.research.available+1]={name=n,ingredients=t.research_unit_ingredients,count=t.research_unit_count} end end end
 out.equipment={ammo=contents(p.get_inventory(defines.inventory.character_ammo)),guns=contents(p.get_inventory(defines.inventory.character_guns)),armor=contents(p.get_inventory(defines.inventory.character_armor))}
 local groups={}
 for _,e in pairs(p.surface.find_entities_filtered{position=p.position,radius=r or 70}) do
  if p.force.is_chunk_charted(p.surface,{math.floor(e.position.x/32),math.floor(e.position.y/32)}) then
   if e.type=='resource' then
    local key=e.name..':'..math.floor(e.position.x/12)..':'..math.floor(e.position.y/12); local g=groups[key] or {name=e.name,count=0,amount=0,x=0,y=0,nearest=e.position,distance=dist(p.position,e.position)};g.count=g.count+1;g.amount=g.amount+e.amount;g.x=g.x+e.position.x;g.y=g.y+e.position.y;if dist(p.position,e.position)<g.distance then g.nearest=e.position;g.distance=dist(p.position,e.position) end;groups[key]=g
   elseif e.type~='character' and e.type~='corpse' and e.type~='particle-source' and e.type~='flying-text' then
    if e.force==p.force or dist(e.position,p.position)<35 or p.force.is_chunk_visible(p.surface,{math.floor(e.position.x/32),math.floor(e.position.y/32)}) then
     local v={name=e.name,type=e.type,position=e.position,bounding_box=e.bounding_box,id=e.unit_number,health=e.health,direction=e.direction,status=e.status,status_name=status_names[e.status]}
     if e.type=='entity-ghost' then v.ghost_name=e.ghost_name end
     if e.type=='tree' or e.type=='simple-entity' then v.mineable=e.minable else
      v.inventories={};for name,id in pairs(defines.inventory) do if name=='lab_modules' or name=='mining_drill_modules' or name=='assembling_machine_modules' or name=='roboport_robot' or name=='roboport_material' or name=='character_corpse' or name=='fuel' or name=='chest' or name=='furnace_source' or name=='furnace_result' or name=='assembling_machine_input' or name=='assembling_machine_output' or name=='lab_input' or name=='turret_ammo' or name=='rocket_silo_input' or name=='rocket_silo_result' then local ok,inv=pcall(function() return e.get_inventory(id) end);if ok and inv then v.inventories[name]=contents(inv) end end end
      if e.type=='container' then local inv=e.get_inventory(defines.inventory.chest);if inv and inv.supports_bar() then v.inventory_bar=inv.get_bar() end end
      if e.type=='roboport' then local n=e.logistic_network;if n then v.logistic_network={construction_robots=n.all_construction_robots,available_construction_robots=n.available_construction_robots} end end
      if e.type=='inserter' then v.use_filters=e.use_filters;v.filter_mode=e.inserter_filter_mode;v.filters={};for j=1,e.filter_slot_count do local f=e.get_filter(j);if f then v.filters[#v.filters+1]=f end end;v.pickup_position=e.pickup_position;v.drop_position=e.drop_position;local h=e.held_stack;if h and h.valid_for_read then v.held_stack={name=h.name,count=h.count} end end
      if e.type=='underground-belt' then v.belt_to_ground_type=e.belt_to_ground_type;local n=e.neighbours;v.underground_neighbour=n and n.position end
      if e.type=='transport-belt' or e.type=='underground-belt' then v.belt_contents={e.get_transport_line(1).get_contents(),e.get_transport_line(2).get_contents()} end
      if e.burner then v.burning=e.burner.currently_burning and e.burner.currently_burning.name;v.fuel_remaining=e.burner.remaining_burning_fuel end
      if e.type=='assembling-machine' or e.type=='furnace' or e.type=='rocket-silo' then local recipe=e.get_recipe();v.recipe=recipe and recipe.name;v.crafting_progress=e.crafting_progress end
      if e.electric_buffer_size then v.energy=e.energy end
      if e.type=='electric-pole' then v.electric_network_id=e.electric_network_id;v.wire_neighbours={};for _,c in pairs(e.get_wire_connectors(false)) do for _,w in pairs(c.connections) do local n=w.target.owner;if n and n.valid then v.wire_neighbours[#v.wire_neighbours+1]={name=n.name,position=n.position,id=n.unit_number} end end end end
      if e.fluidbox and #e.fluidbox>0 then v.fluids={};for i=1,#e.fluidbox do v.fluids[i]=e.fluidbox[i] end end
     end
     out.entities[#out.entities+1]=v
    end
   end
  end
 end
 for _,g in pairs(groups) do g.center={x=g.x/g.count,y=g.y/g.count};g.x=nil;g.y=nil;out.resources[#out.resources+1]=g end
 table.sort(out.resources,function(a,b)return a.distance<b.distance end)
 helpers.write_file('astra/state.json',helpers.table_to_json(out),false)
 if r then helpers.write_file('astra/inspection.json',helpers.table_to_json(out),false) end
end
local function finish(p,result)
 local s=state(); log({action=s.active,result=result});s.active=nil;p.walking_state={walking=false};p.mining_state={mining=false};p.repair_state={repairing=false,position=p.position};p.clear_cursor()
end
local function transfer(p,e,a)
 assert(e and e.valid,'entity not found');assert(p.can_reach_entity(e),'entity out of reach')
 local invname=a.inventory or (a.op=='put' and 'fuel' or 'chest');local inv=e.get_inventory((assert(defines.inventory[invname],'unknown inventory')));assert(inv,'entity has no inventory '..invname)
 local src=a.op=='put' and (a.player_inventory and p.get_inventory((assert(defines.inventory[a.player_inventory],'unknown player inventory'))) or p.get_main_inventory()) or inv;local dst=a.op=='put' and inv or p.get_main_inventory();local item={name=a.item,count=math.min(a.count or 100000,src.get_item_count(a.item)),quality='normal'}
 if item.count==0 then return 0 end
 local removed=src.remove(item);item.count=removed;local inserted=dst.insert(item);if inserted<removed then item.count=removed-inserted;assert(src.insert(item)==item.count,'transfer rollback failed') end
 return inserted
end
local dirs={0,2,4,6,8,10,12,14}
local function navigate(p,a,q,radius)
 assert(game.tick-a.started<(a.timeout or 3600),'navigation timeout')
 if dist(q,p.position)<=radius then p.walking_state={walking=false};return true end
 assert(not a.path_error,a.path_error or 'no path')
 if not a.path then
  if not a.path_request and (not a.retry_tick or game.tick>=a.retry_tick) then
   a.path_request=p.surface.request_path{bounding_box=p.character.prototype.collision_box,collision_mask=p.character.prototype.collision_mask,start=p.position,goal=q,force=p.force,radius=radius,can_open_gates=true,entity_to_ignore=p.character,pathfind_flags={cache=false,allow_destroy_friendly_entities=false,allow_paths_through_own_entities=false}}
  end
  p.walking_state={walking=false};return false
 end
 a.path_index=a.path_index or 1
 while a.path[a.path_index] and dist(p.position,a.path[a.path_index].position)<0.25 do a.path_index=a.path_index+1 end
 local waypoint=a.path[a.path_index]
 if not waypoint then a.path=nil;a.path_request=nil;return false end
 local dx=waypoint.position.x-p.position.x;local dy=waypoint.position.y-p.position.y;local ang=math.atan2(dx,-dy)
 p.walking_state={walking=true,direction=dirs[(math.floor(ang/(math.pi/4)+0.5)%8)+1]};return false
end
script.on_event(defines.events.on_script_path_request_finished,function(event)
 local a=state().active;if not a or a.path_request~=event.id then return end
 if event.try_again_later then a.path_request=nil;a.retry_tick=game.tick+60
 elseif event.path then a.path=event.path;a.path_index=1
 else a.path_error='no walkable path to target' end
end)
local function step(p,a)
 local s=state()
 if a.op=='walk_direction' then
  assert(type(a.direction)=='number' and a.direction%2==0 and a.direction>=0 and a.direction<=14,'invalid walking direction')
  assert(type(a.ticks)=='number' and a.ticks>=1 and a.ticks<=300,'walking duration out of range')
  if game.tick-a.started>=a.ticks then finish(p,{walked=true,position=p.position}) else p.walking_state={walking=true,direction=a.direction} end
 elseif a.op=='walk' then
  if navigate(p,a,pos(a.to),a.tolerance or 0.5) then finish(p,'arrived') end
 elseif a.op=='mine' then
  local e=entity(p,a); if not e then finish(p,'target exhausted');return end
  if not p.can_reach_entity(e) then
   navigate(p,a,e.position,2);return
  end
  p.walking_state={walking=false};a.mining_started=a.mining_started or game.tick
  p.selected=e;p.mining_state={mining=true,position=e.position}
  if game.tick-a.mining_started>=(a.ticks or 300) then finish(p,'mining interval completed') end
 elseif a.op=='repair' then
  local e=entity(p,a);if not e then finish(p,{repaired=false,reason='target missing'});return end
  if not p.can_reach_entity(e) then navigate(p,a,e.position,math.max(2,p.reach_distance-2));return end
  if e.health>=e.max_health then finish(p,{repaired=true,health=e.health});return end
  if not a.repair_started then assert(p.clear_cursor(),'cursor busy');assert(p.pipette(prototypes.item['repair-pack'],'normal',false),'repair pack unavailable');a.repair_started=game.tick end
  assert(game.tick-a.repair_started<3600,'repair timeout')
  p.walking_state={walking=false};p.selected=e;p.repair_state={repairing=true,position=e.position}
 elseif a.op=='wait' then if game.tick-a.started>=(a.ticks or 60) then finish(p,'wait completed') end
 elseif a.op=='wait_inventory' then local e=assert(entity(p,a),'inventory target missing');local inv=assert(e.get_inventory(assert(defines.inventory[a.inventory])),'inventory missing');local n=inv.get_item_count(a.item);if n>=(a.count or 1) then finish(p,{available=n}) end
 elseif a.op=='wait_research' then local t=assert(p.force.technologies[a.name],'unknown technology');if t.researched then finish(p,'research completed') end
 elseif a.op=='wait_player_item' then local n=p.get_main_inventory().get_item_count(a.item);if n>=(a.count or 1) then finish(p,{available=n}) end
 elseif a.op=='wait_crafting' then if not p.crafting_queue or #p.crafting_queue==0 then finish(p,'crafting completed') end
 elseif a.op=='craft' then local requested=a.count or 1;local n=p.begin_crafting{recipe=a.recipe,count=requested};assert(n==requested,'crafting shortage: queued '..n..' of '..requested..' for '..a.recipe);finish(p,{queued=n})
 elseif a.op=='build' then
  local q=pos(a.at);if a.name=='transport-belt' then local existing=p.surface.find_entity('transport-belt',q);if existing then assert(existing.direction==(a.direction or 0),'existing belt direction differs; use explicit rotate or crossing');finish(p,'already present');return end end;if dist(q,p.position)>p.build_distance then navigate(p,a,q,p.build_distance-2);return end;assert(p.clear_cursor(),'cursor could not clear');assert(p.pipette(prototypes.item[a.name],"normal",false),'item unavailable');local v={position=q,direction=a.direction or 0,build_mode=defines.build_mode.normal,terrain_building_size=1};assert(p.can_build_from_cursor(v),'placement blocked');p.build_from_cursor(v);finish(p,'built')
 elseif a.op=='rotate' then local e=assert(entity(p,a),'entity missing');if not p.can_reach_entity(e) then navigate(p,a,e.position,math.max(2,p.reach_distance-2));return end;finish(p,{rotated=e.rotate{by_player=p,reverse=a.reverse or false}})
 elseif a.op=='inserter_filter' then local e=assert(entity(p,a),'entity missing');assert(e.type=='inserter' and e.filter_slot_count>0,'inserter filters unavailable');if not p.can_reach_entity(e) then navigate(p,a,e.position,math.max(2,p.reach_distance-2));return end;local items=a.items or {a.item};assert(#items>0 and #items<=e.filter_slot_count,'invalid filter count');for _,item in ipairs(items) do assert(prototypes.item[item],'unknown filter item') end;for j=1,e.filter_slot_count do e.set_filter(j,nil) end;for j,item in ipairs(items) do e.set_filter(j,item) end;e.inserter_filter_mode='whitelist';e.use_filters=true;local filters={};for j=1,#items do filters[j]=e.get_filter(j) end;finish(p,{filter=e.get_filter(1),filters=filters,enabled=e.use_filters})
 elseif a.op=='inventory_bar' then local e=assert(entity(p,a),'entity missing');if not p.can_reach_entity(e) then navigate(p,a,e.position,math.max(2,p.reach_distance-2));return end;local inv=assert(e.get_inventory(defines.inventory.chest),'chest inventory missing');assert(inv.supports_bar(),'inventory does not support bar');assert(type(a.bar)=='number' and a.bar%1==0 and a.bar>=1 and a.bar<=#inv+1,'invalid bar');inv.set_bar(a.bar);finish(p,{bar=inv.get_bar()})
 elseif a.op=='put' or a.op=='take' then local e=assert(entity(p,a),'entity missing');if not p.can_reach_entity(e) then navigate(p,a,e.position,math.max(2,p.reach_distance-2));return end;finish(p,{transferred=transfer(p,e,a)})
 elseif a.op=='ghost' then
  local q=pos(a.at);if p.surface.find_entity(a.name,q) then finish(p,'already built');return end
  assert(p.force.is_chunk_charted(p.surface,{math.floor(q.x/32),math.floor(q.y/32)}),'uncharted ghost target')
  if dist(q,p.position)>p.build_distance then navigate(p,a,q,p.build_distance-2);return end
  assert(p.clear_cursor(),'cursor busy');p.cursor_ghost=nil;assert(p.pipette(prototypes.item[a.name],'normal',false),'real reference item unavailable')
  local v={position=q,direction=a.direction or 0,build_mode=defines.build_mode.forced}
  assert(p.can_build_from_cursor(v),'ghost placement blocked');p.build_from_cursor(v);p.cursor_ghost=nil
  local found=false;for _,g in pairs(p.surface.find_entities_filtered{position=q,radius=.1,type='entity-ghost'}) do if g.ghost_name==a.name then found=true end end
  assert(found,'ghost was not created');finish(p,'construction planned')
 elseif a.op=='wait_entity' then if p.surface.find_entity(a.name,pos(a.at)) then finish(p,'entity present') end
 elseif a.op=='recipe' then local e=assert(entity(p,a),'entity missing');if not p.can_reach_entity(e) then navigate(p,a,e.position,math.max(2,p.reach_distance-2));return end;assert(p.force.recipes[a.recipe] and p.force.recipes[a.recipe].enabled,'recipe locked');local old=e.get_recipe();assert(not old or old.name==a.recipe,'clear previous recipe inventory manually before changing');local removed=e.set_recipe(a.recipe);for _,item in pairs(removed) do assert(p.insert(item)==item.count,'recipe refund failed') end;finish(p,'recipe set')
 elseif a.op=='swap_equipment' then
  assert(a.inventory=='character_guns' or a.inventory=='character_ammo' or a.inventory=='character_armor','equipment inventory required');local inv=p.get_inventory((assert(defines.inventory[a.inventory])));assert(inv[a.a].swap_stack(inv[a.b]),'equipment swap failed');finish(p,'equipment slots swapped')
 elseif a.op=='select_weapon' then assert(p.character,'character required');assert(a.index>=1 and a.index<=#p.get_inventory(defines.inventory.character_guns),'invalid weapon slot');p.character.selected_gun_index=a.index;finish(p,'weapon selected')
 elseif a.op=='equip' then
  local inv=p.get_inventory((assert(defines.inventory[a.inventory],'unknown inventory')));local src=p.get_main_inventory();local n=math.min(a.count or 100,src.get_item_count(a.item));local item={name=a.item,count=n};if n>0 then item.count=src.remove(item);local accepted=inv.insert(item);if accepted<item.count then item.count=item.count-accepted;src.insert(item) end end;finish(p,'equipped')
 elseif a.op=='shoot' then p.shooting_state={state=defines.shooting.shooting_enemies,position=pos(a.at)};if game.tick-a.started>=(a.ticks or 120) then p.shooting_state={state=defines.shooting.not_shooting};finish(p,'shooting interval completed') end
 elseif a.op=='research_focus' then
  local t=assert(p.force.technologies[a.name],'unknown technology');assert(t.enabled and not t.researched,'technology unavailable');for _,pr in pairs(t.prerequisites) do assert(pr.researched,'prerequisite incomplete') end
  local old=p.force.current_research;local progress=p.force.research_progress;local q={a.name};local postponed={};for _,v in ipairs(p.force.research_queue or {}) do if v.name~=a.name then if #q<7 then q[#q+1]=v.name else postponed[#postponed+1]=v.name end end end
  p.force.research_queue=q;assert(p.force.current_research and p.force.current_research.name==a.name,'research focus rejected');finish(p,{queue=q,postponed=postponed,previous=old and old.name,previous_progress=progress,saved_progress=old and old.saved_progress})
 elseif a.op=='research' then finish(p,{accepted=p.force.add_research(a.name)})
 elseif a.op=='rotate' then local e=assert(entity(p,a),'entity missing');assert(p.can_reach_entity(e),'entity out of reach');finish(p,{rotated=e.rotate{reverse=a.reverse or false,by_player=p}})
 elseif a.op=='save' then game.auto_save(a.name or 'astra-progress');finish(p,'save requested')
 elseif a.op=='launch' then local e=assert(entity(p,a),'entity missing');assert(p.can_reach_entity(e),'entity out of reach');finish(p,{launched=e.launch_rocket()})
 else error('unknown action '..tostring(a.op)) end
end
commands.add_command('astra','Normal player actions as JSON',function(cmd)
 local command_ok,command_err=pcall(function()
 local p=game.get_player(cmd.player_index);if not p or not p.character then return end
 local s=state();local a=helpers.json_to_table(cmd.parameter or '{}');if not a then p.print('Invalid JSON');return end
 if a.op=='reload' then game.reload_mods();return
 elseif a.op=='plan' then local raw=assert(plan_store[a.name],'plan not loaded');local list=assert(helpers.json_to_table(raw),'invalid stored plan');for _,v in ipairs(list) do v._request=a._request;s.queue[#s.queue+1]=v end
 elseif a.op=='prepend' then for i=#a.actions,1,-1 do local v=a.actions[i];v._request=a._request;table.insert(s.queue,1,v) end
 elseif a.op=='stop' then s.queue={};if s.active then finish(p,'stopped') end
 elseif a.op=='observe' then observe(p,a.radius);p.print('Astra observation written');return
 elseif a.op=='placements' then
  assert(p.clear_cursor());assert(p.pipette(prototypes.item[a.name],'normal',false),'item unavailable');local ep=prototypes.entity[a.name];local out={};local origin=a.at and pos(a.at) or p.position
  for _,d in ipairs(a.directions or {0,4,8,12}) do
   local w=ep.tile_width;local h=ep.tile_height;if d==4 or d==12 then w,h=h,w end
   for x=math.floor(p.position.x-p.build_distance),math.ceil(p.position.x+p.build_distance) do for y=math.floor(p.position.y-p.build_distance),math.ceil(p.position.y+p.build_distance) do
    local q={x=x+(w%2)/2,y=y+(h%2)/2};if dist(q,p.position)<=p.build_distance and p.can_build_from_cursor{position=q,direction=d,build_mode=defines.build_mode.normal} then out[#out+1]={at=q,direction=d,distance=dist(q,origin)} end
   end end
  end
  table.sort(out,function(x,y)return x.distance<y.distance end);while #out>80 do table.remove(out) end;p.clear_cursor();helpers.write_file('astra/placements.json',helpers.table_to_json(out),false);return
 elseif a.op=='map' then
  local out={tick=game.tick,settings=p.surface.map_gen_settings,oil={},enemy_bases={}}
  for chunk in p.surface.get_chunks() do if p.force.is_chunk_charted(p.surface,chunk) then
   local area={{chunk.x*32,chunk.y*32},{(chunk.x+1)*32,(chunk.y+1)*32}}
   for _,e in pairs(p.surface.find_entities_filtered{area=area,name='crude-oil'}) do out.oil[#out.oil+1]={position=e.position,amount=e.amount} end
   for _,e in pairs(p.surface.find_entities_filtered{area=area,type='unit-spawner',force='enemy'}) do out.enemy_bases[#out.enemy_bases+1]={name=e.name,position=e.position} end
  end end
  helpers.write_file('astra/map.json',helpers.table_to_json(out),false);return
 elseif a.op=='scan' then
  local q=a.at and pos(a.at) or p.position;local result={entities={},tiles={}};for _,e in pairs(p.surface.find_entities_filtered{position=q,radius=a.radius or 20}) do if p.force.is_chunk_charted(p.surface,{math.floor(e.position.x/32),math.floor(e.position.y/32)}) then result.entities[#result.entities+1]={name=e.name,type=e.type,position=e.position,id=e.unit_number,amount=e.type=='resource' and e.amount or nil} end end
  for _,t in pairs(p.surface.find_tiles_filtered{position=q,radius=a.radius or 20}) do if p.force.is_chunk_charted(p.surface,{math.floor(t.position.x/32),math.floor(t.position.y/32)}) then result.tiles[#result.tiles+1]={name=t.name,position=t.position} end end
  helpers.write_file('astra/scan.json',helpers.table_to_json(result),false);return
 else if a.op=='batch' then for _,v in ipairs(a.actions) do s.queue[#s.queue+1]=v end else s.queue[#s.queue+1]=a end end
 s.player=p.index;observe(p);p.print('Astra queue: '..#s.queue)
 end)
 if not command_ok then local s=state();s.queue={};s.active=nil;log({event='command_error',error=tostring(command_err)});local p=game.get_player(cmd.player_index);if p then p.walking_state={walking=false};p.mining_state={mining=false};p.print('Astra command rejected: '..tostring(command_err)) end end
end)
script.on_event(defines.events.on_player_died,function(event)
 local s=state();s.queue={};s.active=nil;s.combat=nil;s.combat_entity=nil;s.retreat=nil;log({event='player_died',player_index=event.player_index});pcall(observe,game.get_player(event.player_index))
end)
script.on_event(defines.events.on_tick,function()
 local s=state();local p=s.player and game.get_player(s.player) or game.connected_players[1];if not p or not p.character then return end
 if game.tick%6==0 and (not s.active or s.active.op~='shoot') then
  local enemies=p.surface.find_entities_filtered{position=p.position,radius=24,force='enemy',type='unit'}
  local target=s.combat_entity
  if not target or not target.valid or dist(target.position,p.position)>24 then
   target=nil;local distance=25
   for _,e in pairs(enemies) do local d=dist(p.position,e.position);if d<distance then target=e;distance=d end end
  end
  s.combat_entity=target
  if target then
   local nearby_threats=0;for _,enemy in pairs(enemies) do if dist(enemy.position,p.position)<12 then nearby_threats=nearby_threats+1 end end
   if nearby_threats>=12 or p.character.health<125 or s.retreat then
    if not s.retreat then log({event='combat_retreat',enemies=#enemies});s.queue={};s.active=nil end
    local dx,dy=0,0;for _,e in pairs(enemies) do local d=dist(p.position,e.position);dx=dx+(p.position.x-e.position.x)/(d*d+1);dy=dy+(p.position.y-e.position.y)/(d*d+1) end
    local refuge=nil;local refuge_distance=301
    for _,t in pairs(p.surface.find_entities_filtered{position=p.position,radius=300,force=p.force,type='ammo-turret'}) do
     local ammo=t.get_inventory(defines.inventory.turret_ammo)
     local d=dist(t.position,p.position)
     if ammo and not ammo.is_empty() and d<refuge_distance then refuge=t;refuge_distance=d end
    end
    if refuge then dx=refuge.position.x-p.position.x;dy=refuge.position.y-p.position.y end
    if refuge and refuge_distance<7 then s.retreat=nil;p.walking_state={walking=false}
    else local ang=math.atan2(dx,-dy);s.retreat=dirs[(math.floor(ang/(math.pi/4)+0.5)%8)+1] end
   end
   local guns=p.get_inventory(defines.inventory.character_guns);local ammo=p.get_inventory(defines.inventory.character_ammo)
   if guns and ammo then for i=1,#guns do if guns[i].valid_for_read and guns[i].name=='submachine-gun' and ammo[i].valid_for_read then p.character.selected_gun_index=i;break end end end
   s.combat={name=target.name,position=target.position,enemies=#enemies,retreat=s.retreat};p.shooting_state={state=defines.shooting.shooting_enemies,position=target.position}
  else
   if s.retreat then p.walking_state={walking=false} end
   s.retreat=nil;s.combat=nil;p.shooting_state={state=defines.shooting.not_shooting}
  end
 end
 if not s.active and #s.queue>0 then s.active=table.remove(s.queue,1);s.active.started=game.tick end
 if s.active then local ok,err=pcall(step,p,s.active);if not ok then log({error=tostring(err),action=s.active});s.queue={};s.active=nil;p.walking_state={walking=false};p.mining_state={mining=false};p.repair_state={repairing=false,position=p.position};p.clear_cursor();p.print('Astra stopped: '..tostring(err)) end end
 if not s.active and not s.retreat then p.walking_state={walking=false} end
 if s.retreat then p.mining_state={mining=false};p.walking_state={walking=true,direction=s.retreat} end
 if game.tick%120==0 then local ok,err=pcall(observe,p);if not ok then helpers.write_file('astra/error.txt',tostring(err),false) end end
end)

script.on_event(defines.events.on_entity_died,function(event)
 local e=event.entity;local s=state();local p=game.get_player(s.player or 1);if p and e.valid and e.force==p.force then local loss={event="entity_lost",name=e.name,position=e.position,tick=game.tick};local c=event.cause;if c and c.valid and p.force.is_chunk_visible(c.surface,{math.floor(c.position.x/32),math.floor(c.position.y/32)}) then loss.visible_cause={name=c.name,position=c.position} end;s.losses=s.losses or {};s.losses[#s.losses+1]=loss;if #s.losses>30 then table.remove(s.losses,1) end;log(loss) end
end)
script.on_event(defines.events.on_entity_damaged,function(event)
 local e=event.entity;local s=state();local p=game.get_player(s.player or 1);if p and e.valid and e.force==p.force and event.cause and event.cause.valid and event.cause.force.name=="enemy" then s.attack_alert={name=e.name,position=e.position,tick=game.tick,health=e.health} end
end)
