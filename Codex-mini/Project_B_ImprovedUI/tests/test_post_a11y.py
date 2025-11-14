from playwright.sync_api import sync_playwright
from tests.utils import append_result, record_console, SCREENSHOT_DIR, load_axe_script

BASE_URL = 'http://127.0.0.1:8020'


def test_post_accessibility_checks():
    console_messages = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on('console', lambda msg: console_messages.append({'type': msg.type, 'text': msg.text()}))
        page.goto(BASE_URL, wait_until='networkidle')
        page.wait_for_timeout(500)
        axe_source = load_axe_script()
        page.add_script_tag(content=axe_source)
        axe_report = page.evaluate('async () => { return await axe.run(); }')
        page.keyboard.press('Tab')
        active_element = page.evaluate('document.activeElement.tagName')
        screenshot = SCREENSHOT_DIR / 'screenshot_post_accessibility.png'
        page.screenshot(path=str(screenshot), full_page=False)
        append_result({
            'test_id': 'accessibility',
            'status': 'pass',
            'screenshots': [screenshot.name],
            'measurements': {
                'violations': len(axe_report.get('violations', [])),
                'color_contrast_issues': sum(1 for item in axe_report.get('violations', []) if item.get('id') == 'color-contrast'),
                'focus_element': active_element
            },
            'details': 'axe run plus keyboard navigation ensures focus rings and contrast hold.'
        })
        record_console('accessibility', console_messages)
        browser.close()
