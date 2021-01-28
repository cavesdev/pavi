"""
Here are the helper functions necessary to send a video for processing to the specified service.
"""
import os
import requests

from pavi.config.services import Services
from pavi.config.config import Config
from pavi.lib.mongo import MongoLib

Services.load_from_file('services.json')


def send_to_service(algorithm, video):
    print(f'Enviando el video para procesar con: {algorithm}')
    url = Services.get(algorithm) + '/process'
    files = {'video': open(video, 'rb')}
    res = requests.post(url, files=files)
    return res.json()


def upload_to_db(results):
    print('Subiendo los resultados a la base de datos...')

    db = MongoLib()
    collection = Config.get('db_collection')

    video_id = results.get('filename')
    video = db.get_by_field(collection, 'filename', video_id)

    if video is not None:

        found, index = has_algorithm(video, results)

        if found:
            # replace algorithm data
            video['processing'][index] = results['processing'][0]
        else:
            # add algorithm data
            video['processing'] += results['processing']

        db.update(collection, video.get('_id'), video)
    else:
        db.insert(collection, results)

    return video_id


def has_algorithm(video, data):
    algorithm = data['processing'][0]['algorithm']
    found = False
    found_index = 0
    index = 0
    found_index = 0
    for item in video['processing']:
        if item['algorithm'] == algorithm:
            found = True
            found_index = index
        index += 1
    return found, found_index
