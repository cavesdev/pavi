import argparse, subprocess

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

subprocess.run(['python3', 'upload-to-db.py', f'-i {output_file}'])

print('Listo!!!')


