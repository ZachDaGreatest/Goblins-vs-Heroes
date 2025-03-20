import pygame
from commands import frame_count_check
from Hero import hero

class knight_handeler():
    def __init__(self):
        self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Warrior\\Blue\\Warrior_Blue.png')
        # self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Goblins\\Troops\\Torch\\Blue\\Torch_Blue.png')
        self.knight_image = pygame.transform.scale_by(self.knight_image, .5)
        # each knight has a (position), image, and (frame position)
        self.knights = []

        self.knight_types = {
            'standard' : {
                'max_health' : 100,
                'image' : self.knight_image,
                'attack_speed' : 180,
                'damage' : 20
            }
        }

    def make_knight(self, pos, type):
        self.knights.append(hero(type, self, pos))

    def frame_check(self):
            for hero in self.knights:
                hero.frame_check()

    def render_heros(self, screen):
        for hero in self.knights:
             screen.blit(hero.image, (hero.pos[0]*64-16, 160+hero.pos[1]*64), (96*hero.fx, 96*hero.fy, 96, 96))


    # screen.blit(troop_handeler.knight_types[knight[2]][1], (knight[0][0]*64-16, 160+knight[0][1]*64), (96*knight[1][0], 96*knight[1][1], 96, 96))