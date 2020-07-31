import os
import subprocess
import docker.errors

IMAGE_NAME = 'openvinobuild'
ENV_VARS = ['UPLOAD_FOLDER', 'MONGO_URI', 'PROJECT_DIR']

print('Instalando dependencias...')
print('Instalando dependencias de Python...')

try:
    subprocess.check_call(['pip3', 'install', '-r', 'requirements.txt'])
except subprocess.CalledProcessError as err:
    print(f'Ocurrió un error al instalar las dependencias de Python: Error {err.returncode}. Saliendo...')
    exit(err.returncode)

print('Checando si existe la imagen de Docker...')

client = docker.from_env()

try:
    client.images.get(IMAGE_NAME)
except docker.errors.ImageNotFound:
    print(f'La imagen {IMAGE_NAME} no existe en Docker. Favor de referirse al manual de usuario para las instrucciones'
          f' de instalación. Saliendo...')
    exit(1)

print('Inicializando variables de entorno...')

# default value for UPLOAD_FOLDER environment variable.
if os.environ.get('UPLOAD_FOLDER') is None:
    os.environ['UPLOAD_FOLDER'] = 'static'

if os.environ.get('PROJECT_DIR') is None:
    os.environ['PROJECT_DIR'] = os.getcwd()

for var in ENV_VARS:
    if os.environ.get(var) is None:
        print(f'La variable de entorno {var} no existe. Saliendo...')
        exit(1)

print('Iniciando programa...')

subprocess.check_call(['flask', 'run'])
