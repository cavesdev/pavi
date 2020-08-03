import os
import argparse
import json
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Nombre del archivo de video a procesar')
ap.add_argument('-c', '--config', help='Nombre del archivo de donde se cargarán las configuraciones')
args = vars(ap.parse_args())

video_filename = args['video']
model_detection_path = '$INTEL_OPENVINO_DIR/deployment_tools/tools/model_downloader/intel/person-detection-retail' \
                       '-0013/FP16/person-detection-retail-0013.xml '
model_reidentification_path = '$INTEL_OPENVINO_DIR/deployment_tools/tools/model_downloader/intel/person' \
                              '-reidentification-retail-0031/FP16/person-reidentification-retail-0031.xml '

config_file = args['config']
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

openvino_dir = os.environ.get('INTEL_OPENVINO_DIR')
script_path = os.path.join(openvino_dir, 'deployment_tools', 'demo', 'update_and_run_pedestrian_tracker.sh')

subprocess.check_call([script_path,
                       f'-i {video_filename}',
                       f'-m_det {model_detection_path}',
                       f'-m_reid {model_reidentification_path}',
                       f'-sample-options {sample_options}'])
