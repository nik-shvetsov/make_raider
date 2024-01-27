import pygame
from pathlib import Path
import random
from utils import scale_img

ENV_SPEED = 2
EVENTS = {
    'COLLISION': pygame.USEREVENT,
    'TIMER': pygame.USEREVENT + 1,
}

class Poop(pygame.sprite.Sprite):
    def __init__(self, seagull):
        super().__init__()
        self.image = pygame.Surface([10, 10])  # Create a surface for the rectangle
        self.image.fill((139,69,19))  # Fill the surface with a brown color
        self.rect = self.image.get_rect()
        self.rect.x = seagull.rect.centerx  # Spawn at the seagull's center x position
        self.rect.y = seagull.rect.centery  # Spawn at the seagull's center y position
        self.speed = 2  # Random speed for the poop

    def update(self):
        self.rect.y += self.speed  # Move the poop down
