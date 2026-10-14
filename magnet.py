import pygame
import random

class Magnet(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()

        # Image assets used in this game were found through Google Images and pngimg.com.
        self.image = pygame.image.load("magnet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect(x = random.randint(50, width - 50), y = -3000)

    def update(self, dt, speed):
        # make the magnet fall using delta time
        self.rect.y += round(speed * 60 * dt)

    def respawn(self, width):
        # move the magnet back above the screen
        self.rect.y = random.randint(-7000, -5000)
        self.rect.x = random.randint(50, width - 50)

    def reset(self, width):
        # reset the magnet when restart
        self.rect.y = -3000
        self.rect.x = random.randint(50, width - 50)
