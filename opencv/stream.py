import numpy as np
import cv2 as cv
import time
from datetime import datetime

def main():
    # define variables
    cam_port = 0
    frame_rate = 30.0
    width = 640
    height = 480
    matrix = np.array([[712.02357925, 0,            630.48055607],
                       [0,            711.26257739, 382.03460372],
                       [0,            0,            1           ]])
    distortion = np.array([[-0.43635193, 0.37668103, 0.0012934, 0.00165004, -0.4277496]])
    # open camera object
    cam = cv.VideoCapture(cam_port)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv.CAP_PROP_FPS, frame_rate)
    prev_frame_time, new_frame_time = time.time(), time.time()

    # open video writer
    out = cv.VideoWriter('output.avi', cv.VideoWriter_fourcc(*"MJPG"), frame_rate, (width, height))

    # graceful fail
    if not cam.isOpened():
        print('Cannot open camera...')
        exit()

    # main control loop
    while True:
        # obtain frame
        ret, frame = cam.read()
        if not ret:
            print('Failed to obtain frame')
            break

        # mirror flip frame
        frame = cv.flip(frame, 1)

        # calculate fps
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        # add annotations
        cv.putText(frame, 'Cam {} fps: {}'.format(cam_port, str(int(fps))), (30, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv.putText(frame, 'Time: {}'.format(datetime.now()), (30, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # save frame
        out.write(frame)

        # display frame
        cv.imshow('frame', frame)

        # escape protocol
        k = cv.waitKey(1)
        if k%256 == 27: # ESC pressed
            print('Escaping...')
            break

    # cleanup
    cam.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()
