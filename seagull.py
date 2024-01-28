import pygame
from pathlib import Path

from utils import scale_img
from poop import Poop

from constants import EVENTS

class Seagull(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.states_imgs = self.load_images()
        self.image = self.states_imgs['normal']
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300) # init pos
        self.speed = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.1)
        self.collided = False
        self.x_controlled_speed = 2
        self.y_controlled_speed = 5


    def load_images(self):
        return {
            'normal': scale_img(Path('assets', 'imgs', 'seagull_fly.png'), 150),
            'dive': scale_img(Path('assets', 'imgs', 'seagull_dive.png'), 150),
            'collide': scale_img(Path('assets', 'imgs', 'seagull_scared.png'), 150),
            'bounty_collide': scale_img(Path('assets', 'imgs', 'seagull_w_hotdog.png'), 150),
            'pooping': scale_img(Path('assets', 'imgs', 'seagull_poop.png'), 150),
        }

    def switch_state(self, state):
        self.image = self.states_imgs[state]

    def collide(self):
        if not self.collided:
            self.image = self.states_imgs['bounty_collide']
            self.collided = True
            pygame.time.set_timer(EVENTS['ACTOR_COLLISION'], 500)  # Start a timer for 0.5 seconds

    def update(self, win_size):
        self.check_controls()
        self.speed += self.acceleration
        if self.speed.y > 3:
            self.switch_state('dive')
        if self.speed.y < -3:
            self.switch_state('normal')
        self.rect.move_ip(self.speed)
        self.restrict_movement(win_size)
        self.check_collision_event()

    def check_controls(self): 
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        #         self.speed.x = -self.x_controlled_speed
        #     elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        #         self.speed.x = self.x_controlled_speed
        #     else:
        #         self.speed.x = 0
        #     if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        #         self.speed.y = -self.y_controlled_speed

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed.x = -self.x_controlled_speed
        elif keys[pygame.K_RIGHT]:
            self.speed.x = self.x_controlled_speed
        else:
            self.speed.x = 0
        if keys[pygame.K_UP]:
            self.speed.y = -self.y_controlled_speed

    def restrict_movement(self, win_size):
        if self.rect.bottom > win_size[1]: 
            self.rect.bottom = win_size[1]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > win_size[0]:
            self.rect.right = win_size[0]

    def check_collision_event(self):
        for event in pygame.event.get():
            if event.type == EVENTS['ACTOR_COLLISION']:
                self.image = self.states_imgs['normal']
                self.collided = False
