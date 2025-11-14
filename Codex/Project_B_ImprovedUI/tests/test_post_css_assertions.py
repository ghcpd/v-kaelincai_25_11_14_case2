from typing import List, Dict
from playwright.sync_api import Page
from .test_common import screenshot_path, px_to_float, normalize_color


def _shadow_depth(shadow_value: str) -> float:
  tokens = shadow_value.replace(',', ' ').split()
  px_values = []
  for token in tokens:
    if token.endswith('px'):
      try:
        px_values.append(abs(float(token.replace('px', ''))))
      except ValueError:
        continue
  return max(px_values) if px_values else 0.0


def run(page: Page, base_url: str, phase: str, logs: List[str], vectors: List[Dict]):
  results = []
  card_vector = next(v for v in vectors if v['test_id'] == 'card_spacing_hierarchy')
  button_vector = next(v for v in vectors if v['test_id'] == 'button_hover_feedback')
  icon_vector = next(v for v in vectors if v['test_id'] == 'iconography_alignment')

  page.goto(base_url, wait_until='networkidle')
  page.wait_for_selector('.task-card')

  # Card spacing check
  spacing = page.eval_on_selector('.task-card', '''el => {
    const styles = getComputedStyle(el);
    return {
      paddingTop: styles.paddingTop,
      paddingRight: styles.paddingRight,
      marginBottom: styles.marginBottom,
      boxShadow: styles.boxShadow
    };
  }''')
  title = page.eval_on_selector('.task-card .task-title', 'el => getComputedStyle(el).fontSize')
  meta_weight = page.evaluate(\"\"\"() => {
    const meta = document.querySelector('.task-card .task-meta') || document.querySelector('.task-card .meta-list');
    if (!meta) { return '400'; }
    return getComputedStyle(meta).fontWeight;
  }\"\"\")
  padding_value = min(px_to_float(spacing['paddingTop']), px_to_float(spacing['paddingRight']))
  title_size = px_to_float(title)
  meta_value = px_to_float(meta_weight)

  padding_threshold = card_vector['expected']['padding'].get('min', 0)
  if phase in card_vector['expected']['padding'].get('phase', {}):
    padding_threshold = card_vector['expected']['padding']['phase'][phase]
  title_threshold = card_vector['expected']['title-font-size'].get('min', 0)
  if phase in card_vector['expected']['title-font-size'].get('phase', {}):
    title_threshold = card_vector['expected']['title-font-size']['phase'][phase]
  meta_max = card_vector['expected']['meta-font-weight'].get('max', 700)

  spacing_pass = padding_value >= padding_threshold and title_size >= title_threshold and meta_value <= meta_max
  spacing_name = card_vector.get('screenshot', 'screenshot_${phase}_card_spacing.png').replace('${phase}', phase)
  page.locator('.task-card').first.screenshot(path=str(screenshot_path(spacing_name)))
  spacing_result = {
    'test_id': 'card_spacing_hierarchy',
    'status': 'passed' if spacing_pass else 'failed',
    'measurements': {
      'padding_px': padding_value,
      'title_font_px': title_size,
      'meta_font_weight': meta_value
    },
    'screenshot': spacing_name
  }
  results.append(spacing_result)
  logs.append(f"[{phase}] Card spacing padding={padding_value}px title={title_size}px meta_weight={meta_value}")

  # Button hover check
  button_selector = '.task-card .btn-primary'
  button = page.locator(button_selector).first
  button.hover()
  button_styles = page.eval_on_selector(button_selector, 'el => { const s = getComputedStyle(el); return { bg: s.backgroundColor, shadow: s.boxShadow, cursor: s.cursor }; }')
  background = button_styles['bg']
  background_hex = normalize_color(background)
  shadow_strength = _shadow_depth(button_styles['shadow'])
  cursor_state = button_styles['cursor']

  bg_expectations = button_vector['expected']['background-color']
  expected_color = bg_expectations.get('baseline' if phase == 'pre' else 'post')
  hover_shadow_min = button_vector['expected']['hover-shadow']['min']
  cursor_expected = button_vector['expected']['cursor']
  button_pass = (background_hex == expected_color.lower()) if expected_color else False
  button_pass = button_pass and shadow_strength >= hover_shadow_min and cursor_state == cursor_expected

  button_name = button_vector['steps'][3]['name'].replace('${phase}', phase)
  button.screenshot(path=str(screenshot_path(button_name)))
  button_result = {
    'test_id': 'button_hover_feedback',
    'status': 'passed' if button_pass else 'failed',
    'measurements': {
      'background': background_hex,
      'shadow_strength': shadow_strength,
      'cursor': cursor_state
    },
    'screenshot': button_name
  }
  results.append(button_result)
  logs.append(f"[{phase}] Button hover bg={background} shadow={shadow_strength} cursor={cursor_state}")

  # Iconography check
  icon_styles = page.eval_on_selector('.task-card .task-icon', 'el => { const rect = el.getBoundingClientRect(); const s = getComputedStyle(el); return { width: rect.width, height: rect.height, marginRight: s.marginRight }; }')
  icon_styles_2 = page.eval_on_selector('.task-card:nth-child(2) .task-icon', 'el => { const rect = el.getBoundingClientRect(); return { width: rect.width, height: rect.height }; }')
  width = icon_styles['width']
  height = icon_styles['height']
  margin_right = px_to_float(icon_styles['marginRight'])
  width_2 = icon_styles_2['width']
  height_2 = icon_styles_2['height']

  size_expect = icon_vector['expected']['size']
  width_target = size_expect.get('width')
  height_range = size_expect.get('height-range', [0, 100])
  alignment_expect = icon_vector['expected']['alignment']['margin-right-min']
  icon_pass = height_range[0] <= height <= height_range[1] and height_range[0] <= height_2 <= height_range[1]
  if width_target:
    icon_pass = icon_pass and abs(width - width_target) <= 8 and abs(width_2 - width_target) <= 8
  icon_pass = icon_pass and margin_right >= alignment_expect

  icon_name = icon_vector.get('screenshot', 'screenshot_${phase}_iconography.png').replace('${phase}', phase)
  page.locator('.task-card .task-icon').first.screenshot(path=str(screenshot_path(icon_name)))
  icon_result = {
    'test_id': 'iconography_alignment',
    'status': 'passed' if icon_pass else 'failed',
    'measurements': {
      'icon1': {'width': width, 'height': height},
      'icon2': {'width': width_2, 'height': height_2},
      'margin_right': margin_right
    },
    'screenshot': icon_name
  }
  results.append(icon_result)
  logs.append(f"[{phase}] Icon sizes w1={width} h1={height} w2={width_2} h2={height_2} marginRight={margin_right}")

  return results
