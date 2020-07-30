import docker

client = docker.from_env()

try:
    client.api.import_image_from_file('../docker/openvinobuild.tar', repository='pavi', tag='openvinobuild')
except IOError:
    print('El archivo /docker/openvinobuild.tar no existe. Saliendo...')