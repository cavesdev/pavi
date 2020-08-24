import json
import os

import docker
from flask import current_app

CONFIG_FILENAME = 'config.json'
RESULT_FILENAME = 'result.json'

CONFIG_FILE_PATH = os.path.join('scripts', 'helpers', 'pedestrian', CONFIG_FILENAME)
RESULT_FILE_PATH = os.path.join('scripts', 'helpers', 'pedestrian', RESULT_FILENAME)


def process_video(video_filename):
    config = load_config()
    sample_options = get_sample_options(config)
    script_path = 'deployment_tools/demo/run_pedestrian_tracker.sh'

    command = f'/bin/bash -c "{script_path} -i {video_filename} -sample-options {sample_options}"'

    print('Procesando video...')

    volume_path = os.path.join(current_app.config['BASE_DIR'], current_app.config['UPLOAD_FOLDER'])
    client = docker.from_env()

    client.containers.run(
        tty=True,
        user=0,
        volumes={volume_path: {'bind': '/docker', 'mode': 'rw'}},
        remove=True,
        image='openvinobuild',
        command=command
    )

    print('Guardando los resultados...')

    #subir a base de datos

    print('Listo!!!')


def load_config():
    config_file = os.path.join(current_app.config['BASE_DIR'], CONFIG_FILE_PATH)

    # load base config
    with open(config_file, 'r') as f:
        config = json.load(f)

    return config


def get_sample_options(config):
    sample_options = ''

    if config['no_show']:
        sample_options += '-no_show '
    if config['no_save']:
        sample_options += '-no_save '
    if config['json']:
        sample_options += '-json'

    return sample_options
