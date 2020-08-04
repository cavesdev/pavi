import os
import subprocess
import sys
import shutil

ENV_VARS = ['UPLOAD_FOLDER', 'MONGO_URI', 'PROJECT_DIR']

print('Instalando dependencias...')
print('Instalando dependencias de Python...')

try:
    subprocess.check_call(['pip3', 'install', '-r', 'requirements.txt'])
except subprocess.CalledProcessError as err:
    print(f'Ocurrió un error al instalar las dependencias de Python: Error {err.returncode}. Saliendo...')
    exit(err.returncode)

print('Inicializando variables de entorno...')

if os.environ.get('UPLOAD_FOLDER') is None:
    os.environ['UPLOAD_FOLDER'] = 'static'

if os.environ.get('PROJECT_DIR') is None:
    os.environ['PROJECT_DIR'] = os.getcwd()

for var in ENV_VARS:
    if os.environ.get(var) is None:
        print(f'La variable de entorno {var} no existe. Saliendo...')
        exit(1)

print('Creando carpetas...')

project_dir = os.environ.get('PROJECT_DIR')
upload_folder = os.environ.get('UPLOAD_FOLDER')

videos_dir = os.path.join(project_dir, upload_folder, 'videos')
config_dir = os.path.join(project_dir, upload_folder, 'config')

if not os.path.exists(videos_dir):
    os.mkdir(videos_dir)
    print("El directorio ", videos_dir, " fue creado.")
else:
    print("El directorio ", videos_dir, " ya existe.")

if not os.path.exists(config_dir):
    os.mkdir(config_dir)
    print("El directorio ", config_dir, " fue creado.")
else:
    print("El directorio ", config_dir, " fue creado.")

print('Iniciando programa...')

subprocess.check_call([sys.executable, 'app.py'])
