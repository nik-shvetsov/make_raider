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
from enemy import Enemy
from poop import Poop

def spawn_enemies(gstate, x_offset=100, y_position=640, spawn_chance=0.05, dist_threshold=300):
    if random.uniform(0, 1) < 0.05:  # 5% chance per frame
        allowed_spots = Enemy.get_allowed_spots()
        obj_type = random.choice(list(allowed_spots.keys()))
        spots = allowed_spots.get(obj_type, None)
        if spots is None:  # If the spot is None, choose a random spot
            x_spot = random.randint(gstate['win_size'][0] + x_offset, gstate['win_size'][0] + x_offset + gstate['win_size'][0])
            y_spot = y_position
        else:
            spot = random.choice(spots)
            x_spot, y_spot = spot[0] + gstate['win_size'][0] + x_offset, spot[1]
        
        # Check if the new object's position would overlap with an existing object
        for obj in gstate['objects']:
            if abs(x_spot - obj.rect.centerx) < dist_threshold:  # If the distance is less than 200
                return  # Don't spawn a new object

        obj = Enemy(x_spot, y_spot, obj_type)
        gstate['objects'].add(obj)

# def update_game_state(actor, objects, win_size, shits, object_threshold=5):
def update_game_state(gstate, object_threshold=5):
    gstate['actor'].update(gstate['win_size'])
    gstate['objects'].update()
    gstate['shits'].update()
    # Keep the number of objects below the threshold
    if len(gstate['objects']) > object_threshold:
        gstate['objects'].remove(gstate['objects'].sprites()[-1])

    for obj in gstate['objects']:
        if obj.rect.right < 0:
            gstate['objects'].remove(obj) 

    for shit in gstate['shits']:
        if shit.rect.y > gstate['win_size'][0]:
            gstate['shits'].remove(shit)

def play_collision_sound(gstate):
    sound = pygame.mixer.Sound(Path('assets', 'sounds', 'hit.mp3'))
    if gstate['actor'].collided:
        sound.play()
    else:
        sound.stop()

def check_collisions(gstate):
    hits = pygame.sprite.spritecollide(gstate['actor'], gstate['objects'], True)
    if hits:  # If there was a collision
        gstate['actor'].collide()
        
    play_collision_sound(gstate)
    return len(hits)

# def draw_everything(win, bg, actor, score_text, objects,shits):
def draw_everything(gstate):
    """Draw everything on the screen"""
    gstate['win'].blit(gstate['bg'].left_img, (gstate['bg'].left_img_pos, 0))
    gstate['win'].blit(gstate['bg'].right_img, (gstate['bg'].right_img_pos, 0))
    gstate['win'].blit(gstate['actor'].image, gstate['actor'].rect)
    gstate['win'].blit(gstate['score_text'], (10, 10))

    """Draw all the objects"""
    for obj in gstate['objects']:
        gstate['win'].blit(obj.image, obj.rect)

    for poop in gstate['shits']:
        gstate['win'].blit(poop.image, poop.rect)

    pygame.display.flip()

def add_shit_object(gstate, event, shit_cost=1):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if gstate['score'] >= shit_cost:
            poop = Poop(gstate['actor'])  # Create a new instance of Poop
            gstate['shits'].add(poop)  # Add the poop to the objects sprite group
            gstate['score'] -= shit_cost

def init_start_screen(gstate, sound_path):
    start_screen = StartScreen(gstate['win'], gstate['win_size'], sound_path)
    if not start_screen.run(): # Start Screen
        pygame.quit()
        exit()

def main(gstate):
    ### Game loop ###
    running = True
    gstate['score'] = 0 
    gstate['actor'] = Seagull()
    gstate['objects'] = pygame.sprite.Group()
    gstate['shits'] = pygame.sprite.Group()

    font = pygame.font.Font(None, 36)
    while running:
        gstate['score_text'] = font.render('Score: ' + str(gstate['score']), True, (0, 0, 255))   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENTS['COLLISION']:
                gstate['actor'].image = gstate['actor'].states_imgs['normal']
                gstate['actor'].collided = False
            
            add_shit_object(gstate, event)

        """Update the game state"""
        spawn_enemies(gstate)
        update_game_state(gstate)
        gstate['score'] += check_collisions(gstate)

        draw_everything(gstate)
        gstate['bg'].update_position()

    pygame.quit()
 
if __name__ == '__main__':
    ### Setup ###
    gstate = {
        'win_size': (1024, 768),
        'objects': [],
        'actor': None,
        'shits': [],
    }

    gstate['bg'] = Background(Path('assets', 'imgs', 'bg.png'), gstate['win_size'][1], init_speed=1)
    gstate['win'] = pygame.display.set_mode(gstate['win_size'])
    pygame.init()

    ## Game Start ##
    init_start_screen(gstate, sound_path=Path('assets', 'sounds', 'theme_norway.mp3'))
    main(gstate)
