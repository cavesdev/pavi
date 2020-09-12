import json
import subprocess
import os
import sys

from flask import Flask, render_template, request, redirect, flash
from flask_pymongo import PyMongo, DESCENDING
from werkzeug.utils import secure_filename

mongo_url = os.environ.get('MONGO_URI')
upload_folder = os.environ.get('UPLOAD_FOLDER')

app = Flask(__name__)
app.config["MONGO_URI"] = mongo_url
app.config["UPLOAD_FOLDER"] = upload_folder

mongo = PyMongo(app)
db = mongo.db.videos


@app.route('/')
def index():
    """Regresa los 10 videos más recientes de la base de datos"""
    newest_videos = db.find({}, {'filename': 1}).sort('_id', DESCENDING).limit(10)
    video_count = newest_videos.count()
    return render_template('index.html', video_count=video_count, videos=newest_videos)


@app.route('/search')
def search():
    """Buscar en la base de datos por nombre del video"""
    filename = request.args.get('filename')
    video_data = db.find_one({'filename': filename})
    return json.dumps(video_data, default=str)


allowed_algorithms = ['yolo', 'pedestrian']
allowed_video_formats = ['mp4']
allowed_config_formats = ['json']


def allowed_file(filename, formats):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in formats


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
    """Procesar un nuevo video"""

    if request.method != 'POST':
        flash('Método HTTP no aceptado.')
        return redirect(request.url)

    if 'video' not in request.files:
        flash('El formulario no contiene el apartado para subir video.')
        return redirect(request.url)

    video = request.files['video']

    if video.filename == '':
        flash('Ningún video seleccionado.')
        return redirect(request.url)
    elif video and allowed_file(video.filename, allowed_video_formats):
        video_filename = secure_filename(video.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'videos', video_filename)
        video.save(video_path)
    else:
        flash('Ocurrió un error con el archivo de video.')
        return redirect(request.url)

    config = request.files['config']

    if config.filename == '':
        flash('Ningún archivo de configuración seleccionado.')
        return redirect(request.url)
    elif config and allowed_file(config.filename, allowed_config_formats):
        config_filename = secure_filename(config.filename)
        config_path = os.path.join(app.config['UPLOAD_FOLDER'], 'config', config_filename)
        config.save(config_path)
    else:
        flash('Ocurrio un error.')
        return redirect(request.url)

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