import pygame
from commands import frame_count_check
from Hero import hero

class knight_handeler():
    def __init__(self):
        self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Warrior\\Blue\\Warrior_Blue.png')
        self.skull_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Dead\\Dead.png')
        self.skull_image = pygame.transform.scale_by(self.skull_image, .5)
        # self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Goblins\\Troops\\Torch\\Blue\\Torch_Blue.png')
        # self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Pawn\\Blue\\Pawn_Blue.png')
        self.knight_image = pygame.transform.scale_by(self.knight_image, .5)
        # each knight has a (position), image, and (frame position)
        self.heros = []

        self.knight_types = {
            'standard' : {
                'max_health' : 100,
                'image' : self.knight_image,
                'attack_speed' : 120,
                'damage' : 20
            }
        }

    def make_knight(self, pos, type):
        self.heros.append(hero(type, self, pos))

    def frame_check(self):
            for hero in self.heros:
                if hero.frame_check() == False:
                    self.heros.remove(hero)

    def render_heros(self, screen):
        for hero in self.heros:
            if hero.state != 'dead':
                screen.blit(hero.image, (hero.pos[0]*64-16, 150+hero.pos[1]*64), (96*hero.fx, 96*hero.fy, 96, 96))
            else:
                screen.blit(self.skull_image, (hero.pos[0]*64, 166+hero.pos[1]*64), (64*hero.fx, 64*hero.fy, 64, 64))

    def attack(self):
         for hero in self.heros:
            hero.attack()
    
    def check_empty(self, pos):
        for hero in self.heros:
            if (pos[0]-.5 < hero.pos[0] < pos[0]+.5) and (pos[1]-.5 < hero.pos[1] < pos[1]+.5):
                return False
        return True