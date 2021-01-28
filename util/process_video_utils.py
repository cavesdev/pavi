import os

from flask import abort
from werkzeug.utils import secure_filename

SUPPORTED_VIDEO_FORMATS = ['mp4']
SUPPORTED_ALGORITHMS = ['yolov3', 'pedestrian-tracker']


def validate_headers(headers):
    h_length = headers.get('Content-Length')
    h_algorithm = headers.get('Algorithm')

    try:
        h_length = int(h_length)
    except ValueError:
        abort(411, description="Incorrect length value.")

    if (h_length == 0 or
            h_algorithm is None):
        abort(400, description="Required headers are missing.")

    if h_algorithm not in SUPPORTED_ALGORITHMS:
        abort(404, description="The requested algorithm was not found.")


def save_uploaded_video(files, upload_folder):
    if 'video' not in files:
        abort(400, description="Video data not found in request.")

    video = files['video']

    if video.filename == '':
        abort(400, description="Video file not sent.")

    if video and supported_file(video.filename):
        filename = secure_filename(video.filename)
        video_path = os.path.join(upload_folder, filename)
        video.save(video_path)
        return video_path
    else:
        abort(415, description="Video format not supported.")


def supported_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in SUPPORTED_VIDEO_FORMATS
