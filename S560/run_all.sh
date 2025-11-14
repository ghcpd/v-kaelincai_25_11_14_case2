#!/usr/bin/env bash
set -e
ROOT_DIR=$(pwd)

# Run setup
./setup.sh

# Run baseline
pushd Project_A_BaselineUI
./run_tests.sh
popd

# Run improved
pushd Project_B_ImprovedUI
./run_tests.sh
popd

# Generate diffs and aggregate results
python generate_diffs.py

python - <<'PY'
import json, os, base64
from pathlib import Path
root = Path('.').resolve()
pre = json.loads((root/'Project_A_BaselineUI'/'results'/'results_pre.json').read_text())
post = json.loads((root/'Project_B_ImprovedUI'/'results'/'results_post.json').read_text())
report = root/'compare_report.md'
pre_img = lambda name: root/'Project_A_BaselineUI'/'screenshots'/name
post_img = lambda name: root/'Project_B_ImprovedUI'/'screenshots'/name

def img_tag(path):
    if not Path(path).exists():
        return ''
    rel = os.path.relpath(path, root)
    return f"![{os.path.basename(path)}]({rel})"

with report.open('w', encoding='utf-8') as f:
    f.write('# Compare Report\n\n')
    f.write('## Summary\n')
    f.write('Baseline vs Improved visual & accessibility results.\n\n')
    f.write('## Tests\n')
    for p in pre['checks']:
        tid = p['test_id']
        f.write(f"### {tid}\n")
        f.write(f"- Baseline: {p['outcome']} - {img_tag(pre_img(p['screenshot']))}\n")
        post_match = next((x for x in post['checks'] if x['test_id']==tid), {})
        f.write(f"- Improved: {post_match.get('outcome','MISSING')} - {img_tag(post_img(post_match.get('screenshot','')))}\n")
        # compute CSS deltas if measured
        if p.get('measured') and post_match.get('measured'):
            try:
                before = p['measured']
                after = post_match['measured']
                deltas = {k: (after[k]-before[k]) for k in before if isinstance(before[k], (int,float)) and k in after}
                f.write(f"- CSS deltas: {deltas}\n")
            except Exception as e:
                pass
        # Accessibility violations comparison
        if 'violationsCount' in p or 'violationsCount' in post_match:
            f.write(f"- Violations: baseline={p.get('violationsCount',0)} improved={post_match.get('violationsCount',0)}\n")
        diffname = 'diff_' + p['screenshot'].replace('screenshot_pre_','') if p.get('screenshot') else ''
        if diffname:
            diffpath = root/'results'/'diffs'/diffname
            if diffpath.exists():
                f.write(f"- Visual diff: {img_tag(diffpath)}\n")
        f.write('\n')

    f.write('## Accessibility Summary\n')
    f.write('- Baseline issues and improved fixes where applicable.\n')

print('Compare report generated at', report)
PY

echo 'Done'
