#!/bin/bash

echo "Instalando dependencias..."
echo "Instalando dependencias de Python..."

pip3 install -r ../requirements.txt

echo
echo "Instalando dependencias de Docker..."

python3 import-docker-image.py