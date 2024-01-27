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

class Man(pygame.sprite.Sprite):
    def __init__(self, x, y, mtype=None):
        super().__init__()
        self.man_types = self.load_images()
        if mtype is not None:
            self.image = self.man_types[mtype]
        else:
            self.image = self.man_types[random.choice(list(self.man_types.keys()))]
        self.rect = self.image.get_rect(center=(x, y))

    def load_images(self):
        return {
            'man1': scale_img(Path('assets', 'obj_man_1.png'), 100),
            'man2': scale_img(Path('assets', 'obj_man_2.png'), 100),
            'man3': scale_img(Path('assets', 'obj_man_3.png'), 100),
        }

    def update(self, speed=ENV_SPEED):
        self.rect.move_ip(-speed, 0)  # Move objects to the left
    
    @classmethod
    def get_allowed_spots(cls):
        return {
            'man1': None,
            'man2': None,
            'man3': [(300, 200), (400, 200), (500, 200)],
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

def create_title(font_size=50):
    title_font = pygame.font.Font(None, font_size)
    return title_font.render('Måke raider', True, (255, 255, 255))

def create_play_button(win_size):
    return pygame.Rect(win_size[0] / 2 - 50, win_size[1] / 2, 100, 50)

def create_button_text(font_size=36):
    button_font = pygame.font.Font(None, font_size)
    return button_font.render('Play', True, (0, 0, 0))

def start_screen(win, win_size):
    title = create_title()
    play_button = create_play_button(win_size)
    button_text = create_button_text()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return True

        win.fill((0, 0, 0))
        win.blit(title, (win_size[0] / 2 - title.get_width() / 2, win_size[1] / 4))
        pygame.draw.rect(win, (0, 255, 0), play_button)
        win.blit(button_text, (play_button.x + play_button.width / 2 - button_text.get_width() / 2, play_button.y + play_button.height / 2 - button_text.get_height() / 2))
        pygame.display.flip()

# def spawn_objects(objects, win_size, x_offset=100, y_position=640):
#     if random.uniform(0, 1) < 0.1: # 10% chance per frame
#         obj = Man(win_size[0] + x_offset, y_position)
#         objects.add(obj)

def spawn_objects(objects, win_size, x_offset=100, y_position=640, spawn_chance=0.05, dist_threshold=300):
    if random.uniform(0, 1) < 0.05:  # 5% chance per frame
        allowed_spots = Man.get_allowed_spots()
        obj_type = random.choice(list(allowed_spots.keys()))
        spots = allowed_spots[obj_type]
        if spots is None:  # If the spot is None, choose a random spot
            x_spot = random.randint(win_size[0] + x_offset, win_size[0] + x_offset + win_size[0])
            y_spot = y_position
        else:
            spot = random.choice(spots)
            x_spot, y_spot = spot[0] + win_size[0] + x_offset, spot[1]
        
            # Check if the new object's position would overlap with an existing object
            for obj in objects:
                if abs(x_spot - obj.rect.centerx) < dist_threshold:  # If the distance is less than 200
                    return  # Don't spawn a new object

        obj = Man(x_spot, y_spot, obj_type)
        objects.add(obj)

def update_game_state(actor, objects, win_size, object_threshold=5):
    actor.update(win_size)
    objects.update()

    # Keep the number of objects below the threshold
    if len(objects) > object_threshold:
        objects.remove(objects.sprites()[-1])

    for obj in objects:
        if obj.rect.right < 0:
                objects.remove(obj)

def check_collisions(actor, objects):
    hits = pygame.sprite.spritecollide(actor, objects, True)
    if hits:  # If there was a collision
        actor.collide()
    return len(hits)

def draw_everything(win, bg, actor, score_text, objects):
    win.blit(bg.left_img, (bg.left_img_pos, 0))
    win.blit(bg.right_img, (bg.right_img_pos, 0))
    win.blit(actor.image, actor.rect)
    win.blit(score_text, (10, 10))
    for obj in objects:
        win.blit(obj.image, obj.rect)
    pygame.display.flip()

if __name__ == '__main__':
    ### Assets ###
    bg = Background(Path('assets', 'test_bg_l1.png'), Path('assets', 'test_bg_r2.png'))
    win = pygame.display.set_mode(bg.win_size)
    
    ### Game objects ###
    actor = Seagull()
    objects = pygame.sprite.Group()

    ### Game loop ###
    running = True
    score = 0 
    pygame.init()
    font = pygame.font.Font(None, 36)
    if not start_screen(win, bg.win_size):
        pygame.quit()
        exit()

    while running:
        score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENTS['COLLISION']:
                actor.image = actor.states_imgs['normal']
                actor.collided = False

        spawn_objects(objects, bg.win_size)
        update_game_state(actor, objects, bg.win_size)
        score += check_collisions(actor, objects)
        bg.update_position()
        draw_everything(win, bg, actor, score_text, objects)

    pygame.quit()