import pygame
from commands import render_forground, convert_to_game_cords, convert_to_pixel_cords
from Hero_handler import hero_handler
from Goblin_handler import goblin_handler
from random import randint

# this file will eventually be turned into a funtion for the menu to call

# all functions/classes are initiated
pygame.init()
pygame.font.init()
troop_handler = hero_handler()
enemy_handler = goblin_handler()
game_clock = pygame.time.Clock()

# make_knights is for testing and randomly puts knights on squares
def make_knights():
    for x in range(7):
        for y in range(3):
            if randint(0,1) == 1:
                troop_handler.make_hero((x,y), 'standard')

def make_goblins():
    for y in range(3):
        enemy_handler.spawn_goblin((10,y), 'standard')

# all screen initiation is temporary and will be moved to main
# screen is the object that gets drawn on, then it is scaled onto display
# 360 * 640 is the standard ratio which is 16/9
# scale factor is used for anything that uses screen units
HEIGHT = 360
WIDTH = HEIGHT*16/9
scale_factor = HEIGHT/360
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((640, 360))
pygame.display.set_caption('Heros vs Goblins')

# the while loop is where the game happens
gamin = True
while gamin:
    # tick sets the fps, the game is built around 60 fps
    game_clock.tick(60)

    # event handeler is for all imputs
    for event in pygame.event.get():
        # pressing escape stops the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamin = False
            # using v to spawn knights and space to make them attack is used for debugging
            if event.key == pygame.K_v:
                make_knights()
                # using v to spawn goblins and space to make them attack is used for debugging
            if event.key == pygame.K_b:
                make_goblins()
            if event.key == pygame.K_SPACE:
                troop_handler.attack()
                enemy_handler.attack()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x, y = convert_to_game_cords((x,y), scale_factor)
            # example of using check empty, prints false if hero is in square/it isn't swapnable
            # animation testing, if you click near a hero they die, otherwise places hero
            # could be an example of the way a shop place function would work
            if not troop_handler.check_empty(pygame.mouse.get_pos(), scale_factor):
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
    troop_handler.frame_check()
    enemy_handler.frame_check()

    # the screen is drawn over with a solid color and then all objects are drawn on
    screen.fill((0,255,255))
    render_forground(screen)
    troop_handler.render_heros(screen)
    enemy_handler.render_goblins(screen)

    # this line is for testing frame rate based on object amounts
    # print(f'{len(troop_handler.heros)} knights and {len(enemy_handler.goblins)} goblins running at {game_clock.get_fps()} fps')

    # the screen that has everything drawn on it is scaled and put on the actual display
    # temp_screen stores the transformed screen without changing the scale of screen
    temp_screen = pygame.transform.scale_by(screen, scale_factor)
    display.blit(temp_screen, (0,0))

    # this updates the screen to all of the changes
    pygame.display.flip()