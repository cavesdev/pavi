import json
import os

from bson import json_util

from pavi.lib.mongo import MongoLib
from pavi.config.config import Config
from pavi.util.process_video_utils import validate_headers, save_uploaded_video
from pavi.util.service_utils import send_to_service, upload_to_db
from pavi.util.filter_utils import person_filter
from pavi.routes.heatmap import heatmap

from flask import Flask, request
from flask_cors import CORS

# preprocessing
UPLOAD_FOLDER = Config.get('upload_folder')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = Config.get('upload_size_limit')
app.register_blueprint(heatmap)
CORS(app)

db_client = MongoLib()
collection = Config.get('db_collection')


@app.route('/results/<video_id>', methods=['GET'])
def get_result(video_id):
    result = db_client.get_by_field(collection, 'filename', video_id)

    if results_filter := request.args.get('filter'):
        if results_filter == 'person':
            result = person_filter(result)

    return json.loads(json_util.dumps(result))


@app.route('/upload', methods=['POST'])
def process_video():
    validate_headers(request.headers)
    video_file = save_uploaded_video(request.files, UPLOAD_FOLDER)

    results = send_to_service(request.headers.get('Algorithm'), video_file)
    video_id = upload_to_db(results)

    # cleanup video files
    if os.path.exists(video_file):
        os.remove(video_file)

    return {
        'id': video_id,
        'message': 'Video uploaded.'
    }


if __name__ == '__main__':
    app.run()
