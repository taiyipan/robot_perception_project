#!/usr/bin/env bash
cam1_port=0;
cam2_port=2;
width=640;
height=480;
fps=10;
queue_size=1024;
ffmpeg -f v4l2 \
       -input_format mjpeg \
       -video_size ${width}x${height} \
       -thread_queue_size ${queue_size} \
       -i /dev/video${cam1_port} \
       -f v4l2 \
       -input_format mjpeg \
       -video_size ${width}x${height} \
       -thread_queue_size ${queue_size} \
       -i /dev/video${cam2_port} \
       -c:v libx264 -r ${fps} -map 0 output_cam${cam1_port}_$(date +"%Y-%m-%d_%H:%M:%S").mkv \
       -c:v libx264 -r ${fps} -map 1 output_cam${cam2_port}_$(date +"%Y-%m-%d_%H:%M:%S").mkv
