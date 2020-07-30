import argparse
import os
import subprocess
import docker

client = docker.from_env()

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Nombre del archivo de video a procesar')
args = vars(ap.parse_args())

print('Cargando configuraciones...')

video_filename = args['video']
upload_folder = os.environ.get('UPLOAD_FOLDER')
script_path = 'deployment_tools/demo/run_pedestrian_tracker.sh'
model_detection_path = '$INTEL_OPENVINO_DIR/deployment_tools/tools/model_downloader/intel/person-detection-retail' \
                       '-0013/FP16/person-detection-retail-0013.xml '
model_reidentification_path = '$INTEL_OPENVINO_DIR/deployment_tools/tools/model_downloader/intel/person' \
                              '-reidentification-retail-0031/FP16/person-reidentification-retail-0031.xml '
sample_options = '-no_show -no_save -json'

command = f'/bin/bash -c "{script_path} -i {video_filename} -m_det {model_detection_path} ' \
          f'-m_reid {model_reidentification_path} -sample-options {sample_options}"'

print('Procesando video...')

client.containers.run(
    tty=True,
    user=0,
    volumes={f'../{upload_folder}': {'bind': '/docker', 'mode': 'rw'}},
    remove=True,
    image='openvinobuild',
    command=command
)

print('Guardando los resultados...')

output_file = os.path.join('..', upload_folder, 'data.json')
subprocess.run(['python3', 'upload-to-db.py', f'-i {output_file}'])

print('Listo!!!')