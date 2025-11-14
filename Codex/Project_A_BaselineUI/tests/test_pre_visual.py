from typing import List, Dict
from playwright.sync_api import Page
from .test_common import screenshot_path


def run(page: Page, base_url: str, phase: str, logs: List[str], vectors: List[Dict]):
  results = []
  visual_vector = next(v for v in vectors if v['test_id'] == 'baseline_visual')
  page.goto(base_url, wait_until='networkidle')
  page.wait_for_timeout(500)
  page.wait_for_selector('#task-board')
  screenshot_name = visual_vector['expected']['screenshot'].replace('${phase}', phase)
  path = screenshot_path(screenshot_name)
  page.screenshot(path=str(path), full_page=True)
  results.append({
    'test_id': 'baseline_visual',
    'status': 'passed',
    'details': {
      'screenshot': screenshot_name,
      'rule': visual_vector['expected'].get('rule', 'exact')
    }
  })
  logs.append(f"Captured {phase} UI screenshot at {path}")
  return results
