from djitellopy import Tello
from time import sleep


def printBattery():
    # Create tello object
    drone = Tello()
    sleep(3)
    # Connect to drone through Wi-Fi
    drone.connect()

    print(drone.get_battery())

    # Move
    drone.takeoff()
    drone.send_rc_control(0, 100, 0, 0) # forward
    sleep(1.5)
    drone.send_rc_control(100, 0, 0, 0) # right
    sleep(1.5)
    drone.send_rc_control(0, 0, 0, 0)
    drone.land()


if __name__ == '__main__':
    printBattery()
