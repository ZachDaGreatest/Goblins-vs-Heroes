import pygame
from commands import render_forground, convert_to_game_cords, convert_to_pixel_cords, row_spawns
from Hero_handler import hero_handler
from Goblin_handler import goblin_handler
from Sound_handler import sound_handler
from random import randint, choice
from gui import render_gui, check_gui_click
from decorations import render_subtile_map, render_fore_decorations
# this file will eventually be turned into a funtion for the menu to call

# FIXME there are random stuters, 
'''
I have individualy commented out every line in the program and it still happens
if event handler is commented out the program crashes when there would be a lag spike
the old code runs fine
seems like it is caused by poor optomization since it only occurs when on battery and not when plugged in
'''

# TODO include the seed here at the top with random.seed()

# all functions/classes are initiated
pygame.init()
pygame.font.init()
font = pygame.font.Font('slkscr.ttf', 18)
pygame.mixer.init()
sound_manager = sound_handler()
troop_handler = hero_handler(sound_manager)
enemy_handler = goblin_handler(sound_manager)
game_clock = pygame.time.Clock()
pygame.mixer.music.load('music\\runescape attack 6.mp3')
pygame.mixer.music.set_volume(.8)
pygame.mixer.music.play()


gold_mine_inactive = pygame.image.load('Tiny Swords\Tiny Swords (Update 010)\Resources\Gold Mine\GoldMine_Inactive.png')
gold_mine_active = pygame.image.load('Tiny Swords\Tiny Swords (Update 010)\Resources\Gold Mine\GoldMine_Active.png')
gold_mine = gold_mine_inactive


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
WIDTH = pygame.display.Info().current_w
HEIGHT = WIDTH*9/16
scale_factor = HEIGHT/360
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((640, 360))
pygame.display.set_caption('Goblins vs Heroes')
pygame.display.toggle_fullscreen()
frame = 0
f_goal = 60
iteration = 0

top_row = row_spawns()
middle_row = row_spawns()
bottom_row = row_spawns()

# the while loop is whaere the game happens
gamin = True
while gamin:
    # if the music isn't playing it is started again
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    # tick sets the fps, the game is built around 60 fps
    game_clock.tick(60)
    
    # this is a basic enemy spawn system
    # TODO move into goblin handler and add seeds
    frame += 1
    if frame % f_goal == 0 and iteration < 180:
        # make_goblins()
        goblin_type = top_row[iteration]
        if goblin_type != False:
            enemy_handler.spawn_goblin((10,0), goblin_type)
        goblin_type = middle_row[iteration]
        if goblin_type != False:
            enemy_handler.spawn_goblin((10,1), goblin_type)
        goblin_type = bottom_row[iteration]
        if goblin_type != False:
            enemy_handler.spawn_goblin((10,2), goblin_type)
        iteration += 1

    # use this section for economy code
    if iteration > 20:
        gold_mine = gold_mine_active

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
            # example of using check empty, prints false if hero is in square/it isn't swapnable
            # animation testing, if you click near a hero they die, otherwise places hero
            # could be an example of the way a shop place function would work
            if troop_handler.check_empty(pygame.mouse.get_pos(), scale_factor, False):
                troop_handler.make_hero(convert_to_game_cords((x,y), scale_factor), selected_troop)
            else:
                for hero in troop_handler.heros:
                    if hero.pos == convert_to_game_cords((x,y), scale_factor):
                        hero.take_damage(100)
            x, y = pygame.mouse.get_pos()
            selected_troop = check_gui_click(x, y, scale_factor)
        # clicking the x stops the game
        if event.type == pygame.QUIT:
            gamin = False

    # frame check is where most game functions occur
    troop_handler.frame_check(enemy_handler)
    enemy_handler.frame_check(troop_handler)

    # the screen is drawn over with a solid color and then all objects are drawn on
    screen.fill((0,255,255))
    render_subtile_map(screen)
    render_forground(screen)
    render_gui(screen, pygame.mouse.get_pos(), scale_factor)
    troop_handler.render_heros(screen)
    enemy_handler.render_goblins(screen)
    

    # this line is for testing frame rate based on object amounts
    # info = f'{enemy_handler.elims} elims : {len(troop_handler.heros)} knights and {len(enemy_handler.goblins)} goblins : {round(game_clock.get_fps(), 8)} fps'
    # stats = font.render(info, False, (255,0,0))
    # screen.blit(stats, (0,132))
    
    # s = font.render(str(iteration), False, (0,0,0))
    # screen.blit(s, (0,152))

    # the screen that has everything drawn on it is scaled and put on the actual display
    # temp_screen stores the transformed screen without changing the scale of screen
    temp_screen = pygame.transform.scale_by(screen, scale_factor)
    display.blit(temp_screen, (0,0))

    # this alows all sound fx that have been played to be played next frame
    if frame % 5 == 0:
        sound_manager.reset_availability()

    # this updates the screen to all of the changes
    pygame.display.flip()