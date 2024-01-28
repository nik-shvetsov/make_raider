import pygame
import random
from pathlib import Path
from utils import scale_img

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, e_type=None):
        super().__init__()
        self.e_type = e_type if e_type is not None else random.choice(list(self.get_allowed_xy.keys()))
        self.state_imgs = self.load_images(self.e_type)
        self.image = self.state_imgs['default']
        self.rect = self.image.get_rect(center=(x, y))
        self.collided = False

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
                'default': scale_img(Path('assets', 'imgs', 'dog_default.png'), 100),
                'poop_collide': scale_img(Path('assets', 'imgs', 'dog_state2.png'), 100),
                'actor_collide': scale_img(Path('assets', 'imgs', 'dog_state2.png'), 100)
            }
        elif e_type == 'outcat':
            return {
                'default': scale_img(Path('assets', 'imgs', 'outcat_default.png'), 110),
                'poop_collide': scale_img(Path('assets', 'imgs', 'outcat_angry.png'), 130),
                'actor_collide': scale_img(Path('assets', 'imgs', 'outcat_angry.png'), 130),
            }
        elif e_type == 'blond_girl':
            return {
                'default': scale_img(Path('assets', 'imgs', 'blondgirl_default.png'), 140),
                'poop_collide': random.choice([
                    scale_img(Path('assets', 'imgs', 'blondgirl_poop1.png'), 140),
                    scale_img(Path('assets', 'imgs', 'blondgirl_poop2.png'), 140),
                ]),
                'actor_collide': random.choice([
                    scale_img(Path('assets', 'imgs', 'blondgirl_angry1.png'), 140),
                    scale_img(Path('assets', 'imgs', 'blondgirl_angry2.png'), 140),
                ]),
            }
        elif e_type == 'red_girl':
            return {
                'default': scale_img(Path('assets', 'imgs', 'redgirl_default.png'), 140),
                'poop_collide': random.choice([
                    scale_img(Path('assets', 'imgs', 'redgirl_poop1.png'), 140),
                    scale_img(Path('assets', 'imgs', 'redgirl_poop2.png'), 140),
                ]),
                'actor_collide': random.choice([
                    scale_img(Path('assets', 'imgs', 'redgirl_angry1.png'), 140),
                    scale_img(Path('assets', 'imgs', 'redgirl_angry2.png'), 140),
                ]),
            }
        elif e_type == 'can':
            return {
                'default': scale_img(Path('assets', 'imgs', 'can_default.png'), 80),
                'actor_collide': scale_img(Path('assets', 'imgs', 'can_default.png'), 80),
                'poop_collide': scale_img(Path('assets', 'imgs', 'can_default.png'), 80),
            }

    def update(self, action='stand'):
        # self.rect.move_ip(-speed, 0)  # Move objects to the left
        self.rect.move_ip(self.actions_speed[action], 0)
        # self.rect.move_ip(-action_speed, 0)

    @classmethod
    def get_allowed_xy(cls):
        return {
            'dog': (None, 620),
            'outcat': (None, 640),
            'blond_girl': (None, 600),
            'red_girl': (None, 600),
            'can': (None, 580),
        }
