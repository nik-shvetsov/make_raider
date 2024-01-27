import pygame
from pathlib import Path
import random
from utils import scale_img

ENV_SPEED = 2
EVENTS = {
    'COLLISION': pygame.USEREVENT,
    'TIMER': pygame.USEREVENT + 1,
}

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
            'man1': scale_img(Path('assets', 'obj_man_1.png'), 100),
            'man2': scale_img(Path('assets', 'obj_man_2.png'), 100),
            'man3': scale_img(Path('assets', 'obj_man_3.png'), 100),
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
