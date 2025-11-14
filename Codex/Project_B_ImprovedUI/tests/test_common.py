import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
SCREENSHOT_DIR = BASE_DIR / 'screenshots'
LOG_PATH = BASE_DIR / 'logs' / 'log_post.txt'
RESULT_PATH = BASE_DIR / 'results' / 'results_post.json'
TEST_DATA_PATH = BASE_DIR / 'data' / 'test_data.json'

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_vectors():
  with open(TEST_DATA_PATH, 'r', encoding='utf-8') as handle:
    return json.load(handle)


def luminance(rgb):
  def channel(val):
    val = val / 255
    return val / 12.92 if val <= 0.03928 else ((val + 0.055) / 1.055) ** 2.4
  r, g, b = rgb
  return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(rgb_a, rgb_b):
  l1 = luminance(rgb_a) + 0.05
  l2 = luminance(rgb_b) + 0.05
  return round(max(l1, l2) / min(l1, l2), 2)


def parse_color(value):
  if isinstance(value, str) and value.startswith('rgb'):
    nums = value[value.find('(')+1:value.find(')')].split(',')
    return tuple(int(float(n.strip())) for n in nums[:3])
  if isinstance(value, str) and value.startswith('#') and len(value) == 7:
    return tuple(int(value[i:i+2], 16) for i in (1, 3, 5))
  return (0, 0, 0)


def normalize_color(value):
  rgb = parse_color(value)
  return '#{0:02x}{1:02x}{2:02x}'.format(*rgb)


def px_to_float(value):
  if isinstance(value, (int, float)):
    return float(value)
  if isinstance(value, str) and value.strip().isdigit():
    return float(value.strip())
  if isinstance(value, str) and value.endswith('px'):
    try:
      return float(value.replace('px', '').strip())
    except ValueError:
      return 0.0
  return 0.0


def write_results(data):
  with open(RESULT_PATH, 'w', encoding='utf-8') as handle:
    json.dump(data, handle, indent=2)


def write_logs(lines):
  timestamp = datetime.utcnow().isoformat() + 'Z'
  header = f'Test run @ {timestamp}\n'
  with open(LOG_PATH, 'w', encoding='utf-8') as handle:
    handle.write(header)
    for line in lines:
      handle.write(line + '\n')


def screenshot_path(name):
  return SCREENSHOT_DIR / name

