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

    return {
        'message': 'Video uploaded.'
    }


if __name__ == '__main__':
    app.run()
