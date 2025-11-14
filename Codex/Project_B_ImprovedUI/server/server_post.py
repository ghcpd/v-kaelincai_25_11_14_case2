import json
from pathlib import Path
from flask import Flask, send_from_directory, jsonify

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / 'src'
DATA_DIR = BASE_DIR / 'data'

app = Flask(__name__, static_folder=str(SRC_DIR), static_url_path='')

@app.route('/')
def index():
  return send_from_directory(app.static_folder, 'index.html')

@app.route('/data/<path:filename>')
def data_file(filename):
  return send_from_directory(DATA_DIR, filename)

@app.route('/healthz')
def health():
  return jsonify({"status": "ok", "project": "improved"})

@app.route('/<path:asset>')
def serve_asset(asset):
  return send_from_directory(app.static_folder, asset)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5002)
