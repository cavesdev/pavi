"""
YOLOv4 service script.
This script does the preprocessing needed to run inference using the YOLOv4 algorithm in OpenVINO.

Author: Carlos Cuevas Sosa (@cavesdev)
05/08/21
"""

import logging
import os
import sys
import argparse

from pavi.config import Config
from pavi.lib.omz import download_and_convert_model
from pavi.algorithms import yolov4

parser = argparse.ArgumentParser(description='YOLOv4 service script')
parser.add_argument('input', type=str, help="Path to the video file to process.")
args = parser.parse_args()

MODEL_NAME = 'yolo-v4-tiny-tf'
DOWNLOAD_PATH = os.path.join(Config.get('static_folder'), 'raw_models')
CONVERT_PATH = os.path.join(Config.get('static_folder'), 'models')
PRECISION = 'FP32'

logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
log = logging.getLogger()

log.info('Downloading and converting model...')
converted_path = download_and_convert_model(MODEL_NAME, DOWNLOAD_PATH, CONVERT_PATH)
model_xml = os.path.join(converted_path, PRECISION, MODEL_NAME + '.xml')

yolov4(args.input, model_xml, no_show=True)