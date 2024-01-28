import pygame
import random
from pathlib import Path
from utils import scale_img

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, e_type=None):
        super().__init__()
        self.enemy_state_types = self.load_images()
        self.e_type = e_type if e_type is not None else random.choice(list(self.enemy_state_types.keys()))
        self.image = self.enemy_state_types[self.e_type]['default']
        self.rect = self.image.get_rect(center=(x, y))

        self.actions_speed = {
            'stand': -1,
            'walk': 1.5,
            'run': 2
        }
    
    def switch_state(self, state):
        self.image = self.enemy_state_types[self.e_type][state]

    def load_images(self):
        return {
            'dog': {
                'default': scale_img(Path('assets', 'imgs', 'dog_state1.png'), 100),
                'poop_collide': scale_img(Path('assets', 'imgs', 'dog_state2.png'), 100),
            },
            'out_cat': {
                'default': scale_img(Path('assets', 'imgs', 'cat_state1.png'), 100),
                'actor_collide': scale_img(Path('assets', 'imgs', 'cat_state2.png'), 100),
                'poop_collide': scale_img(Path('assets', 'imgs', 'cat_state2.png'), 100),
            },
            'blond_girl': {
                'default': scale_img(Path('assets', 'imgs', 'girl_type1_w_hotdog.png'), 100),
                'poop_collide': scale_img(Path('assets', 'imgs', 'girl_type1_no_hotdog.png'), 100),
                'actor_collide': scale_img(Path('assets', 'imgs', 'girl_type1_no_hotdog.png'), 100),
            }
        }

    def update(self, action='stand'):
        # self.rect.move_ip(-speed, 0)  # Move objects to the left
        self.rect.move_ip(self.actions_speed[action], 0)
        # self.rect.move_ip(-action_speed, 0)
    
    @classmethod
    def get_allowed_spots(cls):
        return {
            'dog': None,
            'out_cat': None, # [(300, 200), (400, 200), (500, 200)],
            'blond_girl': None
        }
