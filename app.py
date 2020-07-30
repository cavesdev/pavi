import json
import subprocess
import os

from flask import Flask, render_template, request, redirect, flash
from flask_pymongo import PyMongo, DESCENDING
from werkzeug.utils import secure_filename

if 'MONGO_URI' not in os.environ:
    print('Error. La variable de entorno MONGO_URI no existe. Para mayor información consultar el manual de uso')
    exit(1)

mongo_url = os.environ.get('MONGO_URI')
temp_folder = os.environ.get('TEMP_FOLDER')

app = Flask(__name__)
app.config["MONGO_URI"] = mongo_url
mongo = PyMongo(app)
db = mongo.db.videos


@app.route('/')
def index():
    """Regresa los 10 videos más recientes de la base de datos"""
    newest_videos = db.find({}, {'filename': 1}).sort('_id', DESCENDING).limit(10)
    video_count = newest_videos.count()
    return render_template('index.html', video_count=video_count, videos=newest_videos)


@app.route('/search', method=["GET"])
def query():
    """Buscar en la base de datos por nombre del video"""
    filename = request.args.get('filename')
    video_data = db.find_one({'filename': filename})
    return json.dumps(video_data, default=str)


allowed_algorithms = ['yolo', 'pedestrian']
allowed_video_formats = ['mp4']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_video_formats


def run_yolo(video, config):
    if config is not None:
        subprocess.run(['python3', 'process-yolo.py', f'-v {video}', f'-c {config}'])
    else:
        subprocess.run(['python3', 'process-yolo.py', f'-v {video}'])


def run_pedestrian():
    pass


@app.route('/process', methods=['POST'])
def process():
    """Procesar un nuevo video"""

    if request.method != 'POST':
        flash('Not an accepted HTTP method')
        return redirect(request.url)

    if 'video' not in request.files:
        flash('No video selector in form')
        return redirect(request.url)

    video = request.files['video']

    if video.filename == '':
        flash('No video selected')
        return redirect(request.url)

    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    config = request.form.get('config-route') or None
    algorithm = request.form.get('algorithm')

    if algorithm not in allowed_algorithms:
        flash('Invalid algorithm selected.')
        return redirect(request.url)

    if algorithm == 'yolo':
        run_yolo(video, config)
    elif algorithm == 'pedestrian':
        run_pedestrian(video)

    return redirect('index.html')
