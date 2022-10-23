#!/usr/bin/env bash
v4l2-ctl --list-devices
echo "ELP Cam"
v4l2-ctl --list-formats-ext -d /dev/video0
echo "Webcam"
v4l2-ctl --list-formats-ext -d /dev/video2
