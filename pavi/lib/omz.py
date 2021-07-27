import os
import subprocess


def download_model(model_name, download_path):
    model_path = os.path.join(download_path, 'public', model_name)

    if not os.path.exists(model_path):
        subprocess.check_output(['omz_downloader', '--name', model_name, '-o', download_path])


def convert_model(model_name, model_path, convert_path):
    converted_path = os.path.join(convert_path, 'public', model_name)

    if not os.path.exists(converted_path):
        subprocess.check_output(['omz_converter', '--name', model_name, '-d', model_path, '-o', convert_path])

    return converted_path


def download_and_convert_model(model_name, download_path, convert_path):

    download_model(model_name, download_path)
    converted_path = convert_model(model_name, download_path, convert_path)

    return converted_path

