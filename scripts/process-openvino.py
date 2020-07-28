import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', required=True, help='Nombre del archivo de video a procesar')
args = vars(ap.parse_args())

video_file = args['video']

print('Procesando video...')