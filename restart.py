#!/usr/bin/env python3
import pathlib,subprocess,time,shutil
root=pathlib.Path(__file__).resolve().parent
base=pathlib.Path.home()/'Library/Application Support/factorio'
subprocess.run(['osascript','-e','tell application "Factorio" to quit'],check=True)
for _ in range(30):
 if subprocess.run(['pgrep','-f','Contents/MacOS/factorio'],stdout=subprocess.DEVNULL).returncode:break
 time.sleep(.2)
shutil.copy2(root/'mods/astra-control_0.1.0/control.lua',base/'mods/astra-control_0.1.0/control.lua')
subprocess.run(['open','-a',str(pathlib.Path.home()/'Library/Application Support/Steam/steamapps/common/Factorio/factorio.app'),'--args','--load-game',str(base/'saves/_autosave-astra-progress.zip')],check=True)
