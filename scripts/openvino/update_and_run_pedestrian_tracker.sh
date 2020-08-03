#!/usr/bin/env bash

# Copyright (C) 2018-2019 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VIDEO_DIR="$PROJECT_DIR/static/videos"

. "$ROOT_DIR/utils.sh"

usage() {
    echo "Process a video using OpenVINO engine and trained models."
    echo "-i		   filename of the video to process."
    echo "-sample-options  extra parameters to pass to the program."
    echo " 	-no_show   process video on background, dont show video while processing."
    echo " 	-json      write detection results to a json file."
    echo " 	-skip      number of frames to skip. Default is 1 (no skip)."
    echo "-help            print help message"
    exit 1
}

trap 'error ${LINENO}' ERR

target="CPU"

# parse command line options
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h | -help | --help)
    usage
    ;;
    -i)
    video="$2"
    echo video = "${video}"
    ;;
    -sample-options)
    sampleoptions="$2 $3 $4 $5 $6"
    echo sample-options = "${sampleoptions}"
    shift
    ;;
    *)
    # unknown option
    ;;
esac
shift
done


target_video_path="$VIDEO_DIR/$video"

run_again="Then run the script again\n\n"
dashes="\n\n###################################################\n\n"

DISTRO="ubuntu"

apt update && apt install sudo
# sudo -E apt update
print_and_run sudo -E apt -y install build-essential python3-pip virtualenv cmake libcairo2-dev libpango1.0-dev libglib2.0-dev libgtk2.0-dev libswscale-dev libavcodec-dev libavformat-dev libgstreamer1.0-0 gstreamer1.0-plugins-base
python_binary=python3
pip_binary=pip3

system_ver=`cat /etc/lsb-release | grep -i "DISTRIB_RELEASE" | cut -d "=" -f2`
if [ $system_ver = "18.04" ]; then
sudo -E apt-get install -y libpng-dev
else
sudo -E apt-get install -y libpng12-dev
fi



if ! command -v $python_binary &>/dev/null; then
    printf "\n\nPython 3.5 (x64) or higher is not installed. It is required to run Model Optimizer, please install it. ${run_again}"
    exit 1
fi


if [ -e "$ROOT_DIR/../../bin/setupvars.sh" ]; then
    setupvars_path="$ROOT_DIR/../../bin/setupvars.sh"
else
    printf "Error: setupvars.sh is not found\n"
fi
if ! . $setupvars_path ; then
    printf "Unable to run ./setupvars.sh. Please check its presence. ${run_again}"
    exit 1
fi

# Step 1. Downloading Intel models
printf "${dashes}"
printf "Downloading Intel models\n\n"


target_precision="FP16"

printf "target_precision = ${target_precision}\n"

downloader_dir="${INTEL_OPENVINO_DIR}/deployment_tools/open_model_zoo/tools/downloader"

downloader_path="$downloader_dir/downloader.py"
models_path="$HOME/openvino_models/ir"
models_cache="$HOME/openvino_models/cache"

declare -a model_args

while read -r model_opt model_name; do
    model_subdir=$("$python_binary" "$downloader_dir/info_dumper.py" --name "$model_name" |
        "$python_binary" -c 'import sys, json; print(json.load(sys.stdin)[0]["subdirectory"])')

    model_path="$models_path/$model_subdir/$target_precision/$model_name"

    print_and_run "$python_binary" "$downloader_path" --name "$model_name" --output_dir "$models_path" --cache_dir "$models_cache"

    model_args+=("$model_opt" "${model_path}.xml")
done < "$ROOT_DIR/run_pedestrian_tracker.conf"

# Step 2. Build samples
printf "${dashes}"
printf "Build Inference Engine demos\n\n"

demos_path="${INTEL_OPENVINO_DIR}/deployment_tools/inference_engine/demos"

if ! command -v cmake &>/dev/null; then
    printf "\n\nCMAKE is not installed. It is required to build Inference Engine demos. Please install it. ${run_again}"
    exit 1
fi

OS_PATH=$(uname -m)
NUM_THREADS="-j2"

if [ $OS_PATH == "x86_64" ]; then
  OS_PATH="intel64"
  NUM_THREADS="-j8"
fi

build_dir="$HOME/inference_engine_demos_build"
if [ -e $build_dir/CMakeCache.txt ]; then
	rm -rf $build_dir/CMakeCache.txt
fi
mkdir -p $build_dir
cd $build_dir
cmake -DCMAKE_BUILD_TYPE=Release $demos_path
make $NUM_THREADS pedestrian_tracker

# Step 3. Run samples
printf "${dashes}"
printf "Run Inference Engine pedestrian_tracker\n\n"

binaries_dir="${build_dir}/${OS_PATH}/Release"
cd $binaries_dir

print_and_run ./pedestrian_tracker -i "$target_video_path" "${model_args[@]}" ${sampleoptions}

printf "${dashes}"
printf "Video processed successfully.\n\n"
