import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from . import test_post_visual, test_post_css_assertions, test_post_a11y
from .test_common import load_vectors, write_results, write_logs


def main():
  base_url = os.environ.get('IMPROVED_URL', 'http://127.0.0.1:5002')
  vectors = load_vectors()
  logs = []
  aggregate_results = []
  timestamp = datetime.utcnow().isoformat() + 'Z'

  with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    for module in (test_post_visual, test_post_css_assertions, test_post_a11y):
      aggregate_results.extend(module.run(page, base_url, 'post', logs, vectors))
    browser.close()

  payload = {
    'phase': 'post',
    'timestamp': timestamp,
    'url': base_url,
    'tests': aggregate_results
  }
  write_results(payload)
  write_logs(logs)


if __name__ == '__main__':
  main()
