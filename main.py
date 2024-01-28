import pygame
from pathlib import Path
import random

# Utils
from utils import scale_img
 # Constants
from constants import EVENTS
# Menue Screen
from start_screen import StartScreen  
# Background 
from background import Background
# Sprites
from seagull import Seagull
from man import Man
from poop import Poop

def spawnEnemies(objects, win_size, x_offset=100, y_position=640, spawn_chance=0.05, dist_threshold=300): # Add Man
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

def update_game_state(actor, objects, win_size, shits, object_threshold=5):
    actor.update(win_size)
    objects.update()
    shits.update()
    # Keep the number of objects below the threshold
    if len(objects) > object_threshold:
        objects.remove(objects.sprites()[-1])

    for obj in objects:
        if obj.rect.right < 0:
                objects.remove(obj) 

    for shit in shits:
        print(shits)  
        if shit.rect.y > win_size[0]:
                shits.remove(shit)

def play_collision_sound(actor):
    sound = pygame.mixer.Sound(Path('assets', 'sounds', 'hit.mp3'))
    if actor.collided:
        sound.play()
    else:
        sound.stop()

def check_collisions(actor, objects):
    hits = pygame.sprite.spritecollide(actor, objects, True)
    if hits:  # If there was a collision
        actor.collide()
        
    play_collision_sound(actor)
    return len(hits)

def draw_everything(win, bg, actor, score_text, objects,shits): # Render Evrthing on screen
    """Draw everything on the screen"""
    win.blit(bg.left_img, (bg.left_img_pos, 0))
    win.blit(bg.right_img, (bg.right_img_pos, 0))
    win.blit(actor.image, actor.rect)
    win.blit(score_text, (10, 100))

    """Draw all the objects"""
    for obj in objects:
        win.blit(obj.image, obj.rect)

    for pop in shits:
        win.blit(pop.image, pop.rect)

    pygame.display.flip()

def lookForPoop(actor, poops, event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        poop = Poop(actor)  # Create a new instance of Poop
        poops.add(poop)  # Add the poop to the objects sprite group

def init_start_screen(sound_path):
    start_screen = StartScreen(win, win_size, sound_path)
    if not start_screen.run(): # Start Screen
        pygame.quit()
        exit()

def main(bg, win):
    ### Game loop ###
    running = True
    score = 0 

    ### Game objects ###
    humans = pygame.sprite.Group()
    actor = Seagull()
    shits = pygame.sprite.Group()

    font = pygame.font.Font(None, 36)
    while running:
        score_text = font.render('Score: ' + str(score), True, (255, 255, 255))   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENTS['COLLISION']:
                actor.image = actor.states_imgs['normal']
                actor.collided = False
            
            lookForPoop(actor, shits, event)

        """Update the game state"""
        spawnEnemies(humans, win_size)
        update_game_state(actor, humans, win_size, shits)
        score += check_collisions(actor, humans)

        draw_everything(win, bg, actor, score_text, humans, shits)
        bg.update_position()

    pygame.quit()
 
if __name__ == '__main__':
    ### Setup ###
    win_size = (1024, 768)
    sound_theme = Path('assets', 'sounds', 'theme_norway.mp3')
    bg = Background(Path('assets', 'imgs', 'bg.png'), win_size[1])
    win = pygame.display.set_mode(win_size)
    pygame.init()

    gstate = {
        'win': win,
        'win_size': (1024, 768),
        'bg': bg,
        'objects': [],
        'actor': None,
        'shits': [],
    }

    ## Game Start ##
    init_start_screen(sound_theme)
    main(bg, win)
