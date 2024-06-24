from djitellopy import Tello
from time import sleep
import cv2
import numpy as np


fbRange = [6200, 6800]


def main():
    # Initialize Tello drone
    drone = Tello()
    drone.connect()
    print(drone.get_battery())
    drone.streamon()

    # Start drone at face level
    drone.takeoff()
    drone.send_rc_control(0, 0, 25, 0)
    sleep(2.2)

    pid = [0.4, 0.4, 0]  # proportional, integral, derivative
    pError = 0
    w, h = 360, 240

    while True:
        img = drone.get_frame_read().frame  # get frame from drone
        img = cv2. resize(img, (w, h))  # resize image
        img, faceInfo = findFace(img)
        pError = trackFace(drone, faceInfo, w, pid, pError)
        # print(faceInfo)
        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray scale
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)  # configure parameters

    # Iterate through all faces
    faceCenters = []
    faceCentersArea = []
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # make red rectangle around faces
        xCenter = x + w // 2
        yCenter = y + h // 2
        area = w * h
        cv2.circle(img, (xCenter, yCenter), 5, (0, 255, 0), cv2.FILLED)
        faceCenters.append((xCenter, yCenter))
        faceCentersArea.append(area)
    if len(faceCenters) != 0:
        # track the biggest face
        i = faceCentersArea.index(max(faceCentersArea))
        return img, [faceCenters[i], faceCentersArea[i]]
    return img, [(0, 0), 0]


def trackFace(drone, faceInfo, w, pid, prevError):
    # Set yaw speed based on center of face and center of screen
    x, y = faceInfo[0]
    if x != 0:
        error = x - w // 2
        yaw_speed = pid[0] * error + pid[1] * (error - prevError)  # change sensitivity of error
        yaw_speed = int(np.clip(yaw_speed, -100, 100))  # limit speed
    else:
        error = 0
        yaw_speed = 0

    # Set forward/backward speed based on distance of drone from face
    area = faceInfo[1]
    if fbRange[0] < area < fbRange[1]:
        fb_speed = 0
    elif area > fbRange[1]:
        fb_speed = -30
    elif area < fbRange[0] and area != 0:
        fb_speed = 30
    else:
        fb_speed = 0

    # Set drone speeds
    drone.send_rc_control(0, fb_speed, 0, yaw_speed)

    return error


if __name__ == '__main__':
    main()
