#pragma once

#include <opencv2/videoio.hpp>
#include "json.hpp"

using namespace std;
using json = nlohmann::json;

class JSONWriter {
    private:
        json j;
        double fps;
        int capture_date;
        string filename;
        string format;
        string algorithm;
        string current_date;
        string tags;
        int persons;
        int max_persons;
        double duration;

        void create_json();

    public:
        JSONWriter(cv::VideoCapture *cap, string file);
        void add_to_json(TrackedObjects detections, int frame_index, int timestamp);
        void write_json_file();
        json get_json();
};