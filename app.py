import json
from bson import json_util

from pavi.lib.mongo import MongoLib
from pavi.config.config import Config
from pavi.util.process_video_utils import validate_headers, save_uploaded_video
from pavi.util.services_utils import send_to_service, upload_to_db

from flask import Flask, request


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = Config.get('upload_size_limit')

db_client = MongoLib()
collection = Config.get('db_collection')


@app.route('/results/<video_id>', methods=['GET'])
def get_result(video_id):
    result = db_client.get_by_field(collection, 'filename', video_id)
    return json.loads(json_util.dumps(result))


@app.route('/upload', methods=['POST'])
def process_video():
    validate_headers(request.headers)
    video_path = save_uploaded_video(request.files, Config.get('upload_folder'))

    results = send_to_service(request.headers.get('Algorithm'), video_path)
    video_id = upload_to_db(results)

    return {
        'id': video_id,
        'message': 'Video uploaded.'
    }


if __name__ == '__main__':
    app.run()
