import json
import os

from pavi.config import Config  # import .env
from pavi.lib import MongoLib
from pavi.util import save_uploaded_video
from pavi.util.service_utils import send_to_service

from flask import Flask, request, abort
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
    try:
        algorithm = request.form.get('algorithm')
        video_path = save_uploaded_video(request.files, UPLOAD_FOLDER)
        send_to_service(algorithm, video_path)
    except RuntimeError as e:
        abort(400, description=str(e))

    # video_id = upload_to_db(results)

    # cleanup video files
    if os.path.exists(video_path):
        os.remove(video_path)

    return {
        'id': 1,
        'message': 'Video uploaded.'
    }


if __name__ == '__main__':
    app.run()
