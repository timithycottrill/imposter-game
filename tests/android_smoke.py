"""Install the real APK and play three rounds offline using Android touch events."""
import json, re, subprocess, time, xml.etree.ElementTree as ET
from pathlib import Path
ART=Path('artifacts');ART.mkdir(exist_ok=True)
def adb(*args):
 return subprocess.check_output(['adb',*args],timeout=40)
def nodes():
 for attempt in range(4):
  try:
   adb('shell','uiautomator','dump','/sdcard/imposter-window.xml')
   return list(ET.fromstring(adb('shell','cat','/sdcard/imposter-window.xml')).iter('node'))
  except Exception:
   if attempt==3:raise
   time.sleep(1)
def texts(ns):return {n.get('text','') for n in ns}|{n.get('content-desc','') for n in ns}
def tap(text):
 ns=nodes()
 for n in ns:
  if text in [n.get('text'),n.get('content-desc')]:
   x1,y1,x2,y2=map(int,re.findall(r'\d+',n.get('bounds','')))
   adb('shell','input','tap',str((x1+x2)//2),str((y1+y2)//2));time.sleep(.4);return
 raise AssertionError(f'Control missing: {text}; visible: {texts(ns)}')
def screen(text):
 ns=nodes();assert text in texts(ns),(text,texts(ns));return ns
words={line.split('|')[0].upper() for line in Path('src/words.ts').read_text().splitlines() if '|' in line and not line.startswith('//')}
adb('install','-r','android/app/build/outputs/apk/debug/app-debug.apk')
adb('shell','svc','wifi','disable');adb('shell','svc','data','disable')
adb('shell','am','force-stop','com.imposter.game')
adb('shell','am','start','-n','com.imposter.game/.MainActivity')
for attempt in range(20):
 if 'START ROUND' in texts(nodes()):break
 time.sleep(1)
else:raise AssertionError('APK failed to launch offline')
screen('START ROUND')
(ART/'android-setup.png').write_bytes(adb('exec-out','screencap','-p'))
tap('Increase number of players');screen('5')
tap('Decrease number of players');screen('4')
last=None
for r in range(3):
 tap('START ROUND' if r==0 else 'NEW ROUND')
 roles=[];imposters=[]
 for player in range(1,5):
  ns=screen(f'PLAYER {player}');visible=texts(ns)
  assert not visible.intersection(words),visible
  assert 'ONE-WORD HINT' not in visible
  tap('REVEAL');visible=texts(screen(f'PLAYER {player}'))
  assert 'ONE-WORD HINT' not in visible
  if 'You do not know the secret word.' in visible:
   imposters.append(player);assert not visible.intersection(words);assert 'SECRET WORD' not in visible
  else:
   values=visible.intersection(words);assert len(values)==1,visible;roles.extend(values)
  tap('FIND THE IMPOSTER' if player==4 else 'HIDE & NEXT PLAYER')
 assert len(imposters)==1;assert len(roles)==3;assert len(set(roles))==1
 visible=texts(screen('ONE-WORD HINT'));assert roles[0] not in visible
 tap('REVEAL ANSWER');visible=texts(screen('THE IMPOSTER'))
 assert roles[0] in visible;assert f'PLAYER {imposters[0]}' in visible
 assert roles[0]!=last;last=roles[0]
tap('Change player count');screen('4')
adb('shell','am','force-stop','com.imposter.game');adb('shell','am','start','-n','com.imposter.game/.MainActivity');time.sleep(2)
screen('START ROUND');screen('4')
result={'offline_first_launch':True,'native_touch_rounds':3,'count_controls':True,'private_roles_and_answers':True,'new_round':True,'reload_and_count_persistence':True,'platform':'Android 35 emulator','physical_samsung_tested':False}
(ART/'android-results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
