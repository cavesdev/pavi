# Usage example:  python3 object_detection_yolo.py --video=run.mp4
#                 python3 object_detection_yolo.py --image=bird.jpg

import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
import json


class YOLODetector:

    def __init__(self, confidence=0.5, nms=0.4, width=416, height=416):
        self.confidence_threshold = confidence  # Confidence threshold
        self.nms_threshold = nms  # Non-maximum suppression threshold
        self.input_width = width  # Width of network's input image
        self.input_height = height  # Height of network's input image

        self.model_cfg = "helpers/yolov3.cfg"
        self.model_weights = "helpers/yolov3.weights"
        self.model_classes = "helpers/coco.names"

FPS = 30 # cv.CAP_PROP_FPS if available
INTERVAL = 1

parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
parser.add_argument('--image', help='Path to image file.')
parser.add_argument('--video', help='Path to video file.')
parser.add_argument('--skip-frames', type=int, dest='interval', help='Number of frames to skip', default=1)
args = parser.parse_args()

net = cv.dnn.readNetFromDarknet(model_cfg, model_weights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)


# Get the names of the output layers
def get_output_names(net):
    # Get the names of all the layers in the network
    layer_names = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawPred(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                 (255, 255, 255), cv.FILLED)
    cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confidence_threshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
    for i in indices:
        i = i[0]
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        append_to_json(classIds[i], box)
        drawPred(classIds[i], confidences[i], left, top, left + width, top + height)


def append_to_json(class_id, box):
    data = dict(class_id=int(class_id), left=int(box[0]), top=int(box[1]), width=int(box[2]), height=int(box[3]))
    json.update(data)


def write_to_json(class_id, box):
    # timestamp = cv.CAP_PROP_POS_MSEC maybe codec issue? returns 0
    timestamp = current_frame / FPS

    data = dict(frame=current_frame, timestamp=int(timestamp), class_id=int(class_id), left=int(box[0]), top=int(box[1]),
                width=int(box[2]), height=int(box[3]))
    with open('data.json', 'a') as data_dump:
        json.dump(data, data_dump)
        data_dump.write(',\n')


# Process inputs
window_name = 'Deep learning object detection in OpenCV'
cv.namedWindow(window_name, cv.WINDOW_NORMAL)
# Load names of classes
classes = None
with open(model_classes, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
if args.image:
    # Open the image file
    if not os.path.isfile(args.image):
        print("Input image file ", args.image, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.image)
    outputFileSuffix = args.image[:-4] + '_yolo_out_py.jpg'
elif args.video:
    # Open the video file
    if not os.path.isfile(args.video):
        print("Input video file ", args.video, " doesn't exist")
        sys.exit(1)
    cap = cv.VideoCapture(args.video)
    outputFileSuffix = args.video[:-4] + '_yolo_out_py.avi'

# Get the video writer initialized to save the output video
if args.video is not None:
    vid_writer = cv.VideoWriter(outputFileSuffix, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30,
                                (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
current_frame = 0
json = {}
while cv.waitKey(1) < 0:

    # get frame from the video
    has_frame, frame = cap.read()
    current_frame += 1

    # Stop the program if reached end of video
    if not has_frame:
        print("Done processing !!!")
        print("Output file is stored as ", outputFileSuffix)
        cv.waitKey(3000)
        cap.release()
        break

    if current_frame % INTERVAL:
        continue

    # Create a 4D blob from a frame.
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (input_width, input_height), [0, 0, 0], 1, crop=False)

    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(get_output_names(net))

    # Remove the bounding boxes with low confidence
    postprocess(frame, outs)

    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the
    # timings for each of the layers(in layersTimes)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    # Write the frame with the detection boxes
    if args.image:
        cv.imwrite(outputFileSuffix, frame.astype(np.uint8))
    else:
        vid_writer.write(frame.astype(np.uint8))

    cv.imshow(window_name, frame)


