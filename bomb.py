from falling_object import FallingObject

# Child class of fallingObject
# Unlike fruit, it catching a bomb causes the player to lose a life
class Bomb(FallingObject):
    def __init__(self, x, y, speed=4):
        super().__init__(x, y, "bomb.png", (60, 60), speed)