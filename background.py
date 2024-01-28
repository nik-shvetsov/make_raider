import pygame
from utils import scale_img

class Background():
    def __init__(self, img_path, d_height, init_speed=1):
        super().__init__()
        self.left_img = scale_img(img_path, d_height=d_height)
        self.right_img = pygame.transform.flip(self.left_img, True, False)
        self.win_size = self.left_img.get_size()
        self.left_img_pos = 0
        self.right_img_pos = self.right_img.get_width()
        self.speed = init_speed

    def update_position(self):
        self.left_img_pos -= self.speed
        self.right_img_pos -= self.speed
        # If one background image goes off screen, reset its position to the right
        if self.left_img_pos < -self.left_img.get_width():
            self.left_img_pos = self.right_img.get_width()
        if self.right_img_pos < -self.right_img.get_width():
            self.right_img_pos = self.left_img.get_width()
