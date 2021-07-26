import json
import os

from pavi.config import Config  # import .env
from pavi.lib import MongoLib
from pavi.util import save_uploaded_video, person_filter

from flask import Flask, request
from flask_cors import CORS
from bson import json_util

# preprocessing
UPLOAD_FOLDER = Config.get('upload_folder')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = Config.get('upload_size_limit')
CORS(app)

db_client = MongoLib()
collection = Config.get('db_collection')


@app.route('/videos/<video_id>', methods=['GET'])
def get_result(video_id):
    result = db_client.get_by_field(collection, 'filename', video_id)

    if results_filter := request.args.get('filter'):
        if results_filter == 'person':
            result = person_filter(result)

    return json.loads(json_util.dumps(result))


@app.route('/videos', methods=['POST'])
def process_video():
    video_path = save_uploaded_video(request.files, UPLOAD_FOLDER)

    # send to openvino

    # video_id = upload_to_db(results)

    # cleanup video files
    if os.path.exists(video_path):
        os.remove(video_path)

    return {
        'id': video_id,
        'message': 'Video uploaded.'
    }


if __name__ == '__main__':
    app.run()
