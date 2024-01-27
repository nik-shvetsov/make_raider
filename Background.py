import pygame
from pathlib import Path
import random
from utils import scale_img

ENV_SPEED = 2
EVENTS = {
    'COLLISION': pygame.USEREVENT,
    'TIMER': pygame.USEREVENT + 1,
}

class Background():
    def __init__(self, left_path, right_path):
        super().__init__()
        self.left_img = pygame.image.load(left_path)
        self.right_img = pygame.image.load(right_path)
        assert self.left_img.get_size() == self.right_img.get_size(), 'Background images must be the same size'
        self.win_size = self.left_img.get_size()

        self.left_img_pos = 0
        self.right_img_pos = self.right_img.get_width()

    def update_position(self):
        self.left_img_pos -= 1
        self.right_img_pos -= 1
        # If one background image goes off screen, reset its position to the right
        if self.left_img_pos < -self.left_img.get_width():
            self.left_img_pos = self.right_img.get_width()
        if self.right_img_pos < -self.right_img.get_width():
            self.right_img_pos = self.left_img.get_width()
