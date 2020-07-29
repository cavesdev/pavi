import argparse
import json
import os

from pymongo import MongoClient

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True, help='JSON a cargar en la base de datos')
args = vars(ap.parse_args())

json_file = args['input'].strip()

print('Subiendo los resultados a la base de datos...')
# load to mongodb
with open(json_file, "r") as f:
    data = json.load(f)

mongo_url = os.environ.get('MONGO_URI')
client = MongoClient(mongo_url)
db = client.pavi
videos = db.videos

video = videos.find_one({'filename': data['filename']})

if video is not None:
    videos.replace_one(
        {'filename': data['filename']},
        data
    )
else:
    videos.insert_one(data)