import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

from openvino.inference_engine import IECore
from pavi.config import Config
from pavi.util.omz_utils import download_model, convert_model

MODEL_NAME = 'yolo-v4-tiny-tf'
DOWNLOAD_PATH = os.path.join(Config.get('static_folder'), 'raw_models')
CONVERT_PATH = os.path.join(Config.get('static_folder'), 'models')

print('Downloading model...')
download_model(MODEL_NAME, DOWNLOAD_PATH)
print('Converting model...')
converted_path = convert_model(MODEL_NAME, DOWNLOAD_PATH, CONVERT_PATH)

model_xml = os.path.join(converted_path, 'FP32', MODEL_NAME + '.xml')

# Initialize Inference Engine
ie = IECore()

# get available devices
devices = ie.available_devices
for device in devices:
    device_name = ie.get_metric(device, "FULL_DEVICE_NAME")
    print(f"{device}: {device_name}")

net = ie.read_network(model=model_xml)
exec_net = ie.load_network(network=net, device_name="CPU")

input_layer = next(iter(net.input_info))
print(f"input layout: {net.input_info[input_layer].layout}")
print(f"input precision: {net.input_info[input_layer].precision}")
print(f"input shape: {net.input_info[input_layer].tensor_desc.dims}")

output_layer = next(iter(net.outputs))
print(f"output layout: {net.outputs[output_layer].layout}")
print(f"output precision: {net.outputs[output_layer].precision}")
print(f"output shape: {net.outputs[output_layer].shape}")

cap = cv2.VideoCapture('one-by-one-person-detection.mp4')
# N,C,H,W = batch size, number of channels, height, width
# N, C, H, W = net.input_info[input_layer].tensor_desc.dims
N, C, H, W = net.input_info[input_layer].input_data.shape

# track frame count and set maximum
frame_num = 0
max_frame_num = 1000
skip_num_frames = 100
last_frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
if last_frame_num < 1: last_frame_num = "unknown"

while cap.isOpened():
    ret, image = cap.read()

    if not ret:
        break

    frame_num += 1

    # skip skip_num_frames of frames, then infer max_frame_num frames from there
    if frame_num > skip_num_frames:
        # infer image
        # OpenCV resize expects the destination size as (width, height)
        resized_image = cv2.resize(src=image, dsize=(W, H))
        # print(resized_image.shape)
        input_data = np.expand_dims(np.transpose(resized_image, (2, 0, 1)), 0).astype(np.float32)
        # print(input_data.shape)

        result = exec_net.infer({input_layer: input_data})
        output = result[output_layer]

        # display results
        # convert colors BGR -> RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # show image then force re-draw to show new image
        plt.imshow(image)
        plt.gcf().canvas.draw()

    # display current frame number
    print("Frame #:", frame_num, "/", last_frame_num, end="\r")

    # limit number of frames, video can be slow and gets slower the more frames that are processed
    if frame_num >= (max_frame_num + skip_num_frames):
        print("\nStopping at frame #", frame_num)
        break

