import pygame
from pathlib import Path
import random
from utils import scale_img

ENV_SPEED = 2
EVENTS = {
    'COLLISION': pygame.USEREVENT,
    'TIMER': pygame.USEREVENT + 1,
}

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

    def load_images(self):
        return {
            'normal': scale_img(Path('assets', 'seagull_normal_fly.png'), 150),
            'collide': scale_img(Path('assets', 'seagull_quack.png'), 150),
        }

    def collide(self):
        if not self.collided:
            self.image = self.states_imgs['collide']
            self.collided = True
            pygame.time.set_timer(EVENTS['COLLISION'], 500)  # Start a timer for 0.5 seconds

    def update(self, win_size):
        self.update_speed()
        self.speed += self.acceleration
        self.rect.move_ip(self.speed)
        self.restrict_movement(win_size)
        self.check_collision_event()

    def update_speed(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed.x = -ENV_SPEED
        elif keys[pygame.K_RIGHT]:
            self.speed.x = ENV_SPEED
        else:
            self.speed.x = 0

        if keys[pygame.K_UP]:
            self.speed.y = -5

        if keys[pygame.K_SPACE]:  # Check if the space key is pressed
            self.poop()  # Call the poop method

    def poop(self):
        poop = Poop(self)  # Create a new instance of Poop
        objects.add(poop)  # Add the poop to the objects sprite group

    
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
            if event.type == EVENTS['COLLISION']:
                self.image = self.states_imgs['normal']
                self.collided = False
