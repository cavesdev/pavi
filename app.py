import json

from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo, DESCENDING

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/yolo"
mongo = PyMongo(app)


@app.route('/')
def index():
    """Return the main page and passes along the (maximum) 10 newest videos added to the database."""
    newest_videos = mongo.db.videos.find({}, {'filename': 1}).sort('_id', DESCENDING).limit(10)
    video_count = newest_videos.count()
    return render_template('index.html', video_count=video_count, videos=newest_videos)


@app.route('/query')
def query():
    """Queries the database for the given filename via get parameter"""
    filename = request.args.get('filename')
    video_data = mongo.db.videos.find_one({'filename': filename})
    return json.dumps(video_data, default=str)
