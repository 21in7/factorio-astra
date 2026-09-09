from pathlib import Path
import shutil
p=Path('mods/astra-control_0.1.0/control.lua');s=p.read_text()
needle='local function step(p,a)'
nav='''local function navigate(p,a,q,radius)
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
'''
s=s.replace(needle,nav+needle)
start=s.index("  local q=pos(a.to);local dx=")
end=s.index(" elseif a.op=='mine'",start)
s=s[:start]+"  if navigate(p,a,pos(a.to),a.tolerance or 0.5) then finish(p,'arrived') end\n"+s[end:]
s=s.replace("local dx=e.position.x-p.position.x;local dy=e.position.y-p.position.y;local ang=math.atan2(dx,-dy);p.walking_state={walking=true,direction=dirs[(math.floor(ang/(math.pi/4)+0.5)%8)+1]};assert(game.tick-a.started<1800,'approach blocked');return", "navigate(p,a,e.position,2);return")
s=s.replace("local q=pos(a.at);assert(dist(q,p.position)<=p.build_distance,'build location out of reach');", "local q=pos(a.at);if dist(q,p.position)>p.build_distance then navigate(p,a,q,p.build_distance-2);return end;")
s=s.replace("elseif a.op=='put' or a.op=='take' then finish(p,{transferred=transfer(p,entity(p,a),a)})", "elseif a.op=='put' or a.op=='take' then local e=assert(entity(p,a),'entity missing');if not p.can_reach_entity(e) then navigate(p,a,e.position,math.max(2,p.reach_distance-2));return end;finish(p,{transferred=transfer(p,e,a)})")
p.write_text(s);shutil.copy2(p,Path.home()/'Library/Application Support/factorio/mods/astra-control_0.1.0/control.lua')
