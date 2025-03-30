'''
metal hit whoosh https://mixkit.co/free-sound-effects/sword/ is sword sound
hammer hit on wood https://mixkit.co/free-sound-effects/discover/hammer/ is hammer sound
Arrow shot through air https://mixkit.co/free-sound-effects/medieval-battle/ is bow sound
Impact of a blow https://mixkit.co/free-sound-effects/hit/ is hit sound
spawn sound is https://pixabay.com/sound-effects/thud-sound-effect-319090/ 
lego death is https://tuna.voicemod.net/sound/9a9a1207-9d4d-49a6-92c1-4827fe1e9506
scream death is https://tuna.voicemod.net/sound/776f023d-1bb4-4365-a5ea-f6e0069695f8
roblox death is https://tuna.voicemod.net/sound/0c1898d8-28fa-4796-8b52-7cc0a9b9b3c8
troop spawn is https://tuna.voicemod.net/sound/f6ebeb9f-b314-4dc5-872b-9d0a77b38525 
'''


import pygame
from commands import render_forground, convert_to_game_cords, convert_to_pixel_cords
from Hero_handler import hero_handler
from Goblin_handler import goblin_handler
from Sound_handler import sound_handler
from random import randint, choice

# this file will eventually be turned into a funtion for the menu to call

# all functions/classes are initiated
pygame.init()
pygame.font.init()
pygame.mixer.init()
sound_manager = sound_handler()
troop_handler = hero_handler(sound_manager)
enemy_handler = goblin_handler(sound_manager)
game_clock = pygame.time.Clock()
pygame.mixer.music.load('fear music.mp3')
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play()

# make_heros is for testing and randomly puts random hero on each square
# heros = ['pawn', 'standard', 'archer']
# def make_heros():
#     for x in range(7):
#         for y in range(3):
#             troop_handler.make_hero((x,y), choice(heros))
def make_heros():
    for x in range(7):
        for y in range(3):
            if x < 5:
                troop_handler.make_hero((x,y), 'archer')
            else:
                troop_handler.make_hero((x,y), 'standard')

goblins = ['standard', 'heavy', 'fast']
def make_goblins():
    for y in range(3):
        enemy_handler.spawn_goblin((10,y), choice(goblins))

# all screen initiation is temporary and will be moved to main
# screen is the object that gets drawn on, then it is scaled onto display
# 360 * 640 is the standard ratio which is 16/9
# scale factor is used for anything that uses screen units
# getting display info before setup gets monitor screen size which is used for auto fill fullscreen
WIDTH = pygame.display.Info().current_w
HEIGHT = WIDTH*9/16
scale_factor = HEIGHT/360
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((640, 360))
pygame.display.set_caption('Heros vs Goblins')
pygame.display.toggle_fullscreen()
frame = 0
f_goal = 300

# the while loop is whaere the game happens
gamin = True
while gamin:
    # tick sets the fps, the game is built around 60 fps
    game_clock.tick(60)

    # this is a basic enemy spawn system
    # TODO move into goblin handler and add seeds
    frame += 1
    if frame % f_goal == 0:
        make_goblins()
        f_goal = 100
        frame = 0

    # event handeler is for all imputs
    for event in pygame.event.get():
        # pressing escape stops the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamin = False
            # using v to spawn knights and space to make them attack is used for debugging
            if event.key == pygame.K_v:
                make_heros()
                # using v to spawn goblins and space to make them attack is used for debugging
            if event.key == pygame.K_b:
                make_goblins()
            if event.key == pygame.K_SPACE:
                troop_handler.attack()
                enemy_handler.attack()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x, y = convert_to_game_cords((x,y), scale_factor)
            if troop_handler.check_empty((x,y), scale_factor, True):
                troop_handler.make_hero((x,y), 'standard')
            # example of using check empty, prints false if hero is in square/it isn't swapnable
            # animation testing, if you click near a hero they die, otherwise places hero
            # could be an example of the way a shop place function would work
            elif not troop_handler.check_empty(pygame.mouse.get_pos(), scale_factor, False):
                for hero in troop_handler.heros:
                    if hero.pos == (x,y):
                        hero.attack()
                        hero.take_damage(100)
            for goblin in enemy_handler.goblins:
                x, y = pygame.mouse.get_pos()
                gx, gy = convert_to_pixel_cords(goblin.pos, scale_factor, 32, 48)
                if x-24 < gx < x+24 and y-24 < gy < y+24:
                    goblin.take_damage(40)
            
        # clicking the x stops the game
        if event.type == pygame.QUIT:
            gamin = False

    # frame check is where most game functions occur
    troop_handler.frame_check(enemy_handler)
    enemy_handler.frame_check(troop_handler)

    # the screen is drawn over with a solid color and then all objects are drawn on
    screen.fill((0,255,255))
    render_forground(screen)
    troop_handler.render_heros(screen)
    enemy_handler.render_goblins(screen)

    # this line is for testing frame rate based on object amounts
    # print(f'you have {enemy_handler.elims} elims while there are {len(troop_handler.heros)} knights and {len(enemy_handler.goblins)} goblins running at {game_clock.get_fps()} fps')

    # the screen that has everything drawn on it is scaled and put on the actual display
    # temp_screen stores the transformed screen without changing the scale of screen
    temp_screen = pygame.transform.scale_by(screen, scale_factor)
    display.blit(temp_screen, (0,0))

    # this alows all sound fx that have been played to be played next frame
    if frame % 5 == 0:
        sound_manager.reset_availability()

    # this updates the screen to all of the changes
    pygame.display.flip()