from djitellopy import Tello
from time import sleep


def main():
    # Create tello object
    drone = Tello()

    # Connect to drone through Wi-Fi
    drone.connect()

    printBattery(drone)

    move(drone)


def printBattery(drone):
    print(drone.get_battery())


def move(drone):
    # Move
    drone.takeoff()
    sleep(1.5)
    drone.send_rc_control(0, 100, 0, 0)  # forward
    sleep(1.5)
    drone.send_rc_control(100, 0, 0, 0)  # right
    sleep(1.5)
    drone.send_rc_control(0, 0, 0, 0)
    drone.land()


if __name__ == '__main__':
    main()
