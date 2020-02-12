from detector import YOLODetector
import cv2 as cv
import numpy as np
import os
import sys


class YOLOImageDetector(YOLODetector):
    def __init__(self):
        super().__init__()

    def load_file(self, filename):
        if not os.path.isfile(filename):
            print("Input image file ", filename, " doesn't exist")
            sys.exit(1)
        self.__cap = cv.VideoCapture(filename)
        self.__output_file = filename[:-4] + '_yolo_out_py.jpg'

    def process(self):
        _, frame = self.__cap.read()

        super().process(frame)

        cv.imwrite(self.__output_file, frame.astype(np.uint8))
        window_name = 'Deep learning object detection in OpenCV'
        cv.imshow(window_name, frame)
        print("Done processing !!!")
        print("Output file is stored as ", self.__output_file)
        cv.waitKey(5000)

