from djitellopy import Tello
import cv2


def main():
    # Create tello object
    drone = Tello()
    # Connect to drone through Wi-Fi
    drone.connect()

    printBattery(drone)

    runCamera(drone)


def printBattery(drone):
    print(drone.get_battery())


def runCamera(drone):
    drone.stream_on()

    while True:
        image = drone.get_frame_read().frame         # get frame from drone
        image = cv2.resize(image, (360, 240))  # resize image
        cv2.imshow("Video Stream", image)   # create window to display image
        cv2.waitKey(1)                               # delay 1ms


if __name__ == '__main__':
    main()
