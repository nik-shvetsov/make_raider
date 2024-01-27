import pygame
from pathlib import Path
import random

# Utils
from utils import scale_img
 # Constants
from constants import EVENTS
# Menue Screen
from startScreen import StartScreen  
# Background 
from background import Background

# Sprites
from seagull import Seagull
from man import Man

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

def play_collision_sound(actor, sound):
    if actor.collided:
        sound.play()
    else:
        sound.stop()

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
    # bg = Background(Path('pics', 'houses_l.png'), Path('pics', 'houses_r.png'))
    bg = Background(Path('assets', 'test_bg_l1.png'), Path('assets', 'test_bg_r2.png'))
    win_size = (1000, 1000)
    win = pygame.display.set_mode(win_size)

    sound_theme = Path('assets','sounds','theme_norway.mp3')
    sound_bird_scream = Path('assets','sounds','bird_scream.mp3')
    sound_man_scream = Path('assets','sounds', 'man_scream.mp3')
    sound_bird_hit = Path('assets', 'sounds', 'hit.mp3')

    pygame.mixer.init()
    collision_sound = pygame.mixer.Sound(str(sound_bird_hit))

    
    ### Game objects ###
    objects = pygame.sprite.Group()
    actor = Seagull(objects)

    ### Game loop ###
    running = True
    score = 0 
    pygame.init()
    font = pygame.font.Font(None, 36)

    startScreen = StartScreen(win, win_size, sound_theme)
    if not startScreen.startScreen(): # Start Screen
        pygame.quit()
        print("Game closed")
        exit()

    while running:
        score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENTS['COLLISION']:
                actor.image = actor.states_imgs['normal']
                actor.collided = False
        
        spawn_objects(objects, win_size)
        update_game_state(actor, objects, win_size)
        score += check_collisions(actor, objects)
        bg.update_position()
        draw_everything(win, bg, actor, score_text, objects)

    pygame.quit()