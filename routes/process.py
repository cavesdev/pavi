import os

from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename

from scripts import yolo, pedestrian

bp = Blueprint('process', __name__)

ALLOWED_ALGORITHMS = {'yolo', 'pedestrian'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4'}
allowed_config_formats = ['json']


def upload_video():
    if 'video' not in request.files:
        raise AttributeError('Video not found in POST data')

    video = request.files['video']

    if video.filename == '':
        raise FileNotFoundError('No video selected.')
    elif video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        video.save(video_path)
    else:
        raise RuntimeError('An unknown error ocurred while uploading the video')

    return video_path


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS


@bp.route('/yolo', methods=['POST'])
def process_yolo():
    try:
        video_path = upload_video()
    except AttributeError:
        return {'message': 'video not found in POST data'}
    except FileNotFoundError:
        return {'message': 'No video selected.'}
    except RuntimeError:
        return {'message': 'An unknown error occurred while uploading the video'}

    # config from form
    user_config = {}
    for key in request.form:
        user_config[key] = request.form[key]

    yolo.process_video(video_path, user_config)

    return {'message': 'Video processed successfully'}


@bp.route('/pedestrian')
def process_pedestrian():
    try:
        video_path = upload_video()
    except AttributeError:
        return {'message': 'video not found in POST data'}
    except FileNotFoundError:
        return {'message': 'No video selected.'}
    except RuntimeError:
        return {'message': 'An unknown error occurred while uploading the video'}

    # get filename
    video_filename = video_path
    pedestrian.process_video(video_filename)

    return {'message': 'Video processed successfully'}





