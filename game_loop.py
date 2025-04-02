import pygame
from commands import render_forground, convert_to_game_cords
from Hero_handler import hero_handler
from Goblin_handler import goblin_handler
from Sound_handler import sound_handler
from Player_functions import player_functions
from random import randint, choice
from gui import render_gui, check_gui_click
from decorations import render_subtile_map, render_fore_decorations
# this file will eventually be turned into a funtion for the menu to call

# TODO add a black and white gold bag that is slowly covered by a normal one to show when the goldmine will produce gold
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
player = player_functions(enemy_handler, troop_handler, game_clock)
pygame.mixer.music.load('music\\tavern brawl.mp3')
pygame.mixer.music.set_volume(.8)
pygame.mixer.music.play()
lost_image = pygame.image.load('skull emoji.gif')

# all screen initiation is temporary and will be moved to main
# screen is the object that gets drawn on, then it is scaled onto display
# 360 * 640 is the standard ratio which is 16/9
# scale factor is used for anything that uses screen units
WIDTH = pygame.display.Info().current_w
# this ensures a even scale factor so that all screen functions work
for n in range(1000):
    if n < (WIDTH/640) < n+1:
        WIDTH = n*640
        break
HEIGHT = WIDTH*9/16
scale_factor = HEIGHT/360
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((640, 360))
pygame.display.set_caption('Goblins vs Heroes')
pygame.display.toggle_fullscreen()
print(WIDTH, scale_factor)

enemy_handler.spawn_algorithm()

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
    enemy_handler.spawn_check()

    # event handeler is for all imputs
    for event in pygame.event.get():
        # pressing escape stops the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamin = False
            # using v to spawn knights and space to make them attack is used for debugging
            if event.key == pygame.K_v:
                player.make_heros()
                # using b to spawn goblins and space to make them attack is used for debugging
            if event.key == pygame.K_b:
                player.make_goblins()
            if event.key == pygame.K_h:
                player.health -= 1
            if event.key == pygame.K_r:
                troop_handler.heros = []
                enemy_handler.goblins = []
                enemy_handler.iteration = 0
                player.gold = 30
                player.health = 3
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # example of using check empty, prints false if hero is in square/it isn't swapnable
            if troop_handler.check_empty(pygame.mouse.get_pos(), scale_factor, False):
                try: 
                    if player.payment_check(selected_troop):
                        troop_handler.make_hero(convert_to_game_cords((x,y), scale_factor), selected_troop)
                except: pass
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
    player.frame_check()

    # the screen is drawn over with a solid color and then all objects are drawn on
    screen.fill((0,210,245))
    render_subtile_map(screen)
    render_forground(screen)
    screen.blit(player.gold_mine, (0, 88))
    render_gui(screen, pygame.mouse.get_pos(), scale_factor)
    troop_handler.render_heros(screen)
    enemy_handler.render_goblins(screen)
    render_fore_decorations(screen)
    player.debug_menu(screen, font)
    if player.state == 'dead':
        for hero in troop_handler.heros:
            if hero.state != 'dead':
                hero.state = 'dead'
                pygame.mixer.Sound('sound fx\\scream death.mp3').play()
        screen.blit(lost_image, (320-lost_image.get_rect()[3]/2, 180-lost_image.get_rect()[2]/2))

    # the screen that has everything drawn on it is scaled and put on the actual display
    # temp_screen stores the transformed screen without changing the scale of screen
    temp_screen = pygame.transform.scale_by(screen, scale_factor)
    display.blit(temp_screen, (0,0))

    # this alows all sound fx that have been played to be played next frame
    if enemy_handler.frame % 5 == 0:
        sound_manager.reset_availability()

    # this updates the screen to all of the changes
    pygame.display.flip()