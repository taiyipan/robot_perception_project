import cv2 as cv

def main():
    cam = cv.VideoCapture(0)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
    cam.set(cv.CAP_PROP_FPS, 60)

    img_count = 0

    if not cam.isOpened():
        print('Cannot open camera...')
        exit()

    while True:
        ret, frame = cam.read()
        if not ret:
            print('Failed to obtain frame')
            break
        cv.imshow('frame', frame)

        k = cv.waitKey(1)
        if k%256 == 27: # ESC pressed
            print('Escaping...')
            break
        elif k%256 == 32: # SPACE pressed
            img_name = 'opencv_frame_{}.png'.format(img_count)
            cv.imwrite(img_name, frame)
            print('{} saved!'.format(img_name))
            img_count += 1

    cam.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
