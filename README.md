# yolo-detection
Python script using YOLOv3 algorithm and OpenCV to detect objects in images and video. 

To get the helper files use the following commands:

```shell script
wget https://pjreddie.com/media/files/yolov3.weights
wget https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg\?raw=true -O yolov3.cfg
wget https://github.com/pjreddie/darknet/blob/master/data/coco.names\?raw=true -O coco.names
```

To import the detectors:
```python
from detectors import YOLOVideoDetector
from detectors import YOLOImageDetector
```

The general process is:
```python
d = YOLOVideoDetector()
d.load_file('filename.mp4')
d.interval = 30  # optional: set the number of frames to skip.
d.process()
d.write_json('filename.json') # optional: write the detection results to a JSON file.
```

Based from: 
https://github.com/spmallick/learnopencv/tree/master/ObjectDetection-YOLO