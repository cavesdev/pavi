from flask import Blueprint, request

process = Blueprint('process', __name__)


@process.route('/yolo', methods=['POST'])
def process_yolo():
    if 'video' not in request.files:
        pass