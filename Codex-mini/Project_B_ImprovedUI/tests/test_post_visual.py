from pathlib import Path
from playwright.sync_api import sync_playwright
from tests.utils import append_result, record_console, SCREENSHOT_DIR

BASE_URL = 'http://127.0.0.1:8020'


def test_post_visual_cards():
    console_messages = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on('console', lambda msg: console_messages.append({'type': msg.type, 'text': msg.text()}))
        page.goto(BASE_URL, wait_until='networkidle')
        page.wait_for_timeout(500)
        full_screenshot = SCREENSHOT_DIR / 'screenshot_post_ui.png'
        page.screenshot(path=str(full_screenshot), full_page=True)
        test_screenshot = SCREENSHOT_DIR / 'screenshot_post_visual.png'
        page.screenshot(path=str(test_screenshot), full_page=False)
        heights = page.evaluate('document.body.scrollHeight')
        append_result({
            'test_id': 'baseline_visual',
            'status': 'pass',
            'screenshots': [full_screenshot.name, test_screenshot.name],
            'measurements': {'page_height': heights},
            'details': 'Improved layout captured to compare spacing and clarity.'
        })
        record_console('baseline_visual', console_messages)
        browser.close()
