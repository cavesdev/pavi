from flask import Blueprint, request, send_file
from pavi.config.config import Config
from pavi.util.process_video_utils import save_uploaded_video
from pavi.util.service_utils import send_to_service
from pavi.util.heatmap import request_heatmap

heatmap = Blueprint('simple_page', __name__,)


@heatmap.route('/heatmap/upload', methods=['POST'])
def process_heatmap():
    video_file = save_uploaded_video(request.files, Config.get('upload_folder'))

    heatmap_id = send_to_service(request.headers.get('Algorithm'), video_file)

    return {
        'id': heatmap_id['heatmap_id'],
        'message': 'Heatmap generated.'
    }


@heatmap.route('/heatmap/download/<string:heatmap_id>', methods=['GET'])
def get_heatmap(heatmap_id):
    heatmap_fn = request_heatmap(heatmap_id)
    return send_file(heatmap_fn, mimetype='image/png')
