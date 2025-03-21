import pygame
from commands import render_forground, frame_count_check
from Knight_handeler import knight_handeler
from random import randint

pygame.init()
pygame.font.init()
troop_handeler = knight_handeler()
def make_knights():
    for x in range(7):
        for y in range(3):
            if randint(0,1) == 1:
                troop_handeler.make_knight((x,y), 'standard')
# troop_handeler.make_knight((0,0), 'standard')

# 360 * 640 is the standard ratio
screen = pygame.display.set_mode((640, 360))
pygame.display.set_caption('Heros vs Goblins')

screen.fill((0,0,0))
pygame.display.flip()

game_clock = pygame.time.Clock()

frame = 0
ff = 0
fx = 0
fy = 0

gamin = True
while gamin:
    game_clock.tick(60)
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamin = False
            if event.key == pygame.K_v:
                make_knights()
            if event.key == pygame.K_SPACE:
                troop_handeler.attack()
                # for hero in troop_handeler.heros:
                #     hero.take_damage(20)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for hero in troop_handeler.heros:
                if (hero.pos[0]*64-16 + 96 > x > hero.pos[0]*64-16) and  (150+hero.pos[1]*64 + 96 > y > 150+hero.pos[1]*64):
                    hero.attack()
                    hero.take_damage(20)
        if event.type == pygame.QUIT:
            gamin = False

    troop_handeler.frame_check()

    screen.fill((0,255,255))
    render_forground(screen)

    troop_handeler.render_heros(screen)

    # print(game_clock.get_fps(), len(troop_handeler.heros))

    pygame.display.flip()