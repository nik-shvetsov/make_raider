import pygame
from pathlib import Path
import random
from utils import scale_img

ENV_SPEED = 2
EVENTS = {
    'COLLISION': pygame.USEREVENT,
    'TIMER': pygame.USEREVENT + 1,
}

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

def spawn_objects(objects, win_size, x_offset=100, y_position=640, spawn_chance=0.05, dist_threshold=300): # Add Man
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

def draw_everything(win, bg, actor, score_text, objects): # Render Evrthing on screen
    win.blit(bg.left_img, (bg.left_img_pos, 0))
    win.blit(bg.right_img, (bg.right_img_pos, 0))
    win.blit(actor.image, actor.rect)
    win.blit(score_text, (10, 100))
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