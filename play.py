#!/usr/bin/env python3
import json,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
DATA=pathlib.Path.home()/'Library/Application Support/factorio'
STATE=DATA/'script-output/astra/state.json'
def read():return json.loads(STATE.read_text())
def console(a):
 for args in [('release',),('key','50'),('key','51'),('unicode','/astra '+json.dumps(a,separators=(',',':'))),('key','36'),('release',)]:
  subprocess.run([str(ROOT/'native-input'),*args],check=True,stdout=subprocess.DEVNULL)
def send(actions):
 a=actions if isinstance(actions,dict) else {'op':'batch','actions':actions}
 request=str(time.time_ns()//1000000)[-9:]
 if a.get('op')=='batch':
  for v in a['actions']:v['_request']=request
 else:a['_request']=request
 if a.get('op')=='batch' and len(json.dumps(a))>500:
  raw=json.dumps(a['actions'],separators=(',',':'))
  assert ']====]' not in raw
  lua='return {_version="'+request+'", ["'+request+'"]=[====['+raw+']====]}\n'
  for d in [ROOT/'mods/astra-control_0.1.0',DATA/'mods/astra-control_0.1.0']:(d/'plans.lua').write_text(lua)
  archive=ROOT/'plans';archive.mkdir(exist_ok=True);(archive/(request+'.json')).write_text(json.dumps(a['actions'],indent=2))
  console({'op':'reload'})
  for _ in range(50):
   if read().get('controller_plan_version')==request:break
   time.sleep(.2)
  else:raise RuntimeError('Stored plan reload was not observed')
  a={'op':'plan','name':request,'_request':request}
 console(a)
 if a.get('op') not in ['observe','scan','map','stop','reload','placements']:
  for _ in range(50):
   time.sleep(.2)
   s=read(); records=list(s.get('queue') or [])+[s.get('active') or {}]+[v.get('action',{}) for v in s.get('log',[])]
   if any(v.get('_request')==request for v in records):
    print('ack',request);return
  raise RuntimeError('No game acknowledgment: inspect console before retrying')
def brief():
 s=read();s['log']=s['log'][-5:];print(json.dumps({k:s.get(k) for k in ['tick','position','health','inventory','crafting','active','queue','log','research']},indent=2))
if __name__=='__main__':
 if len(sys.argv)==1:brief()
 elif sys.argv[1]=='send':send(json.loads(sys.argv[2]))
 elif sys.argv[1]=='file':send(json.loads(pathlib.Path(sys.argv[2]).read_text()))
 elif sys.argv[1]=='entities':print(json.dumps(read()['entities'],indent=2))
 elif sys.argv[1]=='resources':print(json.dumps(read()['resources'],indent=2))
