#include <opencv2/videoio.hpp>
#include "core.hpp"

#include "json.hpp"
#include "json_writer.hpp"

#include <iostream>
#include <ctime>
#include <chrono>
#include <string>
#include <fstream>

using namespace std;
using json = nlohmann::json;

JSONWriter::JSONWriter(cv::VideoCapture *cap, string file) {
    fps = cap->get(cv::CAP_PROP_FPS);
    capture_date = 1;
    
    int dot_pos = file.find_last_of('.');
    int slash_pos = file.find_last_of('/');
    filename = file.substr(slash_pos);
    format = file.substr(dot_pos + 1);

    int filename_size = filename.size() - format.size() - 2; //slash and dot
    filename = file.substr(slash_pos + 1, filename_size);

    algorithm = "OpenVINO pedestrian tracker";

    auto now = chrono::system_clock::now();
    time_t t = chrono::system_clock::to_time_t(now);
    current_date = ctime(&t);

    tags = "";
    persons = 0;
    max_persons = 0;
    

    if (0.0 == fps) {
        // the default frame rate
        fps = 30.0;
    }

    duration = cap->get(cv::CAP_PROP_FRAME_COUNT) / fps;

    create_json();
}

void JSONWriter::add_to_json(TrackedObjects detections, int frame_index, int timestamp) {
    json person, boxes, det;
    persons = 0;

    for (const auto &detection : detections) {
        persons++;

        if (detection.object_id < max_persons) {
            max_persons = detection.object_id;
        }

        boxes["x"] = detection.rect.x;
        boxes["y"] = detection.rect.y;
        boxes["width"] = detection.rect.width;
        boxes["height"] = detection.rect.height;
        person["boxes"] += boxes;
    }

    person["count"] = persons;

    det["frame"] = frame_index;
    det["seconds"] = timestamp / 1000;
    det["objects"] = { {"person", person} };

    j["processing"][0]["detections"] += det;

    return;
}

void JSONWriter::write_json_file() {
    cout << "writing..." << endl;

    ofstream jsonfile;
    jsonfile.open("/home/caves/Desktop/pavi/yolo-detection/data.json");

    if (!jsonfile.is_open()) {
        throw runtime_error("Can't open file data.json to write.\n");
        return;
    }

    jsonfile << j.dump(2, ' ', true, json::error_handler_t::ignore);
    jsonfile.close();

    return;
}

json JSONWriter::get_json() {
    return j;
}

void JSONWriter::create_json() {
    json p;

    p["algorithm"] = algorithm;
    p["processed_date"] = current_date;
    p["detections"] = json::array();

    j["FPS"] = fps;
    j["capture_date"] = capture_date;
    j["duration"] = duration;
    j["filename"] = filename;
    j["format"] = format;
    j["tags"] = tags;
    j["processing"] = { p };

    return;
}