import pygame
from commands import frame_count_check

class knight_handeler():
    def __init__(self):
        self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Warrior\\Blue\\Warrior_Blue.png')
        # self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Goblins\\Troops\\Torch\\Blue\\Torch_Blue.png')
        self.knight_image = pygame.transform.scale_by(self.knight_image, .5)
        # each knight has a (position), image, and (frame position)
        self.knights = []
    def make_knight(self, pos, type):
        fx = 0
        fy = 0
        frame = 0
        self.knights.append(((pos, self.knight_image, (fx, fy, 0), type)))
    def frame_check(self):
        temporary = self.knights
        self.knights = []
        for knight in temporary:
            fx, fy, ff = knight[2]
            fx, fy, ff = frame_count_check(fx, fy, ff, 0, 0)
            knight = ((knight[0][0], knight[0][1]), knight[1], (fx, fy, ff), knight[3])
            self.knights.append(knight)