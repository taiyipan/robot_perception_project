#!/usr/bin/env bash
ffmpeg -f video4linux2 -list_formats all -i /dev/video0
ffmpeg -f video4linux2 -list_formats all -i /dev/video2
