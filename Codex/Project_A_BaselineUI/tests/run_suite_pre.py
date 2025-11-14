import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from . import test_pre_visual, test_pre_css_assertions, test_pre_a11y
from .test_common import load_vectors, write_results, write_logs


def main():
  base_url = os.environ.get('BASELINE_URL', 'http://127.0.0.1:5001')
  vectors = load_vectors()
  logs = []
  aggregate_results = []
  timestamp = datetime.utcnow().isoformat() + 'Z'

  with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    for module in (test_pre_visual, test_pre_css_assertions, test_pre_a11y):
      aggregate_results.extend(module.run(page, base_url, 'pre', logs, vectors))
    browser.close()

  payload = {
    'phase': 'pre',
    'timestamp': timestamp,
    'url': base_url,
    'tests': aggregate_results
  }
  write_results(payload)
  write_logs(logs)


if __name__ == '__main__':
  main()
