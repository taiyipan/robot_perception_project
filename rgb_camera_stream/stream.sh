ffmpeg -f v4l2 \
       -input_format mjpeg \
       -video_size 640x480 \
       -i /dev/video0 \
       -f v4l2 \
       -input_format mjpeg \
       -video_size 640x480 \
       -i /dev/video2 \
       -c:v copy -map 0 output_0.mkv \
       -c:v copy -map 1 output_2.mkv
