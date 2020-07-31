import os
import subprocess
import docker.errors

IMAGE_NAME = 'openvinobuild'
IMAGE_PATH = os.path.join('docker', f'{IMAGE_NAME}.tar')
ENV_VARS = ['UPLOAD_FOLDER', 'MONGO_URI', 'PROJECT_DIR']

print('Instalando dependencias...')
print('Instalando dependencias de Python...')

try:
    subprocess.check_call(['pip3', 'install', '-r', 'requirements.txt'])
except subprocess.CalledProcessError as err:
    print(f'Ocurrió un error al instalar las dependencias de Python: Error {err.returncode}. Saliendo...')
    exit(err.returncode)

print('Cargando la imagen de Docker...')

# client = docker.from_env()
#
# try:
#     client.images.get(IMAGE_NAME)
# except docker.errors.ImageNotFound:
#     with open(IMAGE_PATH, 'rb') as binary_file:
#         image = client.images.load(binary_file)
#         image[0].tag(repository='pavi', tag=IMAGE_NAME)
# except IOError:
#     print(f'El archivo {IMAGE_PATH} no existe. Saliendo...')
# except docker.errors.APIError:
#     print('Ocurrió un error con Docker. Favor de checar si está corriendo correctamente en la PC. Saliendo...')
# except:
#     print('Ocurrió un error no identificado con Docker. Saliendo...')

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
