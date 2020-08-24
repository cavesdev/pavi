import subprocess
import os
import sys

from flask import Flask, request, redirect, flash, render_template
from routes import videos, process
from werkzeug.utils import secure_filename

upload_folder = os.environ.get('UPLOAD_FOLDER')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['BASE_DIR'] = os.getcwd()

app.register_blueprint(videos.bp, url_prefix='/api/videos')
app.register_blueprint(process.bp, url_prefix='/api/process')


@app.route('/')
def index():
    return render_template('index.html')


def run_yolo(video, config):
    script_path = os.path.join('scripts', 'process-yolo.py')
    if len(config) > 1:
        subprocess.run([sys.executable, script_path, f'-v {video}', f'-c {config}'])
    else:
        subprocess.run([sys.executable, script_path, f'-v {video}'])


def run_pedestrian(video_filename, config):
    script_path = os.path.join('scripts', 'process-pedestrian-docker.py')
    subprocess.run([sys.executable, script_path, f'-v {video_filename}', f'-c {config}'])


@app.route('/process', methods=['POST'])
def process():

    config = request.files['config']

    if config.filename == '':
        flash('Ningún archivo de configuración seleccionado.')
        return redirect(request.url)
    elif config and allowed_file(config.filename, allowed_config_formats):
        config_filename = secure_filename(config.filename)
        config_path = os.path.join(app.config['UPLOAD_FOLDER'], 'config', config_filename)
        config.save(config_path)

    abs_config_path = os.path.join(os.getcwd(), config_path)
    abs_video_path = os.path.join(os.getcwd(), video_path)
    algorithm = request.form.get('algorithm')

    if algorithm not in allowed_algorithms:
        flash('Algoritmo inválido seleccionado.')
        return redirect(request.url)

    if algorithm == 'yolo':
        run_yolo(abs_video_path, abs_config_path)
    elif algorithm == 'pedestrian':
        run_pedestrian(video_filename, abs_config_path)

    return redirect('/')


if __name__ == '__main__':
    app.run()