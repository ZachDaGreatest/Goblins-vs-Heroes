import pygame
from commands import render_forground
from Hero_handler import hero_handler
from random import randint

# this file will eventually be turned into a funtion for the menu to call

# all functions/classes are initiated
pygame.init()
pygame.font.init()
troop_handeler = hero_handler()
game_clock = pygame.time.Clock()

# make_knights is for testing and randomly puts knights on squares
def make_knights():
    for x in range(7):
        for y in range(3):
            if randint(0,1) == 1:
                troop_handeler.make_hero((x,y), 'standard')

# all screen initiation is temporary and will be moved to main
# 360 * 640 is the standard ratio
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption('Heros vs Goblins')
screen.fill((0,0,0))
pygame.display.flip()

# the while loop is where the game happens
gamin = True
while gamin:
    # tick sets the fps, the game is built around 60 fps
    game_clock.tick(60)

    # event handeler is for all imputs
    for event in pygame.event.get():
        # pressing escape or the x stops the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamin = False
            # using v to spawn knights and space to make them attack is used for debugging
            if event.key == pygame.K_v:
                make_knights()
            if event.key == pygame.K_SPACE:
                troop_handeler.attack()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # animation testing, if you click near a hero they die
            for hero in troop_handeler.heros:
                if (hero.pos[0]*64-16 + 96 > x > hero.pos[0]*64-16) and  (150+hero.pos[1]*64 + 96 > y > 150+hero.pos[1]*64):
                    hero.attack()
                    hero.take_damage(100)
        if event.type == pygame.QUIT:
            gamin = False

    # frame check is where most game functions occur
    troop_handeler.frame_check()

    # the screen is drawn over with a solid color and then all objects are drawn on
    screen.fill((0,255,255))
    render_forground(screen)
    troop_handeler.render_heros(screen)

    # this line is for testing frame rate based on hero amounts
    # print(game_clock.get_fps(), len(troop_handeler.heros))

    # this updates the screen to all of the changes
    pygame.display.flip()