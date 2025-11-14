import os, json
from PIL import Image, ImageChops

BASE = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'Project_A_BaselineUI')
IMPR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'Project_B_ImprovedUI')
OUT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'results')

os.makedirs(OUT, exist_ok=True)

results_pre = os.path.join(BASE, 'results', 'results_pre.json')
results_post = os.path.join(IMPR, 'results', 'results_post.json')

with open(results_pre) as f: pre = json.load(f)
with open(results_post) as f: post = json.load(f)

report_md = os.path.join(OUT, 'compare_report.md')

lines = [
"# Compare Report\n",
"## Executive Summary\n",
"This report compares the baseline dense UI with the improved UI. It summarizes per-test pass/fail and visual diffs.\n",
"---\n",
]

# embed top-level screenshots
pre_ss = os.path.join(BASE, 'screenshots', 'screenshot_pre_ui.png')
post_ss = os.path.join(IMPR, 'screenshots', 'screenshot_post_ui.png')
if os.path.exists(pre_ss) and os.path.exists(post_ss):
    diff_out = os.path.join(OUT, 'screenshot_diff_ui.png')
    a = Image.open(pre_ss).convert('RGBA')
    b = Image.open(post_ss).convert('RGBA')
    if a.size != b.size:
        a = a.resize(b.size)
    diff = ImageChops.difference(a,b)
    diff.save(diff_out)
    lines.append('### Before / After UI\n')
    lines.append(f'![pre]({pre_ss})  ![post]({post_ss})  ![diff]({diff_out})\n')

lines.append('---\n')
lines.append('## Per-test Comparison\n')

# assume matching order
for p, q in zip(pre, post):
    tid = p['test_id']
    lines.append(f"### Test: {tid}\n")
    lines.append(f"- Baseline: {'PASS' if p.get('pass') else 'FAIL'}\n")
    lines.append(f"- Improved: {'PASS' if q.get('pass') else 'FAIL'}\n")
    if p.get('screenshot') and q.get('screenshot'):
        preimg = p['screenshot']
        postimg = q['screenshot']
        diffimg = os.path.join(OUT, f"diff_{tid}.png")
        try:
            a = Image.open(preimg).convert('RGBA')
            b = Image.open(postimg).convert('RGBA')
            if a.size != b.size:
                a = a.resize(b.size)
            diff = ImageChops.difference(a,b)
            diff.save(diffimg)
            total = b.size[0]*b.size[1]
            nonzero = sum(1 for px in diff.getdata() if px!=(0,0,0,0))
            pct = round(nonzero/total*100,2) if total else 0.0
            lines.append(f"- Visual diff: {pct}% different. Diff saved: {diffimg}\n")
        except Exception as e:
            lines.append(f"- Visual diff computation failed: {e}\n")
    # include observations
    lines.append(f"- Baseline observations: {json.dumps(p.get('observations',{}),indent=0)}\n")
    lines.append(f"- Improved observations: {json.dumps(q.get('observations',{}),indent=0)}\n")
    lines.append('\n')

# a11y summary
lines.append('---\n')
lines.append('## Accessibility summary\n')

a11y_pre = [r for r in pre if r['test_id'].startswith('accessibility') or r['test_id']=='accessibility_contrast']
a11y_post = [r for r in post if r['test_id'].startswith('accessibility') or r['test_id']=='accessibility_contrast']
if a11y_pre and a11y_post:
    lines.append('- Baseline contrast: '+str(a11y_pre[0]['observations'].get('contrast'))+'\n')
    lines.append('- Improved contrast: '+str(a11y_post[0]['observations'].get('contrast'))+'\n')

with open(report_md,'w',encoding='utf-8') as f:
    f.writelines(lines)

print('generate_report complete. Report at', report_md)
