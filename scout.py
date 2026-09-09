#!/usr/bin/env python3
"""Walk normally, monitoring the live observation for oil or danger."""
import sys,time,json
from play import read,send
x,y=map(float,sys.argv[1:3]);initial=read()
if initial.get('alive') is False:raise SystemExit('Player is dead; respawn through the game UI before scouting')
send({'op':'walk','to':[x,y]})
start=time.monotonic()
while time.monotonic()-start<45:
 s=read()
 if s.get('alive') is False:
  print(json.dumps({'reason':'player died','tick':s['tick']}));break
 oil=[r for r in s['resources'] if r['name']=='crude-oil']
 enemies=[e for e in s['entities'] if e['type'] in ['unit','unit-spawner','turret']]
 if oil or enemies or s['health']<initial['health']:
  send({'op':'stop'});print(json.dumps({'reason':'oil' if oil else 'danger','position':s['position'],'health':s['health'],'oil':oil,'enemies':[{'name':e['name'],'position':e['position']} for e in enemies]}));break
 if not s.get('active') and not s.get('queue'):
  print(json.dumps({'reason':'walk finished','tick':s['tick'],'position':s['position'],'health':s['health'],'last':s['log'][-1].get('error') or s['log'][-1].get('result')}));break
 time.sleep(1)
else:print(json.dumps({'reason':'still walking','tick':s['tick'],'position':s['position'],'health':s['health']}))
