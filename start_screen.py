import pygame
from pathlib import Path
from utils import scale_img

class StartScreen:
    def __init__(self, window, window_size, theme_path):
        self.window = window
        self.window_size = window_size 
        self.bg_image = pygame.image.load(Path('assets', 'imgs', 'loadscreen.png'))
        self.description_img = scale_img(Path('assets', 'imgs', 'desc.png'), d_height=200)
        self.play_button_img = scale_img(Path('assets', 'imgs', 'start_btn.png'), d_height=100)
        self.play_button = self.create_play_button()
        self.theme_sound = pygame.mixer.Sound(theme_path)
    
    def create_play_button(self):
        img_width, img_height = self.play_button_img.get_size()
        window_size = self.window_size
        return pygame.Rect(
            img_width * 0.05, 
            window_size[1] - img_height * 1.05, 
            img_width, 
            img_height
        )
    
    def draw(self):
        window = self.window
        window.blit(self.bg_image, (0, 0))  # draw the background image
        window.blit(self.description_img, 
            (
                self.window_size[0] - (self.description_img.get_size()[0] + 20),
                self.window_size[1] - (self.description_img.get_size()[1] + 20)
            ))  # draw the description image
        window.blit(self.play_button_img, (self.play_button.x, self.play_button.y)) 

    def run(self):
        while True:
            self.theme_sound.play()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.collidepoint(event.pos):
                        self.theme_sound.stop()
                        return True
            self.draw()
            pygame.display.flip()





