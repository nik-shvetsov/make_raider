import pygame
from pathlib import Path
from utils import scale_img

class StartScreen:
    def __init__(self, window, window_size, theme_path):
        self.window = window
        self.window_size = window_size 
        self.play_button_img = scale_img(Path('assets', 'imgs', 'play.png'), 300)
        self.title = self.create_title()
        # self.button_text = self.create_button_text()
        self.play_button = self.create_play_button()
        self.theme_sound = pygame.mixer.Sound(theme_path)
        
    # def create_button_text(self, font_size=36):
    #     button_font = pygame.font.Font(None, font_size)
    #     return button_font.render('Play', True, (0, 0, 0))
    
    def create_play_button(self):
        img_width, img_height = self.play_button_img.get_size()
        window_size = self.window_size
        return pygame.Rect(window_size[0] / 2 - img_width / 2, window_size[1] / 2 - img_height / 2, img_width, img_height)
    
    def create_title(self, font_size=50):
        title_font = pygame.font.Font(None, font_size)
        return title_font.render('Måke raider', True, (255, 255, 255))
    
    def draw(self):
        window = self.window
        window.fill((0, 0, 0))
        window.blit(self.title, (self.window_size[0] / 2 - self.title.get_width() / 2, self.window_size[1] / 4))
        # pygame.draw.rect(window, (0, 255, 0), self.play_button)
        window.blit(self.play_button_img, (self.play_button.x, self.play_button.y))
        # window.blit(self.button_text, 
        #     (self.play_button.x + self.play_button.width / 2 - self.button_text.get_width() / 2, 
        #     self.play_button.y + self.play_button.height / 2 - self.button_text.get_height() / 2)
        # )

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





