from flask import Flask, send_from_directory
import pathlib

static_dir = pathlib.Path(__file__).resolve().parents[1] / 'src'
app = Flask('improved', static_folder=str(static_dir), static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:resource>')
def resources(resource):
    return send_from_directory(app.static_folder, resource)

if __name__ == '__main__':
    app.run(port=8020)
