from flask import Blueprint, request
from lib.mongo import MongoLib
from bson.json_util import dumps as json_dumps

collection = 'videos'
db = MongoLib()

bp = Blueprint('videos', __name__)


@bp.route('/')
def get_videos():
    limit = request.args.get('limit') or 0
    videos = db.get_all(collection, limit=int(limit))
    return {
        'data': json_dumps(videos),
        'message': 'Retrieved videos from database'
    }


@bp.route('/<video_id>')
def get_video(video_id):
    video = db.get(collection, video_id)
    return {
        'data': json_dumps(video),
        'message': 'Retrieved video from database'
    }


@bp.route('/', methods=['POST'])
def insert_video():
    document = request.get_json()
    inserted_video_id = db.insert(collection, document)
    return {
        'id': inserted_video_id,
        'message': 'Inserted video with appended ID.'
    }


@bp.route('/<video_id>', methods=['PUT'])
def update_video(video_id):
    data = request.get_json()
    updated_video_id = db.update(collection, video_id, data)
    return {
        'id': updated_video_id,
        'message': 'Updated video with appended ID.'
    }


@bp.route('/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    deleted_video_id = db.delete(collection, video_id)
    return {
        'id': deleted_video_id,
        'message': 'Deleted video with appended ID.'
    }


