#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECTS=("Project_A_BaselineUI" "Project_B_ImprovedUI")

for project in "${PROJECTS[@]}"; do
  echo "Running $project tests"
  (cd "$ROOT_DIR/$project" && bash ./run_tests.sh)
done

mkdir -p "$ROOT_DIR/results"
cp "$ROOT_DIR/Project_A_BaselineUI/results/results_pre.json" "$ROOT_DIR/results/results_pre.json"
cp "$ROOT_DIR/Project_B_ImprovedUI/results/results_post.json" "$ROOT_DIR/results/results_post.json"

PY_BIN="$ROOT_DIR/Project_B_ImprovedUI/.venv/bin/python"
if [ ! -x "$PY_BIN" ]; then
  PY_BIN="$ROOT_DIR/Project_B_ImprovedUI/.venv/Scripts/python"
fi

export HARNESS_ROOT="$ROOT_DIR"

"$PY_BIN" - <<'PY'
import json
import os
from pathlib import Path
from PIL import Image, ImageChops

root = Path(os.environ.get('HARNESS_ROOT', Path.cwd()))
with open(root / 'results' / 'results_pre.json', 'r', encoding='utf-8') as handle:
  pre = json.load(handle)
with open(root / 'results' / 'results_post.json', 'r', encoding='utf-8') as handle:
  post = json.load(handle)

comparisons = []
post_lookup = {t['test_id']: t for t in post['tests']}
for test in pre['tests']:
  post_test = post_lookup.get(test['test_id'])
  delta = {
    'test_id': test['test_id'],
    'pre_status': test['status'],
    'post_status': post_test['status'] if post_test else 'missing',
    'notes': ''
  }
  if 'measurements' in test and post_test and 'measurements' in post_test:
    delta['measurements'] = {}
    for key, value in post_test['measurements'].items():
      pre_value = test['measurements'].get(key)
      if isinstance(value, (int, float)) and isinstance(pre_value, (int, float)):
        delta['measurements'][key] = round(value - pre_value, 2)
  comparisons.append(delta)

aggregate = {
  'generated_by': 'run_all.sh',
  'summary': {
    'pre_pass': sum(1 for t in pre['tests'] if t['status'] == 'passed'),
    'post_pass': sum(1 for t in post['tests'] if t['status'] == 'passed')
  },
  'comparisons': comparisons
}

with open(root / 'results' / 'aggregate_results.json', 'w', encoding='utf-8') as handle:
  json.dump(aggregate, handle, indent=2)

pre_img = Image.open(root / 'Project_A_BaselineUI' / 'screenshots' / 'screenshot_pre_ui.png').convert('RGB')
post_img = Image.open(root / 'Project_B_ImprovedUI' / 'screenshots' / 'screenshot_post_ui.png').convert('RGB')
if pre_img.size != post_img.size:
  post_img = post_img.resize(pre_img.size)

diff = ImageChops.difference(pre_img, post_img)
diff_path = root / 'results' / 'screenshot_diff_ui.png'
diff.save(diff_path)

report_lines = []
report_lines.append('# Task List Visual Redesign Comparison')
report_lines.append('')
report_lines.append('![Baseline](Project_A_BaselineUI/screenshots/screenshot_pre_ui.png)')
report_lines.append('![Improved](Project_B_ImprovedUI/screenshots/screenshot_post_ui.png)')
report_lines.append('![Diff](results/screenshot_diff_ui.png)')
report_lines.append('\n## Test Outcomes')
for entry in comparisons:
  measurements = entry.get('measurements')
  metric_text = ''
  if measurements:
    metric_pairs = [f"{k}: {v:+}" for k, v in measurements.items()]
    metric_text = ' | Δ ' + ', '.join(metric_pairs)
  report_lines.append(f"- **{entry['test_id']}** pre={entry['pre_status']} post={entry['post_status']}{metric_text}")

summary_text = (
  f"Pre passes: {aggregate['summary']['pre_pass']} / {len(pre['tests'])}, "
  f"Post passes: {aggregate['summary']['post_pass']} / {len(post['tests'])}"
)
report_lines.append('\n' + summary_text)
report_lines.append('\n### Recommendations')
report_lines.append('- Roll out via feature flag, monitor scan time telemetry, schedule dedicated accessibility audit.')

(Path(root) / 'compare_report.md').write_text('\n'.join(report_lines), encoding='utf-8')
PY
