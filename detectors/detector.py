import cv2 as cv
import numpy as np
import os.path


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

        self.__net = cv.dnn.readNetFromDarknet(self.__model_cfg, self.__model_weights)
        self.__net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        self.__net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        self.__classes = None
        self.__cap = None
        self.__output_file = '_yolo_out_py'  # TODO
        self.__frame_json = {'detections': {}}

        self.__load_classes()

    def __load_classes(self):
        with open(self.__model_classes, 'rt') as f:
            self.__classes = f.read().rstrip('\n').split('\n')

    def _process(self, frame):
        self.__frame_json = {'detections': {}}

        # Create a 4D blob from a frame.
        blob = cv.dnn.blobFromImage(frame, 1 / 255, (self.input_width, self.input_height), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        self.__net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = self.__net.forward(self.__get_output_names(self.__net))

        # Remove the bounding boxes with low confidence
        self.__postprocess(frame, outs)

        self.__add_inference_time(frame)

    # Get the names of the output layers
    def __get_output_names(self, net):
        # Get the names of all the layers in the network
        layer_names = self.__net.getLayerNames()
        # Get the names of the output layers, i.e. the layers with unconnected outputs
        return [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Remove the bounding boxes with low confidence using non-maxima suppression
    def __postprocess(self, frame, outs):
        frame_height = frame.shape[0]
        frame_width = frame.shape[1]

        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.confidence_threshold:
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    width = int(detection[2] * frame_width)
                    height = int(detection[3] * frame_height)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    class_ids.append(class_id)
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
            self.__add_to_json(class_ids[i])
            self.__draw_pred(frame, class_ids[i], confidences[i], left, top, left + width, top + height)

    def __add_to_json(self, class_id):
        class_name = self.__classes[class_id]

        class_exists = self.__frame_json.get('detections').get(class_name)

        if class_exists is None:
            new_class = {class_name: 1}
            self.__frame_json.get('detections').update(new_class)
        else:
            self.__frame_json['detections'][class_name] += 1

    # Draw the predicted bounding box
    def __draw_pred(self, frame, class_id, conf, left, top, right, bottom):
        # Draw a bounding box.
        cv.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

        label = '%.2f' % conf

        # Get the label for the class name and its confidence
        if self.__classes:
            assert (class_id < len(self.__classes))
            label = '%s:%s' % (self.__classes[class_id], label)

        # Display the label at the top of the bounding box
        label_size, base_line = cv.getTextSize(label, cv.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, label_size[1])
        cv.rectangle(frame, (left, top - round(1.5 * label_size[1])),
                     (left + round(1.5 * label_size[0]), top + base_line), (255, 255, 255), cv.FILLED)
        cv.putText(frame, label, (left, top), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

    def __add_inference_time(self, frame):
        # Put efficiency information. The function getPerfProfile returns the overall time for inference(t) and the
        # timings for each of the layers(in layersTimes)
        t, _ = self.__net.getPerfProfile()
        label = 'Inference time: %.2f ms' % (t * 1000.0 / cv.getTickFrequency())
        cv.putText(frame, label, (0, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))

    def _get_json(self):
        return self.__frame_json



