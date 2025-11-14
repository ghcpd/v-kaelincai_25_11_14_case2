import os, subprocess, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[2]
SERVER_SCRIPT=ROOT/'server'/'server_pre.py'
SCREENSHOT_DIR=ROOT/'screenshots'
RESULTS_DIR=ROOT/'results'
LOG_DIR=ROOT/'logs'

SIGNALS={'port':8000, 'host':'127.0.0.1'}

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

server_proc=None


def start_server():
    global server_proc
    server_proc = subprocess.Popen(['python', str(SERVER_SCRIPT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    # wait for server to start
    time.sleep(1)


def stop_server():
    global server_proc
    if server_proc:
        server_proc.terminate(); server_proc.wait()


def get_page_styles(page, selector):
    return page.evaluate('''(sel)=>{const el=document.querySelector(sel);const cs=window.getComputedStyle(el);return {paddingTop:parseFloat(cs.paddingTop),paddingBottom:parseFloat(cs.paddingBottom),paddingLeft:parseFloat(cs.paddingLeft),paddingRight:parseFloat(cs.paddingRight),fontSize:parseFloat(cs.fontSize),color:cs.color,background:cs.backgroundColor,boxShadow:cs.boxShadow}}''', selector)


def test_full_render_and_css():
    try:
        start_server()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            url = f"http://{SIGNALS['host']}:{SIGNALS['port']}/index.html"
            page.goto(url)
            page.wait_for_selector('.task-card')
            page.screenshot(path=str(SCREENSHOT_DIR/'screenshot_pre_ui.png'), full_page=True)
            # capture per-test
            # spacing/hierarchy check
            styles = get_page_styles(page, '.task-card')
            page.screenshot(path=str(SCREENSHOT_DIR/'screenshot_pre_spacing_hierarchy.png'))

            # button consistency and hover
            primary = page.query_selector('.task-card .btn-primary')
            box_before = primary.bounding_box()
            pre_bg = page.evaluate("sel=>window.getComputedStyle(document.querySelector(sel)).backgroundColor", '.task-card .btn-primary')
            page.hover('.task-card .btn-primary')
            time.sleep(0.3)
            hover_box = page.evaluate("sel=>window.getComputedStyle(document.querySelector(sel)).boxShadow", '.task-card .btn-primary')
            page.screenshot(path=str(SCREENSHOT_DIR/'screenshot_pre_button_hover.png'))

            # icon size
            icon_style = get_page_styles(page, '.task-card .icon')
            page.screenshot(path=str(SCREENSHOT_DIR/'screenshot_pre_icon_consistency.png'))

            # accessibility checks: inject axe-core
            axe_js_url='https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.6.3/axe.min.js'
            page.add_script_tag(url=axe_js_url)
            results = page.evaluate('''async ()=>{return await axe.run(document,{ runOnly: {type: 'tag', values: ['wcag2aa']}})}''')
            with open(RESULTS_DIR/'results_pre.json','w',encoding='utf8') as fh:
                json.dump({'checks':[{'test_id':'baseline_render','outcome':'pass','screenshot':'screenshot_pre_ui.png'},{'test_id':'spacing_hierarchy','outcome':'warn','screenshot':'screenshot_pre_spacing_hierarchy.png','measured':styles},{'test_id':'button_consistency','outcome':'warn','screenshot':'screenshot_pre_button_hover.png','bg':pre_bg,'hover_box':hover_box},{'test_id':'icon_consistency','outcome':'warn','screenshot':'screenshot_pre_icon_consistency.png','measured_icon':icon_style},{'test_id':'accessibility_checks','outcome':('fail' if results['violations'] else 'pass'),'violationsCount':len(results['violations'])}]}, fh, indent=2)
            browser.close()
    finally:
        stop_server()

if __name__=='__main__':
    test_full_render_and_css()

