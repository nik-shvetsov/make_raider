import pygame
from pathlib import Path

from utils import scale_img
from poop import Poop

from constants import EVENTS

import sys
import os

# Check if we're running in a PyInstaller bundle
if getattr(sys, 'frozen', False):
    # If we are, set the base directory to the directory containing the .exe file
    base_dir = sys._MEIPASS
else:
    # Otherwise, set it to the current directory
    base_dir = os.path.dirname(__file__)

class Seagull(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.states_imgs = self.load_images()
        self.image = self.states_imgs['normal']
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300) # init pos
        self.speed = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.015)
        self.collided = False
        self.x_controlled_speed = 1.2
        self.y_controlled_speed = 1.1

        # # Scale bbox
        # self.rect.width *= 0.5
        # self.rect.height *= 0.8

    def load_images(self):
        return {
            'normal': scale_img(Path(base_dir, 'assets', 'imgs', 'seagull_fly.png'), 180),
            'dive': scale_img(Path(base_dir, 'assets', 'imgs', 'seagull_dive.png'), 180),
            'collide': scale_img(Path(base_dir, 'assets', 'imgs', 'seagull_scared.png'), 250),
            'bounty_collide': scale_img(Path(base_dir, 'assets', 'imgs', 'seagull_w_hotdog.png'), 220),
            'pooping': scale_img(Path(base_dir, 'assets', 'imgs', 'seagull_poop.png'), 180),
        }

    def switch_state(self, state):
        self.image = self.states_imgs[state]

    def collide(self):
        if not self.collided:
            self.image = self.states_imgs['bounty_collide']
            self.collided = True
            pygame.time.set_timer(EVENTS['ACTOR_COLLISION'], 1000)  # Start a timer for 0.5 seconds

    def update(self, win_size):
        self.check_controls()

        self.speed += self.acceleration
        if not self.collided:
            if self.speed.y > 0.5:
                self.switch_state('dive')
            if self.speed.y < -0.3:
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
        if self.rect.bottom > win_size[1] * 1.08: 
            self.rect.bottom = win_size[1] * 1.07
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
