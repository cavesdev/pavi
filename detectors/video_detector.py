from detectors.detector import YOLODetector
import cv2 as cv
import numpy as np
import os
import sys
import json
from datetime import datetime


class YOLOVideoDetector(YOLODetector):
    def __init__(self):
        super().__init__()

        self.fps = 30
        self.interval = 1
        self.__vid_writer = None
        self.__filename = None
        self.__json = {}

    def load_file(self, filename):
        if not os.path.isfile(filename):
            print("Input video file ", filename, " doesn't exist")
            sys.exit(1)
        self.__cap = cv.VideoCapture(filename)
        self.__output_file = filename[:-4] + '_yolo_out_py.avi'
        # self.fps = cv.CAP_PROP_FPS
        self.__filename = filename

        # Get the video writer initialized to save the output video
        self.__vid_writer = cv.VideoWriter(self.__output_file, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'), self.fps,
                                           (round(self.__cap.get(cv.CAP_PROP_FRAME_WIDTH)),
                                            round(self.__cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
        self.__initialize_json()

    def process(self):
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
                break

            # skip frames
            if current_frame % self.interval:
                continue

            super()._process(frame)

            self.__vid_writer.write(frame.astype(np.uint8))
            self.__update_json(current_frame)
            cv.imshow(window_name, frame)

        self.__cap.release()
        cv.destroyAllWindows()

    def __update_json(self, current_frame):
        frame_json = super()._get_json()
        seconds = current_frame / self.fps

        data = dict(frame=current_frame, seconds=seconds,objects=frame_json['detections'])

        self.__json.get('processing')[0].get('detections').append(data)

    def __initialize_json(self):
        video_date = 1
        processed_date = datetime.now().__str__()
        name, extension = os.path.splitext(self.__filename)
        tags = None
        duration = cv.CAP_PROP_FRAME_COUNT

        algorithm = dict(algorithm='YOLOv3', processed_date=processed_date, detections=[])
        video_metadata = dict(filename=name, capture_date=video_date, tags=tags, duration=duration, FPS=self.fps,
                              format=extension, processing=[algorithm])
        self.__json = video_metadata

    def write_json(self, filename):
        with open(filename, 'w') as output:
            json.dump(self.__json, output, sort_keys=True, indent=2)