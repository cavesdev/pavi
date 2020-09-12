import argparse
import os
import subprocess
import sys
import json

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Nombre del archivo de video a procesar')
ap.add_argument('-c', '--config', help='Nombre del archivo de donde se cargarán las configuraciones')
args = vars(ap.parse_args())

print('Cargando configuraciones...')

video_filename = args['video'].strip()
upload_folder = os.environ.get('UPLOAD_FOLDER')
script_path = '/opt/intel/openvino/deployment_tools/demo/run_pedestrian_tracker.sh'
config_file = args['config'].strip()

with open(config_file, "r") as f:
    data = json.load(f)

try:
    no_show = data['no_show']
    no_save = data['no_save']
    save_json = data['json']
except KeyError:
    print('Error en el archivo de configuración. Saliendo...')
    exit(1)

sample_options = ''

if no_show:
    sample_options += '-no_show '
if no_save:
    sample_options += '-no_save '
if save_json:
    sample_options += '-json'

command = f'{script_path} -i {video_filename} -sample-options {sample_options}'

print('Procesando video...')

project_dir = os.environ.get('PROJECT_DIR')
volume_path = os.path.join(project_dir, upload_folder)

subprocess.call(command, shell=True)

print('Guardando los resultados...')

project_dir = os.environ.get('PROJECT_DIR')
output_file = os.path.join(project_dir, upload_folder, 'data.json')
script_path = os.path.join(project_dir, 'scripts', 'upload-to-db.py')

subprocess.check_call([sys.executable, script_path, f'-i {output_file}'])

print('Listo!!!')