from djitellopy import tello
from time import sleep
import KeyPressModule as kp


def main():
    # Initialization
    drone = tello.Tello()
    drone.connect()
    print(drone.get_battery())
    kp.init()

    while True:
        vel = getKeyboardInput(drone)
        drone.send_rc_control(vel[0], vel[1], vel[2], vel[3])
        sleep(0.05)


# Get movement depending on key presses
def getKeyboardInput(drone):
    lr = 0  # left right velocity
    fb = 0  # forward backward velocity
    ud = 0  # up down velocity
    yaw = 0  # yaw velocity
    speed = 50

    # Start and stop
    if kp.getKey("e"):
        drone.takeoff()

    if kp.getKey("q"):
        drone.land()

    # Movement
    if kp.getKey("a"):
        lr = -speed
    elif kp.getKey("d"):
        lr = speed

    if kp.getKey("w"):
        fb = speed
    elif kp.getKey("s"):
        fb = -speed

    if kp.getKey("UP"):
        ud = speed
    elif kp.getKey("DOWN"):
        ud = -speed

    if kp.getKey("RIGHT"):
        yaw = speed
    elif kp.getKey("LEFT"):
        yaw = -speed

    return [lr, fb, ud, yaw]


if __name__ == '__main__':
    main()
