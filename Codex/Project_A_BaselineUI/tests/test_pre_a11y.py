import json
from pathlib import Path
from typing import List, Dict
from playwright.sync_api import Page
from .test_common import screenshot_path, contrast_ratio, parse_color

AXE_PATH = Path(__file__).resolve().parents[1] / 'results' / 'axe_pre.json'


def run(page: Page, base_url: str, phase: str, logs: List[str], vectors: List[Dict]):
  results = []
  vector = next(v for v in vectors if v['test_id'] == 'accessibility_contrast_focus')
  page.goto(base_url, wait_until='networkidle')
  page.wait_for_selector('.task-card')

  summary_styles = page.eval_on_selector('.task-card .task-summary', 'el => { const s = getComputedStyle(el); return { color: s.color, background: s.backgroundColor }; }')
  fg = parse_color(summary_styles['color'])
  bg = parse_color(summary_styles['background'])
  ratio = contrast_ratio(fg, bg if bg != (0, 0, 0) else parse_color('rgb(255,255,255)'))

  button_selector = '.task-card .btn-primary'
  page.focus(button_selector)
  outline_value = page.eval_on_selector(button_selector, 'el => getComputedStyle(el).outline')

  keyboard_steps = int(next(step for step in vector['steps'] if step['action'] == 'keyboard')['value'])
  for _ in range(keyboard_steps):
    page.keyboard.press('Tab')
  active_selector = page.evaluate('''() => {
    const active = document.activeElement;
    if (!active) { return null; }
    return active.className || active.tagName;
  }''')

  axe_payload = page.evaluate('''() => {
    const issues = [];
    document.querySelectorAll('.task-card button').forEach((btn, idx) => {
      if (!btn.hasAttribute('aria-label')) {
        issues.push({
          id: 'missing-aria-label',
          selector: '.task-card button:nth-of-type(' + (idx + 1) + ')',
          impact: 'moderate'
        });
      }
    });
    document.querySelectorAll('.task-card .task-summary').forEach((summary, idx) => {
      const text = summary.textContent || '';
      if (text.length < 20) {
        issues.push({
          id: 'insufficient-description',
          selector: '.task-card .task-summary:nth-of-type(' + (idx + 1) + ')',
          impact: 'minor'
        });
      }
    });
    return issues;
  }''')

  AXE_PATH.parent.mkdir(parents=True, exist_ok=True)
  AXE_PATH.write_text(json.dumps({'phase': phase, 'issues': axe_payload}, indent=2), encoding='utf-8')

  expected_ratio = vector['expected']['contrast-ratio']['min']
  violation_cap = vector['expected']['axe-violations'].get('post' if phase == 'post' else 'max', 2)
  focus_required = vector['expected']['focus-outline']['required']

  status = 'passed'
  if ratio < expected_ratio or (outline_value == 'none' and focus_required):
    status = 'failed'
  if len(axe_payload) > violation_cap:
    status = 'failed'

  screenshot_name = vector['screenshot'].replace('${phase}', phase)
  page.locator('.task-card').first.screenshot(path=str(screenshot_path(screenshot_name)))

  logs.append(f"[{phase}] a11y ratio={ratio} outline={outline_value} issues={len(axe_payload)} active={active_selector}")

  results.append({
    'test_id': 'accessibility_contrast_focus',
    'status': status,
    'measurements': {
      'contrast_ratio': ratio,
      'outline': outline_value,
      'axe_issues': len(axe_payload),
      'active_after_tab': active_selector
    },
    'screenshot': screenshot_name,
    'axe_report': str(AXE_PATH.relative_to(Path(__file__).resolve().parents[1]))
  })

  return results
