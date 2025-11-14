import json
import os
import time
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(ROOT, 'data', 'test_data.json')
RESULTS_FILE = os.path.join(ROOT, 'results', 'results_pre.json')
LOG_FILE = os.path.join(ROOT, 'logs', 'log_pre.txt')
SCREENSHOT_DIR = os.path.join(ROOT, 'screenshots')


def log(msg):
    print(msg)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(msg + '\n')


def measure_css(page, selector, properties):
    script = '''(selector, props) => {
        const el = document.querySelector(selector);
        if(!el) return null;
        const cs = window.getComputedStyle(el);
        const out = {};
        for(const p of props) out[p] = cs.getPropertyValue(p);
        const rect = el.getBoundingClientRect();
        out['rect'] = {width: rect.width, height: rect.height, top: rect.top, left: rect.left};
        return out;
    }'''
    return page.evaluate(script, selector, properties)


def compute_contrast(fg_hex, bg_hex):
    def hex_to_rgb(hexc):
        hexc = hexc.strip()
        if hexc.startswith('#'): hexc = hexc[1:]
        if len(hexc) == 3:
            hexc = ''.join([c*2 for c in hexc])
        r = int(hexc[0:2],16)
        g = int(hexc[2:4],16)
        b = int(hexc[4:6],16)
        return [r/255.0,g/255.0,b/255.0]
    def lum(rgb):
        r,g,b = rgb
        def f(c):
            return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
        R,G,B = f(r), f(g), f(b)
        return 0.2126*R + 0.7152*G + 0.0722*B
    L1 = lum(hex_to_rgb(fg_hex))
    L2 = lum(hex_to_rgb(bg_hex))
    brighter = max(L1,L2); darker = min(L1,L2)
    return (brighter+0.05)/(darker+0.05)


def diff_images(img1_path, img2_path, out_path):
    a = Image.open(img1_path).convert('RGBA')
    b = Image.open(img2_path).convert('RGBA')
    if a.size != b.size:
        a = a.resize(b.size)
    diff = ImageChops.difference(a,b)
    bbox = diff.getbbox()
    diff.save(out_path)
    # compute percent diff
    total_pixels = b.size[0]*b.size[1]
    nonzero = 0
    for px in diff.getdata():
        if px != (0,0,0,0): nonzero +=1
    return nonzero/total_pixels if total_pixels else 0.0


def run_tests():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    with open(DATA_FILE,'r',encoding='utf-8') as f:
        tests = json.load(f)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width':1200,'height':900})
        console_messages = []
        page.on('console', lambda msg: console_messages.append({'type':msg.type, 'text':msg.text()}))
        for t in tests:
            tid = t['test_id']
            log(f"Running {tid}")
            page.goto(t['url'])
            log('Console messages so far: ' + str(console_messages))
            time.sleep(0.5)
            entry = {'test_id':tid,'pass':False,'observations':{},'screenshot':None}
            if t.get('steps'):
                for step in t['steps']:
                    if step['action']=='hover':
                        sel=step['selector']; page.hover(sel); time.sleep(0.2)
                    if step['action']=='open':
                        pass
                    if step['action']=='query':
                        pass
            # screenshot
            ss_path = os.path.join(SCREENSHOT_DIR,t.get('screenshot','screenshot_'+tid+'.png'))
            page.screenshot(path=ss_path, full_page=True)
            entry['screenshot'] = ss_path
            entry['console_logs'] = console_messages.copy()
            # sample checks
            if tid=='card_spacing':
                props = measure_css(page,t['selector'],['padding-left','padding-right','padding-top','padding-bottom','font-size'])
                entry['observations'].update(props or {})
                # convert to ints
                def px_to_int(v):
                    try: return int(float(v.replace('px','')))
                    except: return 0
                paddings = [px_to_int(props.get('padding-left','0')),
                            px_to_int(props.get('padding-right','0')),
                            px_to_int(props.get('padding-top','0')),
                            px_to_int(props.get('padding-bottom','0'))]
                fontsize = px_to_int(props.get('font-size','0'))
                entry['pass'] = all(p>=16 for p in paddings) and fontsize>=16
            elif tid=='button_consistency':
                # check primary button style and hover
                btns = page.query_selector_all(t['selector'])
                if btns:
                    colors = set()
                    for b in btns:
                        cs = page.evaluate('el => window.getComputedStyle(el).getPropertyValue("background-color")', b)
                        colors.add(cs)
                    # hover first
                    first = page.query_selector(t['selector'])
                    if first:
                        page.hover(t['selector'])
                        time.sleep(0.2)
                        bs = page.evaluate('el => window.getComputedStyle(el).getPropertyValue("box-shadow")', first)
                    entry['observations']['bg_colors']=list(colors)
                    entry['observations']['hover_box_shadow']=bs
                    entry['pass'] = len(colors)==1 and 'rgba' in list(colors)[0]
            elif tid=='iconography_alignment':
                # check icon dimensions
                icons = page.query_selector_all(t['selector'])
                dims = []
                for i in icons:
                    rect = page.evaluate('el=>el.getBoundingClientRect()', i)
                    dims.append({'w':rect['width'],'h':rect['height'],'top':rect['top']})
                entry['observations']['dims']=dims
                if dims:
                    uniform = all(abs(d['w']-dims[0]['w'])<2 and abs(d['h']-dims[0]['h'])<2 for d in dims)
                    aligned = all(abs(d['top']-dims[0]['top'])<3 for d in dims)
                    entry['pass'] = uniform and aligned
            elif tid=='accessibility_contrast':
                # compute contrast of body text
                body = page.query_selector('body')
                fg = page.evaluate('el => window.getComputedStyle(el).getPropertyValue("color")', body)
                bg = page.evaluate('el => window.getComputedStyle(el).getPropertyValue("background-color")', body)
                # convert rgb(a) to hex
                def rgb_to_hex(rgb):
                    if rgb.startswith('rgb'):
                        nums = [int(n) for n in rgb.replace('rgba(','').replace('rgb(','').replace(')','').split(',')[:3]]
                        return '#%02x%02x%02x' % tuple(nums)
                    return '#000000'
                fghex = rgb_to_hex(fg)
                bghex = rgb_to_hex(bg)
                contrast = compute_contrast(fghex,bghex)
                entry['observations']['fg']=fg; entry['observations']['bg']=bg; entry['observations']['contrast']=contrast
                # focus check: focus on first button
                firstbtn = page.query_selector('.btn')
                if firstbtn:
                    firstbtn.focus(); time.sleep(0.1)
                    outline = page.evaluate('el => window.getComputedStyle(el).getPropertyValue("outline")', firstbtn)
                    entry['observations']['focus_outline']=outline
                    entry['pass'] = contrast>=4.5 and 'none' not in outline
            else:
                # baseline visual always passes load
                entry['pass'] = True
            results.append(entry)
        browser.close()
    with open(RESULTS_FILE,'w',encoding='utf-8') as f:
        json.dump(results,f,indent=2)

if __name__=='__main__':
    run_tests()
