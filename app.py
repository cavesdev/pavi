from lib.mongo import MongoLib
from config.config import Config
from bson.objectid import ObjectId
from bson.errors import InvalidId
from util.process_video_utils import validate_headers, save_uploaded_video

from flask import Flask, request, abort


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = Config.get('upload_size_limit')

db_client = MongoLib()
collection = Config.get('db_collection')


@app.route('/results/<video_id>', methods=['GET'])
def get_result(video_id):
    try:
        video_id = ObjectId(video_id)
    except InvalidId:
        abort(400, description="Incorrect ID value, please refer to the documentation.")

    return db_client.get(collection, video_id)


@app.route('/upload', methods=['POST'])
def process_video():
    validate_headers(request.headers)
    save_uploaded_video(request.files, Config.get('upload_folder'))

<<<<<<< HEAD
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
    script_path = os.path.join('scripts', 'process-pedestrian-docker-inst.py')
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
=======
    return {
        'message': 'Video uploaded.'
    }
>>>>>>> arq_refactor


if __name__ == '__main__':
    app.run()
