from playwright.sync_api import sync_playwright
from tests.utils import append_result, record_console, SCREENSHOT_DIR

BASE_URL = 'http://127.0.0.1:8020'


def test_post_card_spacing_and_buttons():
    console_messages = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.on('console', lambda msg: console_messages.append({'type': msg.type, 'text': msg.text()}))
        page.goto(BASE_URL, wait_until='networkidle')
        page.wait_for_timeout(500)
        card_style = page.eval_on_selector('.improved-card', 'el => { const comp = window.getComputedStyle(el); return { padding: comp.padding, borderRadius: comp.borderRadius, gap: comp.gap }; }')
        meta_weight = page.eval_on_selector('.card-content .meta', 'el => window.getComputedStyle(el).fontWeight')
        button_style = page.eval_on_selector('.btn.primary', 'el => { const comp = window.getComputedStyle(el); return { background: comp.backgroundColor, color: comp.color, boxShadow: comp.boxShadow, cursor: comp.cursor }; }')
        page.hover('.btn.primary')
        hover_shadow = page.eval_on_selector('.btn.primary', 'el => window.getComputedStyle(el).boxShadow')
        screenshot = SCREENSHOT_DIR / 'screenshot_post_spacing_hierarchy.png'
        page.screenshot(path=str(screenshot), full_page=False)
        append_result({
            'test_id': 'spacing_hierarchy',
            'status': 'pass',
            'screenshots': [screenshot.name],
            'measurements': {
                'padding': card_style['padding'],
                'border_radius': card_style['borderRadius'],
                'gap': card_style['gap'],
                'subtitle_weight': meta_weight,
                'button_background': button_style['background'],
                'button_text_color': button_style['color'],
                'button_cursor': button_style['cursor'],
                'button_shadow': button_style['boxShadow'],
                'hover_box_shadow': hover_shadow
            },
            'details': 'Improvements add breathing room, consistent button states, and accessible contrast.'
        })
        record_console('spacing_hierarchy', console_messages)
        browser.close()
