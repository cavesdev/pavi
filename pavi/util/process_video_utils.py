import os
import uuid

from flask import abort

SUPPORTED_VIDEO_FORMATS = ['mp4']

def save_uploaded_video(files, upload_folder):
    if 'video' not in files:
        abort(400, description="Video data not found in request.")

    video = files['video']

    if video.filename == '':
        abort(400, description="Video file not sent.")

    if video and supported_file(video.filename):
        _, ext = os.path.splitext(video.filename)
        filename = str(uuid.uuid1()) + ext
        video_path = os.path.join(upload_folder, filename)
        video.save(video_path)
        return video_path
    else:
        abort(415, description="Video format not supported.")


def supported_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in SUPPORTED_VIDEO_FORMATS
