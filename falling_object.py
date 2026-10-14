import pygame

# parent class for objects that fall from the top of the screen
# Fruit and bomb inherit from this class to reuse the same movement code

class FallingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, size, speed):
        super().__init__()

        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed

    def update(self, dt):
        self.rect.y += round(self.speed * 60 * dt)