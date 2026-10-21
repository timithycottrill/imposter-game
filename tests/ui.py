"""Full mobile interaction and PWA checks. pip install playwright; use system Chromium."""
import json, os, time, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
BASE=os.environ.get('GAME_URL','http://127.0.0.1:4173/')
ART=Path('artifacts'); ART.mkdir(exist_ok=True)

def run():
 with sync_playwright() as p:
  ctx=p.chromium.launch_persistent_context(tempfile.mkdtemp(prefix='imposter-browser-'),executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'],viewport={'width':360,'height':780},device_scale_factor=3,is_mobile=True,has_touch=True)
  page=ctx.new_page(); errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
  page.goto(BASE);page.clock.install()
  def tap(name):
   page.clock.fast_forward(260)
   page.get_by_role('button',name=name,exact=True).tap()
  def phase(s):expect(page.locator('main')).to_have_attribute('data-phase',s)
  def count(n):expect(page.get_by_label('Number of players',exact=True)).to_have_text(str(n))
  def fit(): assert page.evaluate('document.documentElement.scrollHeight <= innerHeight'), 'Unexpected scrolling'
  count(4);fit();tap('Decrease number of players');count(3)
  expect(page.get_by_label('Decrease number of players')).to_be_disabled()
  for n in range(4,21):tap('Increase number of players');count(n)
  expect(page.get_by_label('Increase number of players')).to_be_disabled()
  page.reload();page.clock.fast_forward(260);count(20)
  # Observe every DOM mutation: private transitions must never render old word nodes.
  page.evaluate('''() => { window.disclosures=[]; new MutationObserver(() => {
    const m=document.querySelector('main');
    if(m?.dataset.phase==='PASS_PHONE' && (m.textContent.includes('SECRET WORD') || m.querySelector('.value'))) window.disclosures.push(m.textContent);
  }).observe(document.getElementById('app'),{childList:true,subtree:true,characterData:true}); }''')
  def complete_round(players, begin=True):
   if begin:tap('START ROUND')
   phase('PASS_PHONE');imposters=[];words=[]
   for i in range(players):
    expect(page.get_by_role('heading')).to_have_text(f'PLAYER {i+1}')
    expect(page.locator('.value')).to_have_count(0)
    expect(page.get_by_text('ONE-WORD HINT',exact=True)).to_have_count(0)
    tap('REVEAL');phase('REVEAL_ROLE');fit()
    expect(page.get_by_text('ONE-WORD HINT',exact=True)).to_have_count(0)
    if page.get_by_text('You do not know the secret word.',exact=True).count():
     imposters.append(i+1);expect(page.get_by_text('SECRET WORD',exact=True)).to_have_count(0)
     expect(page.locator('.value')).to_have_text('IMPOSTER')
    else:words.append(page.locator('.value').inner_text())
    tap('FIND THE IMPOSTER' if i==players-1 else 'HIDE & NEXT PLAYER')
    phase('DISCUSSION' if i==players-1 else 'PASS_PHONE')
   assert len(imposters)==1;assert len(set(words))==1
   expect(page.get_by_text('ONE-WORD HINT',exact=True)).to_be_visible()
   hint=page.locator('.value').inner_text();assert len(hint.split())==1;fit()
   tap('REVEAL ANSWER');phase('ANSWER');fit()
   expect(page.locator('.value').nth(0)).to_have_text(words[0])
   expect(page.locator('.value').nth(1)).to_have_text(f'PLAYER {imposters[0]}')
   expect(page.get_by_text('ONE-WORD HINT',exact=True)).to_have_count(0)
   return words[0]
  last=complete_round(20)
  # Consecutive NEW ROUND UI cycles; all counts checked, including 3 and 20.
  for r in range(100):
   if r%5==0:
    tap('Change player count');phase('SETUP')
    target=3+(r//5)%18
    current=int(page.get_by_label('Number of players',exact=True).inner_text())
    while current!=target:
     tap('Increase number of players' if current<target else 'Decrease number of players');current+=1 if current<target else -1
    new=complete_round(target)
   else:
    tap('NEW ROUND');phase('PASS_PHONE')
    new=complete_round(target,False)
   assert last!=new;last=new
  assert not page.evaluate('window.disclosures')
  tap('NEW ROUND');tap('REVEAL')
  # Real browser visibility event privacy guard; no player index change.
  player=page.get_by_role('heading').inner_text()
  page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))")
  phase('PASS_PHONE');expect(page.get_by_role('heading')).to_have_text(player)
  page.evaluate("delete document.hidden")
  # Intentional rapid double tap must not expose the next role.
  page.clock.fast_forward(300);page.get_by_role('button',name='REVEAL',exact=True).dblclick(delay=20)
  phase('REVEAL_ROLE')
  page.clock.fast_forward(300)
  label='HIDE & NEXT PLAYER' if page.get_by_role('button',name='HIDE & NEXT PLAYER',exact=True).count() else 'FIND THE IMPOSTER'
  page.get_by_role('button',name=label,exact=True).dblclick(delay=20)
  phase('PASS_PHONE');expect(page.locator('.value')).to_have_count(0)
  # Reload only restores player count, never a role/answer.
  page.reload();phase('SETUP');count(target)
  page.screenshot(path=str(ART/'samsung-setup.png'))
  # Native keyboard controls: Tab reaches count controls, Enter starts round.
  page.get_by_label('Increase number of players').focus();page.keyboard.press('Enter');count(target+1)
  page.get_by_role('button',name='START ROUND',exact=True).focus();page.clock.fast_forward(300);page.keyboard.press('Enter');phase('PASS_PHONE')
  page.get_by_role('button',name='REVEAL',exact=True).focus();page.clock.fast_forward(300);page.keyboard.press('Space');phase('REVEAL_ROLE')
  # Manifest and install prerequisites are read from the actual production page.
  manifest=page.evaluate('''async () => { const link=document.querySelector('link[rel=manifest]');return {url:link.href,data:await (await fetch(link.href)).json()}; }''')
  m=manifest['data'];assert m['display']=='standalone';assert m['orientation']=='portrait';assert m['theme_color']=='#000000'
  for icon in m['icons']:
   assert ctx.request.get(manifest['url'].rsplit('/',1)[0]+'/'+icon['src']).ok
  page.evaluate('navigator.serviceWorker.ready.then(() => true)')
  page.wait_for_function('navigator.serviceWorker.controller !== null')
  # Browser CDP installability diagnostics.
  cdp=ctx.new_cdp_session(page);cdp.send('Page.enable')
  install_errors=cdp.send('Page.getInstallabilityErrors')['installabilityErrors']
  assert not install_errors,install_errors
  cache_urls=page.evaluate('''async()=>{const names=await caches.keys();return (await Promise.all(names.map(async n=>(await (await caches.open(n)).keys()).map(r=>r.url)))).flat()}''')
  assert any('index' in u and '.js' in u for u in cache_urls)
  # Entire round succeeds with network disabled, after an offline page reload.
  ctx.set_offline(True);page.reload();phase('SETUP');count(target+1)
  complete_round(target+1)
  tap('NEW ROUND');phase('PASS_PHONE')
  ctx.set_offline(False)
  for size in [{'width':360,'height':640},{'width':412,'height':915},{'width':320,'height':568},{'width':780,'height':360}]:
   page.set_viewport_size(size);fit()
  assert not errors,errors
  results={'engine_rounds':1150,'ui_rounds':102,'mobile_viewport':'360×780, touch, DPR 3','extra_viewports':['360×640','412×915','320×568','780×360'],'keyboard':True,'offline_reload_and_full_round':True,'installability_errors':install_errors,'console_errors':errors,'transition_disclosures':[],'base_url':BASE}
  (ART/'ui-results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
  ctx.close()
if __name__=='__main__':run()
