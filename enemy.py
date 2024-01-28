import pygame
import random
from pathlib import Path
from utils import scale_img
import sys
import os

# Check if we're running in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # If we are, set the base directory to the directory containing the .exe file
    base_dir = sys._MEIPASS
else:
    # Otherwise, set it to the current directory
    base_dir = os.path.dirname(__file__)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, e_type=None):
        super().__init__()
        self.e_type = e_type if e_type is not None else random.choice(list(self.get_allowed_xy.keys()))
        self.state_imgs = self.load_images(self.e_type)
        self.image = self.state_imgs['default']
        self.rect = self.image.get_rect(center=(x, y))
        self.collided = False

        ### bbox scaling
        # scale_factor = 0.1
        # self.rect.width *= scale_factor
        # self.rect.height *= scale_factor

        # self.scaling_factor = {
        #     'dog': 2,
        #     'outcat': 1,
        #     'blond_girl': 0.1,
        #     'red_girl': 0.1,
        #     'can': 1,
        # }

        # self.rect.width *= self.scaling_factor[self.e_type]
        # self.rect.height *= self.scaling_factor[self.e_type]


        self.actions_speed = {
            'stand': -1,
            'walk': 1.5,
            'run': 2
        }
    
    def switch_state(self, state):
        self.image = self.state_imgs[state]

    def load_images(self, e_type):
        if e_type == 'dog': 
            return {
                'default': scale_img(Path(base_dir, 'assets', 'imgs', 'dog_default.png'), 140),
                'poop_collide': scale_img(Path(base_dir, 'assets', 'imgs', 'dog_poop.png'), 140),
                'actor_collide': scale_img(Path(base_dir, 'assets', 'imgs', 'dog_bite.png'), 300)
            }
        elif e_type == 'outcat':
            return {
                'default': scale_img(Path(base_dir, 'assets', 'imgs', 'outcat_default.png'), 110),
                'poop_collide': scale_img(Path(base_dir, 'assets', 'imgs', 'outcat_angry.png'), 200),
                'actor_collide': scale_img(Path(base_dir, 'assets', 'imgs', 'outcat_angry.png'), 200),
            }
        elif e_type == 'blond_girl':
            return {
                'default': scale_img(Path(base_dir, 'assets', 'imgs', 'blondgirl_default.png'), 160),
                'poop_collide': random.choice([
                    scale_img(Path(base_dir, 'assets', 'imgs', 'blondgirl_poop1.png'), 160),
                    scale_img(Path(base_dir, 'assets', 'imgs', 'blondgirl_poop2.png'), 170),
                ]),
                'actor_collide': random.choice([
                    scale_img(Path(base_dir, 'assets', 'imgs', 'blondgirl_angry1.png'), 160),
                    scale_img(Path(base_dir, 'assets', 'imgs', 'blondgirl_angry2.png'), 160),
                ]),
            }
        elif e_type == 'red_girl':
            return {
                'default': scale_img(Path(base_dir, 'assets', 'imgs', 'redgirl_default.png'), 160),
                'poop_collide': random.choice([
                    scale_img(Path(base_dir, 'assets', 'imgs', 'redgirl_poop1.png'), 160),
                    scale_img(Path(base_dir, 'assets', 'imgs', 'redgirl_poop2.png'), 160),
                ]),
                'actor_collide': random.choice([
                    scale_img(Path(base_dir, 'assets', 'imgs', 'redgirl_angry1.png'), 160),
                    scale_img(Path(base_dir, 'assets', 'imgs', 'redgirl_angry2.png'), 160),
                ]),
            }
        elif e_type == 'can':
            return {
                'default': scale_img(Path(base_dir, 'assets', 'imgs', 'can_default.png'), 100),
                'actor_collide': scale_img(Path(base_dir, 'assets', 'imgs', 'can_default.png'), 100),
                'poop_collide': scale_img(Path(base_dir, 'assets', 'imgs', 'can_default.png'), 100),
            }

    def update(self, action='stand'):
        # self.rect.move_ip(-speed, 0)  # Move objects to the left
        self.rect.move_ip(self.actions_speed[action], 0)
        # self.rect.move_ip(-action_speed, 0)

    @classmethod
    def get_allowed_xy(cls):
        return {
            'dog': (None, 600),
            'outcat': (None, 630),
            'blond_girl': (None, 580),
            'red_girl': (None, 580),
            'can': (None, 570),
        }
