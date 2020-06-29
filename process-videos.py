import json
import argparse

from pymongo import MongoClient

from detectors import VideoDetector

# argumentos que acepta el programa
ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Nombre del archivo de video a procesar')
ap.add_argument('-o', '--output', help='Nombre del archivo en donde se guardarán los resultados (JSON)')
ap.add_argument('-c', '--config', help='Nombre del archivo de donde se cargarán las configuraciones')
args = vars(ap.parse_args())

output_file = args['output'] or 'data.json'
config_file = args['config'] or None
video_file = args['video']

print('Cargando configuraciones...')
d = VideoDetector(config_file=config_file)

print('Cargando video...')
d.load_file(video_file)

print('Procesando video...')
d.process()

print('Guardando los resultados...')
d.write_json_to_file(output_file)

print('Subiendo los resultados a la base de datos...')
# load to mongodb
with open(output_file, "r") as f:
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

print('Listo!!!')


