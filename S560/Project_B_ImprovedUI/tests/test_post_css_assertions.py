import os, subprocess, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
SERVER_SCRIPT=ROOT/'server'/'server_post.py'
RESULTS_DIR=ROOT/'results'

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

server_proc=None

def start_server():
    global server_proc
    server_proc = subprocess.Popen(['python', str(SERVER_SCRIPT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    time.sleep(0.8)


def stop_server():
    global server_proc
    if server_proc:
        server_proc.terminate(); server_proc.wait()


def get_card_props(page):
    return page.evaluate('''()=>{const el=document.querySelector('.task-card');const cs=window.getComputedStyle(el);return {paddingTop:parseFloat(cs.paddingTop),paddingLeft:parseFloat(cs.paddingLeft),fontSize:parseFloat(window.getComputedStyle(el.querySelector('.title')).fontSize),metaColor:window.getComputedStyle(el.querySelector('.meta')).color}}''')


def test_css_assertions():
    try:
        start_server()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto('http://127.0.0.1:8001/index.html')
            page.wait_for_selector('.task-card')
            props = get_card_props(page)
            res = {'spacing': props['paddingTop'], 'fontSize_title': props['fontSize'], 'meta_color': props['metaColor']}
            with open(RESULTS_DIR/'results_post_css.json','w',encoding='utf8') as fh:
                json.dump({'test_id':'spacing_hierarchy','measured':res,'min_padding_expected':16,'min_title_font':18}, fh, indent=2)
            browser.close()
    finally:
        stop_server()

if __name__=='__main__':
    test_css_assertions()
