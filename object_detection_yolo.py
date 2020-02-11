# Usage example:  python3 object_detection_yolo.py --video=run.mp4
#                 python3 object_detection_yolo.py --image=bird.jpg

import cv2 as cv
import argparse
import sys
import numpy as np
import os.path
import json

#TODO
def parse_arguments():
    parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
    parser.add_argument('--image', help='Path to image file.')
    parser.add_argument('--video', help='Path to video file.')
    parser.add_argument('--skip-frames', type=int, dest='interval', help='Number of frames to skip', default=1)
    args = parser.parse_args()


# Get the names of the output layers
def get_output_names(net):
    # Get the names of all the layers in the network
    layer_names = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def add_inference_time(net, frame):
    # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the
    # timings for each of the layers(in layersTimes)
    t, _ = net.getPerfProfile()
    label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
    cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))


def append_to_json(class_id, box):
    data = dict(class_id=int(class_id), left=int(box[0]), top=int(box[1]), width=int(box[2]), height=int(box[3]))
    json.update(data)


def write_to_json(class_id, box):
    # timestamp = cv.CAP_PROP_POS_MSEC maybe codec issue? returns 0
    timestamp = current_frame / FPS

    data = dict(frame=current_frame, timestamp=int(timestamp), class_id=int(class_id), left=int(box[0]),
                top=int(box[1]),
                width=int(box[2]), height=int(box[3]))
    with open('data.json', 'a') as data_dump:
        json.dump(data, data_dump)
        data_dump.write(',\n')


class YOLODetector:

    def __init__(
            self,
            confidence_threshold=0.5,
            nms_threshold=0.4,
            input_width=416,
            input_height=416,
            helpers_path='helpers'
    ):
        self.confidence_threshold = confidence_threshold  # Confidence threshold
        self.nms_threshold = nms_threshold  # Non-maximum suppression threshold
        self.input_width = input_width  # Width of network's input image
        self.input_height = input_height  # Height of network's input image

        # TODO set better way to deal with these files
        self.__model_cfg = os.path.join(helpers_path, 'yolov3.cfg')
        self.__model_weights = os.path.join(helpers_path, 'yolov3.weights')
        self.__model_classes = os.path.join(helpers_path, 'coco.names')

        self.__fps = 30
        self.__interval = 1

        self.__net = cv.dnn.readNetFromDarknet(self.__model_cfg, self.__model_weights) # TODO
        self.__net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.__net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        self.__classes = None
        self.__cap = None
        self.__vid_writer = None
        self.__output_file = '_yolo_out_py' #TODO

    def load_file(self, file, image=False, video=False):
        if image:
            self.__load_image(file)
            image = False
        elif video:
            self.__load_video(file)
            video = False
        else:
            print('Please provide a valid file type.')
            sys.exit(1)

    def __load_classes(self):
        with open(self.__model_classes, 'rt') as f:
            self.__classes = f.read().rstrip('\n').split('\n')

    def __load_image(self, filename):
        if not os.path.isfile(filename):
            print("Input image file ", filename, " doesn't exist")
            sys.exit(1)
        self.__cap = cv.VideoCapture(filename)
        self.__output_file = filename[:-4] + '_yolo_out_py.jpg'
        self.__vid_writer = None

    def __load_video(self, filename):
        if not os.path.isfile(filename):
            print("Input video file ", filename, " doesn't exist")
            sys.exit(1)
        self.__cap = cv.VideoCapture(filename)
        self.__output_file = filename[:-4] + '_yolo_out_py.avi'
        self.fps = 30 # cv.CAP_PROP_FPS if available TODO

        # Get the video writer initialized to save the output video
        self.__vid_writer = cv.VideoWriter(self.__output_file, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.__fps,
                                           (round(self.__cap.get(cv.CAP_PROP_FRAME_WIDTH)),
                                            round(self.__cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

    def __write_frame(self, frame):
        # Write the frame with the detection boxes
        if self.__vid_writer is None:
            cv.imwrite(self.__output_file, frame.astype(np.uint8))
        else:
            self.__vid_writer.write(frame.astype(np.uint8))

    # Remove the bounding boxes with low confidence using non-maxima suppression
    def postprocess(self, frame, outs):
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
                if confidence > self.confidence_threshold:
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
        indices = cv.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, self.nms_threshold)
        for i in indices:
            i = i[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            # append_to_json(classIds[i], box)
            self.draw_pred(frame, classIds[i], confidences[i], left, top, left + width, top + height)

    # Draw the predicted bounding box
    def draw_pred(self, frame, class_id, conf, left, top, right, bottom):
        # Draw a bounding box.
        cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

        label = '%.2f' % conf

        # Get the label for the class name and its confidence
        if self.__classes:
            assert (class_id < len(self.__classes))
            label = '%s:%s' % (self.__classes[class_id], label)

        # Display the label at the top of the bounding box
        labelSize, baseLine = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv.rectangle(frame, (left, top - round(1.5 * labelSize[1])), (left + round(1.5 * labelSize[0]), top + baseLine),
                     (255, 255, 255), cv.FILLED)
        cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

    def process(self):
        # Process inputs
        window_name = 'Deep learning object detection in OpenCV'
        cv.namedWindow(window_name, cv.WINDOW_NORMAL)

        current_frame = 0

        while cv.waitKey(1) < 0:

            # get frame from the video
            has_frame, frame = self.__cap.read()
            current_frame += 1

            # Stop the program if reached end of video
            if not has_frame:
                print("Done processing !!!")
                print("Output file is stored as ", self.__output_file)
                cv.waitKey(3000)
                self.__cap.release()
                break

            # skip frames
            if current_frame % self.__interval:
                continue

            # Create a 4D blob from a frame.
            blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.input_width, self.input_height), [0, 0, 0], 1, crop=False)

            # Sets the input to the network
            self.__net.setInput(blob)

            # Runs the forward pass to get output of the output layers
            outs = self.__net.forward(get_output_names(self.__net))

            # Remove the bounding boxes with low confidence
            self.postprocess(frame, outs)

            add_inference_time(self.__net, frame)

            self.__write_frame(frame)

            cv.imshow(window_name, frame)


if __name__ == '__main__':
    detector = YOLODetector()
    detector.load_file('content/bird.jpg', image=True)
    detector.process()

