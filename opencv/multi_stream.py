import traceback
import numpy as np
import cv2 as cv
import time
from datetime import datetime
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, wait

# define global variables
cam_port = 0
cam_port_2 = 2
frame_rate = 30.0
width = 640
height = 480

# instantiate and return a VideoCapture object as camera handle
def open_cam(port: int):
    camera = cv.VideoCapture(port)
    camera.set(cv.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    camera.set(cv.CAP_PROP_FPS, frame_rate)
    return camera

# frame capture: a blocking operation for a single thread
def generate_frame(cam_obj, cam_port, prev_frame_time):
    # obtain frame
    ret, cam_frame = cam_obj.read()
    # mirror flip frame
    cam_frame = cv.flip(cam_frame, 1)
    # calculate fps
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    # add annotations
    cv.putText(cam_frame, 'Cam {} fps: {}'.format(cam_port, str(int(fps))), (30, 30), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv.putText(cam_frame, 'Time: {}'.format(datetime.now()), (30, 50), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    return ret, cam_frame, new_frame_time

def main():
    try:
        # define multithreaded program executor
        executor = ThreadPoolExecutor()

        # open camera objects
        cam = open_cam(cam_port)
        cam2 = open_cam(cam_port_2)

        # open video writer objects
        out = cv.VideoWriter('output_cam_{}.avi'.format(cam_port), cv.VideoWriter_fourcc(*"MJPG"), frame_rate, (width, height))
        out2 = cv.VideoWriter('output_cam_{}.avi'.format(cam_port_2), cv.VideoWriter_fourcc(*"MJPG"), frame_rate, (width, height))

        # graceful fail scenarios
        if not cam.isOpened():
            print('Cannot open camera...')
            exit()
        elif not cam2.isOpened():
            print('Cannot open camera...')
            exit()

        # time step 0
        prev_frame_time_cam1, prev_frame_time_cam2 = time.time(), time.time()

        # main control loop
        while True:
            # obtain frames asynchronously (via concurrent.futures.ThreadPoolExecutor)
            futures = list()
            futures.append(executor.submit(generate_frame, cam, 0, prev_frame_time_cam1)) # submit task 1
            futures.append(executor.submit(generate_frame, cam2, 2, prev_frame_time_cam2)) # submit task 2
            wait(futures, return_when = concurrent.futures.ALL_COMPLETED) # wait for concurrent execution
            ret1, frame1, prev_frame_time_cam1 = futures[0].result() # obtain task 1 output
            ret2, frame2, prev_frame_time_cam2 = futures[1].result() # obtain task 2 output

            # display and save frames
            if (ret1):
                cv.imshow('frame1', frame1)
                out.write(frame1)
            if (ret2):
                cv.imshow('frame2', frame2)
                out2.write(frame2)

            # escape protocol
            k = cv.waitKey(1)
            if k%256 == 27: # ESC pressed
                print('Escaping...')
                break
    except:
        # print traceback to console
        traceback.print_exc()

    finally:
        # release memory resources
        cam.release()
        cam2.release()
        out.release()
        out2.release()
        cv.destroyAllWindows()
        executor.shutdown()

if __name__ == '__main__':
    main()
