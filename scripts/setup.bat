@ECHO OFF
ECHO "Instalando dependencias..."
ECHO "Instalando dependencias de Python..."

pip3 install -r ../requirements.txt

ECHO
ECHO "Instalando dependencias de Docker..."

python3 import-docker-image.py