from djitellopy import Tello
from time import sleep
import cv2
import numpy as np


fb_range = [6200, 6800]


def main():
    # Initialize Tello drone
    drone = Tello()
    drone.connect()
    print(drone.get_battery())
    drone.streamon()

    # Start drone at face level
    drone.takeoff()
    drone.send_rc_control(0, 0, 25, 0)
    sleep(2.5)

    pid = [0.4, 0.4, 0]  # proportional, integral, derivative
    yaw_prev_error = 0
    ud_prev_error = 0
    w, h = 360, 240 # window size

    while True:
        img = drone.get_frame_read().frame  # get frame from drone
        img = cv2. resize(img, (w, h))  # resize image
        img, face_info = findFace(img)
        yaw_prev_error, ud_prev_error = trackFace(drone, face_info, w, h, pid, yaw_prev_error, ud_prev_error)
        # print(face_info)
        cv2.imshow("Output", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            drone.land()
            break


def findFace(img):
    face_cascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to gray scale
    faces = face_cascade.detectMultiScale(img_gray, 1.1, 6)  # configure parameters

    # Iterate through all faces
    face_centers = []
    face_centers_area = []
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # make red rectangle around faces
        x_center = x + w // 2
        y_center = y + h // 2
        area = w * h
        cv2.circle(img, (x_center, y_center), 5, (0, 255, 0), cv2.FILLED)
        face_centers.append((x_center, y_center))
        face_centers_area.append(area)
    if len(face_centers) != 0:
        # track the biggest face
        i = face_centers_area.index(max(face_centers_area))
        return img, [face_centers[i], face_centers_area[i]]
    return img, [(0, 0), 0]


def trackFace(drone, face_info, w, h, pid, prev_yaw_error, prev_ud_error):
    x, y = face_info[0]

    # Set yaw speed based on center of face and center of screen
    if x != 0:
        yaw_error = x - w // 2
        yaw_speed = pid[0] * yaw_error + pid[1] * (yaw_error - prev_yaw_error)  # change sensitivity of error
        yaw_speed = int(np.clip(yaw_speed, -100, 100))  # limit speed
    else:
        yaw_error = 0
        yaw_speed = 0
        
    # Set up/down speed based on center of face and center of screen
    if y != 0:
        ud_error = y - h // 2
        ud_speed = pid[0] * ud_error + pid[1] * (ud_error - prev_ud_error)  # change sensitivity of error
        ud_speed = int(np.clip(ud_speed, -30, 30))  # limit speed
    else:
        ud_error = 0
        ud_speed = 0

    # Set forward/backward speed based on distance of drone from face
    area = face_info[1]
    if fb_range[0] < area < fb_range[1]:
        fb_speed = 0
    elif area > fb_range[1]:
        fb_speed = -20
    elif area < fb_range[0] and area != 0:
        fb_speed = 20
    else:
        fb_speed = 0

    # Set drone speeds
    drone.send_rc_control(0, fb_speed, -ud_speed, yaw_speed)

    print("fb: {}, -ud: {}, yaw: {}".format(fb_speed, -ud_speed, yaw_speed))
    
    return yaw_error, ud_error


if __name__ == '__main__':
    main()
