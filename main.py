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

def spawn_enemies(gstate, x_offset=100, y_position=640, spawn_chance=0.05, dist_range_threshold=(100, 500)):
    if random.uniform(0, 1) < spawn_chance:  # 5% chance per frame
        obj_type = random.choice(list(Enemy.get_allowed_xy().keys()))
        allowed_xy = Enemy.get_allowed_xy().get(obj_type, None)
        if allowed_xy is None:  # If the spot is None, choose a random spot
            x_spot = random.randint(gstate['win_size'][0] + x_offset, gstate['win_size'][0] + x_offset + gstate['win_size'][0])
            y_spot = y_position
        else:
            if allowed_xy[0] is None:
                x_spot = random.randint(gstate['win_size'][0] + x_offset, gstate['win_size'][0] + x_offset + gstate['win_size'][0])
            else:
                x_spot = allowed_xy[0]
            y_spot = allowed_xy[1]
        
        # Check if the new object's position would overlap with an existing object
        dist_threshold = random.randint(*dist_range_threshold)
        for obj in gstate['objects']:
            
            if abs(x_spot - obj.rect.centerx) < dist_threshold:  # If the distance is less than 200
                return  # Don't spawn a new object

        obj = Enemy(x_spot, y_spot, obj_type)
        gstate['objects'].add(obj)

# def update_game_state(actor, objects, win_size, shits, object_threshold=5):
def update_game_state(gstate, object_threshold=8):
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

    for poop in gstate['shits']:
        enemies_hit = pygame.sprite.spritecollide(poop, gstate['objects'], False)
        for enemy in enemies_hit:
            # Handle collision: add score, change state, remove poop
            gstate['score'] += 5
            play_enemy_scream(enemy)
            enemy.switch_state('poop_collide')
            gstate['shits'].remove(poop)
    

def play_bounty_sound(gstate):
    sound = pygame.mixer.Sound(Path('assets', 'sounds', 'hit.mp3'))
    if gstate['actor'].collided:
        sound.play()
    else:
        sound.stop()

def play_enemy_scream(enemy):
    girl_sound = pygame.mixer.Sound(Path('assets','sounds', 'woman_scream.mp3'))
    dog_sound = pygame.mixer.Sound(Path('assets','sounds', 'dog_howl_1.mp3'))
    cat_sound = pygame.mixer.Sound(Path('assets','sounds', 'cat_scream.mp3'))
    if enemy.e_type == 'blond_girl' or enemy.e_type == 'red_girl':
        girl_sound.play(maxtime=450)
    elif enemy.e_type == 'dog':
        dog_sound.play(maxtime=450)
    elif enemy.e_type == 'outcat':
        cat_sound.play(maxtime=450)


def check_collisions_bounty(gstate):
    # hits = pygame.sprite.spritecollide(gstate['actor'], gstate['objects'], True)
    hits = [obj for obj in gstate['objects'] if (
        isinstance(obj, Enemy) and 
        not obj.collided and
        (obj.e_type == 'blond_girl' or obj.e_type == 'red_girl' or obj.e_type == 'can') and 
        pygame.sprite.collide_rect(gstate['actor'], obj)
    )]
    for hit in hits:
        hit.collided = True
        gstate['actor'].collide()
        
    play_bounty_sound(gstate)
    return len(hits)

# def draw_everything(win, bg, actor, score_text, objects,shits):
def draw_everything(gstate):
    """Draw everything on the screen"""
    gstate['win'].blit(gstate['bg'].left_img, (gstate['bg'].left_img_pos, 0))
    gstate['win'].blit(gstate['bg'].right_img, (gstate['bg'].right_img_pos, 0))
    gstate['win'].blit(gstate['actor'].image, gstate['actor'].rect)

    gstate['win'].blit(gstate['score_img'], (10, 20))
    gstate['win'].blit(gstate['score_text'], (gstate['score_img'].get_rect().right + 20, gstate['score_img'].get_rect().centery + 10))

    gstate['win'].blit(gstate['hotdog_img'], (10, 80))
    gstate['win'].blit(gstate['hotdog_text'], (gstate['hotdog_img'].get_rect().right, gstate['hotdog_img'].get_rect().centery + 55))

    """Draw all the objects"""
    for obj in gstate['objects']:
        gstate['win'].blit(obj.image, obj.rect)

    for poop in gstate['shits']:
        gstate['win'].blit(poop.image, poop.rect)

    pygame.display.flip()

def add_shit_object(gstate, event, shit_sound, shit_cost=1):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        if gstate['hotdog_count'] >= shit_cost:
            shit_sound.stop()
            shit_sound.play()
            poop = Poop(gstate['actor'])  # Create a new instance of Poop
            gstate['shits'].add(poop)  # Add the poop to the objects sprite group
            gstate['hotdog_count'] -= shit_cost

def init_start_screen(gstate, sound_path):
    start_screen = StartScreen(gstate['win'], gstate['win_size'], sound_path)
    if not start_screen.run(): # Start Screen
        pygame.quit()
        exit()

def main(gstate):
    ### Game loop ###
    running = True
    gstate['actor'] = Seagull()
    gstate['objects'] = pygame.sprite.Group()
    gstate['shits'] = pygame.sprite.Group()
    gstate['score_img'] = scale_img(Path('assets', 'imgs', 'score.png'), 100)
    gstate['hotdog_img'] = scale_img(Path('assets', 'imgs', 'hotdogscore.png'), 100)
    # Path('assets','fonts', 'Honk', 'honk.ttf')

    ### Init sounds here ###
    fire_sound = pygame.mixer.Sound(Path('assets', 'sounds', 'fire.mp3'))
    bird_hitted_sound = pygame.mixer.Sound(Path('assets','sounds', 'bird_scream.mp3'))
    dog_sound = None

    while running:
        gstate['score_text'] = pygame.font.Font(None, 36).render(str(gstate['score']), True, (255,100,0))
        gstate['hotdog_text'] = pygame.font.Font(None, 80).render(str(gstate['hotdog_count']), True, (255,0,0))  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == EVENTS['ACTOR_COLLISION']:
                gstate['actor'].image = gstate['actor'].states_imgs['normal']
                gstate['actor'].collided = False
            
            add_shit_object(gstate, event, shit_sound=fire_sound)

        """Update the game state"""
        spawn_enemies(gstate)
        update_game_state(gstate)
        gstate['hotdog_count'] += check_collisions_bounty(gstate)
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
        'score': 0,
        'hotdog_count': 0
    }

    gstate['bg'] = Background(Path('assets', 'imgs', 'bg.png'), gstate['win_size'][1], init_speed=1)
    gstate['win'] = pygame.display.set_mode(gstate['win_size'])
    pygame.init()

    ## Game Start ##
    init_start_screen(gstate, sound_path=Path('assets', 'sounds', 'theme_norway.mp3'))
    main(gstate)
