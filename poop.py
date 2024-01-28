import pygame
from pathlib import Path
from utils import scale_img

class Poop(pygame.sprite.Sprite):
    def __init__(self, seagull):
        super().__init__()
        self.image = scale_img(Path('assets', 'imgs', 'poop_default.png'), 40)
        self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = seagull.rect.centerx, seagull.rect.centery
        self.rect.x = seagull.rect.left + seagull.rect.width * 0.2
        self.rect.y = seagull.rect.bottom - seagull.rect.height * 0.2
        self.speed = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.1)

    def update(self):
        self.speed += self.acceleration
        self.rect.move_ip(self.speed)    
