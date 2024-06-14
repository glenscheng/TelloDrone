import pygame


def test():
    init()

    while True:
        if getKey("LEFT"):
            print("Left key pressed")
        if getKey("RIGHT"):
            print("Right key pressed")


def init():
    pygame.init()
    window = pygame.display.set_mode((400, 400))
    pygame.display.set_caption("Pygame Window")


def getKey(keyName):
    pressed = False
    for event in pygame.event.get():  # get events but don't do anything with them
        pass
    keyInput = pygame.key.get_pressed()  # returns list of state of all keyboard buttons
    encKeyName = getattr(pygame, 'K_{}'.format(keyName))  # equivalent to pygame.K_{}
    if keyInput[encKeyName]:
        pressed = True
    pygame.display.update()  # update window

    return pressed


if __name__ == '__main__':
    test()
