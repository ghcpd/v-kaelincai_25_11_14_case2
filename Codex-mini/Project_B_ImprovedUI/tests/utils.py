import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
RESULT_FILE = BASE_DIR / 'results' / 'results_post.json'
LOG_FILE = BASE_DIR / 'logs' / 'log_post.txt'
SCREENSHOT_DIR = BASE_DIR / 'screenshots'
AXE_FILE = Path(__file__).resolve().parent / 'axe.min.js'

SCREENSHOT_DIR.mkdir(exist_ok=True)
if not RESULT_FILE.exists():
    RESULT_FILE.write_text('[]')


def append_result(entry):
    if RESULT_FILE.exists():
        data = json.loads(RESULT_FILE.read_text())
    else:
        data = []
    data = [item for item in data if item.get('test_id') != entry.get('test_id')]
    data.append(entry)
    RESULT_FILE.write_text(json.dumps(data, indent=2))


def record_console(test_id, messages):
    lines = [f"[{datetime.utcnow().isoformat()}][{test_id}] {m['type']} {m['text']}" for m in messages]
    if lines:
        with LOG_FILE.open('a', encoding='utf-8') as out:
            out.write('\n'.join(lines) + '\n')


def load_axe_script():
    if AXE_FILE.exists():
        return AXE_FILE.read_text(encoding='utf-8')
    raise FileNotFoundError('axe.min.js not found')
