import os, subprocess, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
SERVER_SCRIPT=ROOT/'server'/'server_pre.py'
RESULTS_DIR=ROOT/'results'

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

server_proc=None


def start_server():
    global server_proc
    server_proc = subprocess.Popen(['python', str(SERVER_SCRIPT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    time.sleep(0.6)


def stop_server():
    global server_proc
    if server_proc:
        server_proc.terminate(); server_proc.wait()


def test_a11y_checks():
    try:
        start_server()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('http://127.0.0.1:8000/index.html')
            page.wait_for_selector('.task-card')
            axe_js_url='https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.6.3/axe.min.js'
            page.add_script_tag(url=axe_js_url)
            results = page.evaluate('''async ()=>{return await axe.run(document,{runOnly:{type:'tag',values:['wcag2aa']}})}''')
            # Check focus - keyboard order by pressing Tab several times and capturing active element
            keys = []
            for i in range(6):
                page.keyboard.press('Tab')
                active = page.evaluate('()=>document.activeElement && document.activeElement.outerHTML')
                keys.append(active)
            with open(RESULTS_DIR/'results_pre_a11y.json','w',encoding='utf8') as fh:
                json.dump({'test_id':'accessibility_checks','violationsCount':len(results['violations']),'active_sequence':keys}, fh, indent=2)
            browser.close()
    finally:
        stop_server()

if __name__=='__main__':
    test_a11y_checks()
