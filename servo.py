import os
import time
import getch
import cv2
from multiprocessing import Process
from gpiozero import AngularServo
from picamera.array import PiRGBArray
from picamera import PiCamera

# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 32
# rawCapture = PiRGBArray(camera, size=(640, 480))
# time.sleep(0.1)

# left: 90 / right: -90
panServo = AngularServo("BCM2")

# up: -90 / down: 90
tiltServo = AngularServo("BCM3")

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


def clamp(minV, maxV, val):
    return max(min(val, maxV), minV)

def controls():
    AMOUNT = 1

    while True:
        key = getch.getch()

        if key == 'w':
            tiltServo.angle = clamp(-90, 90, tiltServo.angle - AMOUNT)

        if key == 'a':
            panServo.angle = clamp(-90, 90, panServo.angle - AMOUNT)

        if key == 's':
            tiltServo.angle = clamp(-90, 90, tiltServo.angle + AMOUNT)

        if key == 'd':
            panServo.angle = clamp(-90, 90, panServo.angle + AMOUNT)

        if key == 'q':
            break

def capture():
    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    # cap = cv2.VideoCapture("rtsp://raspberrypi.local:8554/stream", cv2.CAP_FFMPEG)
    # ret, frame = cap.read()
    # while ret:
    #     cv2.imshow("frame", frame) 
    #     ret, frame = cap.read()

    #     key = cv2.waitKey(1) & 0xFF

    #     if key == ord("q"):
    #         break

if __name__ == "__main__":
    processControls = Process(target=controls)
    processControls.start()

    capture()

    panServo.close()
    tiltServo.close()
