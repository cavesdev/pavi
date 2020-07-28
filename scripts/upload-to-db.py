import argparse
import json

from pymongo import MongoClient

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True, help='JSON a cargar en la base de datos')
args = vars(ap.parse_args())

json_file = args['input'].strip()

print('Subiendo los resultados a la base de datos...')
# load to mongodb
with open(json_file, "r") as f:
    data = json.load(f)

client = MongoClient()
db = client.yolo
videos = db.videos

video = videos.find_one({'filename': data['filename']})

if video is not None:
    videos.replace_one(
        {'filename': data['filename']},
        data
    )
else:
    videos.insert_one(data)