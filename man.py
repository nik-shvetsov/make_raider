import pygame
import random
from pathlib import Path
from utils import scale_img
# Constants
from constants import ENV_SPEED


class Man(pygame.sprite.Sprite):
    def __init__(self, x, y, mtype=None):
        super().__init__()
        self.man_types = self.load_images()
        if mtype is not None:
            self.image = self.man_types[mtype]
        else:
            self.image = self.man_types[random.choice(list(self.man_types.keys()))]
        self.rect = self.image.get_rect(center=(x, y))

    def load_images(self):
        return {
            'man1': scale_img(Path('pics', 'dog1.png'), 100),
            'man2': scale_img(Path('pics', 'girl1.png'), 100),
            'man3': scale_img(Path('pics', 'cat1.png'), 100),
        }

    def update(self, speed=ENV_SPEED):
        self.rect.move_ip(-speed, 0)  # Move objects to the left
    
    @classmethod
    def get_allowed_spots(cls):
        return {
            'man1': None,
            'man2': None,
            'man3': [(300, 200), (400, 200), (500, 200)],
        }
