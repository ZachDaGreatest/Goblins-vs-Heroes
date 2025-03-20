import pygame
from commands import render_forground, frame_count_check
from Knight_handeler import knight_handeler

pygame.init()
pygame.font.init()
troop_handeler = knight_handeler()

for x in range(7):
    for y in range(3):
        troop_handeler.make_knight((x,y), 'guy')

# 360 * 640 is the standard ratio
screen = pygame.display.set_mode((640, 360))

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        if event.type == pygame.QUIT:
            gamin = False

    troop_handeler.frame_check()







    screen.fill((0,255,255))
    render_forground(screen)

    for knight in troop_handeler.knights:
        screen.blit(knight[1], (knight[0][0]*64-16, 160+knight[0][1]*64), (96*knight[2][0], 96*knight[2][1], 96, 96))

    fx, fy, ff = frame_count_check(fx, fy, ff, 1, 1)
    mx,my = pygame.mouse.get_pos()

    screen.blit(troop_handeler.knight_image, (mx-48, my-48), (fx*96,fy*96,96,96))

    pygame.display.flip()