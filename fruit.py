from falling_object import FallingObject

# Child class of FallingObject
# Inherit the image loading and falling movement from the parent class
# It is used for all fruits
class Fruit(FallingObject):
    def __init__(self, x, y, image, speed=3):
        super().__init__(x, y, image, (50, 50), speed)