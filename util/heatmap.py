import os

import requests
from config import Services
from flask import abort

HEATMAP_FOLDER = os.path.join('static', 'heatmap')

if not os.path.exists(HEATMAP_FOLDER):
    os.makedirs(HEATMAP_FOLDER)


def request_heatmap(heatmap_id):
    url = Services.get('heatmap') + f'/download/{heatmap_id}'
    response = requests.get(url)
    heatmap_fn = os.path.join(HEATMAP_FOLDER, f'{heatmap_id}.png')

    if not response.ok:
        abort(404, description='Heatmap id not found.')

    with open(heatmap_fn, 'wb') as f:
        f.write(response.content)

    return heatmap_fn
