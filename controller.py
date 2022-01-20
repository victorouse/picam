import os
import argparse
import signal
import time
import sys

from multiprocessing import Manager
from multiprocessing import Process
from imutils.video import VideoStream

from tracker.detector import Detector
from tracker.pid import PID

from gpiozero import AngularServo
import cv2


os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

servoRange = (-90, 90)

# left: 90 / right: -90
panServo = AngularServo("BCM2", min_angle=servoRange[0], max_angle=servoRange[1])

# up: -90 / down: 90
tiltServo = AngularServo("BCM3", min_angle=servoRange[0], max_angle=servoRange[1], initial_angle=-45.0)

# function to handle keyboard interrupt
def signal_handler(sig, frame):
    print("[INFO] You pressed `ctrl + c`! Exiting...")

    panServo.close()
    tiltServo.close()

    sys.exit()

def obj_center(args, objX, objY, centerX, centerY):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # start the video stream and wait for the camera to warm up
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    obj = Detector(args["cascade"])

    while True:
        # grab the frame from the threaded video stream 
        frame = vs.read()

        # calculate the center of the frame
        (H, W) = frame.shape[:2]
        centerX.value = W // 2
        centerY.value = H // 2

        # find the object's location
        objectLoc = obj.update(frame, (centerX.value, centerY.value))
        ((objX.value, objY.value), rect) = objectLoc

        # extract the bounding box and draw it
        if rect is not None:
            (x, y, w, h) = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # display the frame to the screen
        cv2.imshow("Pan-Tilt Face Tracking", frame)
        cv2.waitKey(1)

def pid_process(output, p, i, d, objCoord, centerCoord):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # create a PID and initialize it
    p = PID(p.value, i.value, d.value)
    p.initialize()

    # loop indefinitely
    while True:
        # calculate the error
        error = centerCoord.value - objCoord.value

        # update the value
        output.value = p.update(error)

def in_range(val, start, end):
	# determine the input value is in the supplied range
	return (val >= start and val <= end)

def set_servos(p, t):
    # signal trap to handle keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)

    # loop indefinitely
    while True:
        # the pan and tilt angles are reversed
        panAngle = p.value
        tiltAngle = -1 * t.value

        # if the pan angle is within the range, pan
        if in_range(panAngle, servoRange[0], servoRange[1]):
            # print("panning: " + str(p.value))
            panServo.angle = panAngle
            # time.sleep(1)

        # if the tilt angle is within the range, tilt
        if in_range(tiltAngle, servoRange[0], servoRange[1]):
            # print("tilting: " + str(t.value))
            tiltServo.angle = tiltAngle
            # time.sleep(1)

if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", type=str, required=True, help="path to input Haar cascade for face detection")
    args = vars(ap.parse_args())

    # start a manager for managing process-safe variables
    with Manager() as manager:
        # set integer values for the object center (x, y)-coordinates
        centerX = manager.Value("i", 0)
        centerY = manager.Value("i", 0)

        # set integer values for the object's (x, y)-coordinates
        objX = manager.Value("i", 0)
        objY = manager.Value("i", 0)

        # pan and tilt values will be managed by independed PIDs
        pan = manager.Value("i", -45)
        tilt = manager.Value("i", 0)

        # set PID values for panning
        panP = manager.Value("f", 0.15)
        panI = manager.Value("f", 0.0008)
        panD = manager.Value("f", 0.00006)


        # set PID values for tilting
        tiltP = manager.Value("f", 0.15)
        tiltI = manager.Value("f", 0.0008)
        tiltD = manager.Value("f", 0.00006)

        # we have 4 independent processes
        # 1. objectCenter  - finds/localizes the object
        # 2. panning       - PID control loop determines panning angle
        # 3. tilting       - PID control loop determines tilting angle
        # 4. setServos     - drives the servos to proper angles based
        #                    on PID feedback to keep object in center
        processObjectCenter = Process(target=obj_center,
            args=(args, objX, objY, centerX, centerY))
        processPanning = Process(target=pid_process,
            args=(pan, panP, panI, panD, objX, centerX))
        processTilting = Process(target=pid_process,
            args=(tilt, tiltP, tiltI, tiltD, objY, centerY))
        processSetServos = Process(target=set_servos, args=(pan, tilt))

        # start all 4 processes
        processObjectCenter.start()
        processPanning.start()
        processTilting.start()
        processSetServos.start()

        # join all 4 processes
        processObjectCenter.join()
        processPanning.join()
        processTilting.join()
        processSetServos.join()

        # disable the servos
        panServo.close()
        tiltServo.close()
