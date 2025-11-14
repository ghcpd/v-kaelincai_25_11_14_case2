from playwright.sync_api import sync_playwright
from tests.utils import append_result, record_console, SCREENSHOT_DIR

BASE_URL = 'http://127.0.0.1:8010'


def test_pre_card_spacing_and_buttons():
    console_messages = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on('console', lambda msg: console_messages.append({'type': msg.type, 'text': msg.text()}))
        page.goto(BASE_URL, wait_until='networkidle')
        page.wait_for_timeout(500)
        card_style = page.eval_on_selector('.task-card', 'el => { const comp = window.getComputedStyle(el); return { padding: comp.padding, fontSize: comp.fontSize, background: comp.backgroundColor }; }')
        meta_weight = page.eval_on_selector('.task-card .meta', 'el => window.getComputedStyle(el).fontWeight')
        action_style = page.eval_on_selector('.action', 'el => { const comp = window.getComputedStyle(el); return { background: comp.backgroundColor, border: comp.border, cursor: comp.cursor }; }')
        page.hover('.action')
        hover_shadow = page.eval_on_selector('.action', 'el => window.getComputedStyle(el).boxShadow')
        test_screenshot = SCREENSHOT_DIR / 'screenshot_pre_spacing_hierarchy.png'
        page.screenshot(path=str(test_screenshot), full_page=False)
        append_result({
            'test_id': 'spacing_hierarchy',
            'status': 'pass',
            'screenshots': [test_screenshot.name],
            'measurements': {
                'padding': card_style['padding'],
                'title_font_size': card_style['fontSize'],
                'subtitle_weight': meta_weight,
                'button_background': action_style['background'],
                'button_border': action_style['border'],
                'button_cursor': action_style['cursor'],
                'hover_box_shadow': hover_shadow
            },
            'details': 'Measured dense card spacing, meta weight, and button affordances.'
        })
        record_console('spacing_hierarchy', console_messages)
        browser.close()
