import os
import subprocess

print('Inicializando variables de entorno...')

ENV_VARS = ['UPLOAD_FOLDER', 'MONGO_URI']

# default value for UPLOAD_FOLDER environment variable.
if os.environ.get('UPLOAD_FOLDER') is None:
    os.environ['UPLOAD_FOLDER'] = 'static'

for var in ENV_VARS:
    if os.environ.get(var) is None:
        print(f'La variable de entorno {var} no existe. Saliendo...')
        exit(1)

print('Iniciando programa...')

subprocess.run(['python3', 'app.py'])

