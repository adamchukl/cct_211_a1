import pygame

WIDTH = 800
HEIGHT = 600

class Basket(pygame.sprite.Sprite):
    # this class represent the basket controlled by the player

    def __init__(self, x, y, speed=700):
        super().__init__()

        self.image = pygame.image.load("basket.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 70))

        self.rect = self.image.get_rect(center=(x,y))

        self.speed = speed

    def update(self, dt):
        # update the basket position using keyboard
        # delta time helps keep movement consistent at different time rates
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= round(self.speed * dt)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += round(self.speed * dt)

        # keep the basket inside the screen
        self.rect.clamp_ip(pygame.Rect(0,0, WIDTH, HEIGHT))