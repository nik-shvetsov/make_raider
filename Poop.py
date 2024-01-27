import pygame
from pathlib import Path
from utils import scale_img

ENV_SPEED = 2
EVENTS = {
    'COLLISION': pygame.USEREVENT,
    'TIMER': pygame.USEREVENT + 1,
}

class Poop(pygame.sprite.Sprite):
    def __init__(self, seagull):
        super().__init__()
        self.image = scale_img(Path('assets', 'shit.png'), 50)
        self.rect = self.image.get_rect()
        self.rect.x = seagull.rect.centerx  # Spawn at the seagull's center x position
        self.rect.y = seagull.rect.centery  # Spawn at the seagull's center y position
        self.speed = 2  # Random speed for the poop
        self.speed = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.1)

    def update(self):
        self.speed += self.acceleration
        self.rect.move_ip(self.speed)
         # Move the poop down
    
