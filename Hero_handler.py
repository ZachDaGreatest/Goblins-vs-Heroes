import pygame
from Hero import hero
from commands import convert_to_game_cords, convert_to_pixel_cords

# the hero handler is for doing things with every hero
# Ex: drawing sprites, checking occupied spaces, preforming frame checks
class hero_handler():
    def __init__(self, sound_handler):
        # all images have to be loaded and scaled down by 50%
        self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Warrior\\Blue\\Warrior_Blue.png')
        self.knight_image = pygame.transform.scale_by(self.knight_image, .5)

        self.archer_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Archer\\Archer + Bow\Archer_Blue_(NoArms).png')
        self.archer_image = pygame.transform.scale_by(self.archer_image, .5)
        
        self.archer_bow = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Archer\\Archer + Bow\\Archer_Bow_Blue.png')
        self.archer_bow = pygame.transform.scale_by(self.archer_bow, .5)

        self.skull_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Dead\\Dead.png')
        self.skull_image = pygame.transform.scale_by(self.skull_image, .5)

        self.pawn_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Pawn\\Blue\\Pawn_Blue.png')
        self.pawn_image = pygame.transform.scale_by(self.pawn_image, .5)
        self.archer_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Archer\\Blue\\Archer_Blue.png')
        self.archer_image = pygame.transform.scale_by(self.archer_image, .5)
        self.arrow_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Archer\\Arrow\\Arrow.png')
        self.arrow_image = pygame.transform.scale_by(self.arrow_image, .5)

        # heros is the list of all hero objects
        self.heros = []

        # using the handler prevents overlap of sound attacks between objects
        self.sound_handler = sound_handler

        # this dictionary gives all info for hero types that doesn't change 
        # Ex: health changes depending on the hero so it isn't included, max health is constant across a type so it is included
        self.hero_types = {
            'standard' : {
                'max_health' : 100,
                'image' : self.knight_image,
                'sound' : 'sword',
                'attack_speed' : 120,
                'damage' : 80,
                'range' : 1,
                'is ranged' : False,
                'cost' : 20
            },
            'pawn' : {
                'max_health' : 60,
                'image' : self.pawn_image,
                'sound' : 'hammer',
                'attack_speed' : 60,
                'damage' : 10,
                'range' : 1,
                'is ranged' : False,
                'cost': 10
            },
            'archer' : {
                'max_health' : 10,
                'image' : self.archer_image,
                'sound' : 'bow',
                'attack_speed' : 120,
                'damage' : 10,
                'range' : 10,
                'is ranged' : True,
                'cost' : 25
            }
        }

    # this should be called by the shop
    def make_hero(self, pos, type):
        self.sound_handler.play('hero spawn')
        self.heros.append(hero(type, self, pos, self.sound_handler))

    # the hero.frame_check returns false if they have 0 health or less
    def frame_check(self, goblin_handler):
            for hero in self.heros:
                if hero.frame_check(goblin_handler) == False:
                    self.heros.remove(hero)

    # if the hero is dead the image is smaller so it needs a different blit command
    def render_heros(self, screen):
        for hero in self.heros:
            if hero.state != 'dead':
                screen.blit(hero.image, convert_to_pixel_cords(hero.pos, 1, -16, 0), (96*hero.fx, 96*hero.fy, 96, 96))
                if hero.is_ranged:
                    for arrow in hero.arrows:
                        screen.blit(self.arrow_image, convert_to_pixel_cords(arrow, 1, 16, 36), (0, 0, 32, 32))

            else:
                screen.blit(self.skull_image, convert_to_pixel_cords(hero.pos, 1, 0, 16), (64*hero.fx, 64*hero.fy, 64, 64))
    # this command is for debugging
    def attack(self):
         for hero in self.heros:
            hero.attack()
    
    # feed a click pos (pixel based) and it will check if there is a hero at that pos
    # pos needs to be converted from pixel cords to game cords
    def check_empty(self, pos, sf, is_game_cords):
        if not is_game_cords:
            x,y = convert_to_game_cords(pos, sf)
        else:
            x,y = pos
        # if the space is not part of the spawnable grid it returns false
        if x > 6 or y < 0:
            return False
        # if a hero is at the position it returns false since the space is not empty
        for hero in self.heros:
            if (x,y) == hero.pos:
                return False
        return True
    
    def damage_hero(self, pos, damage):
        for hero in self.heros:
            if hero.pos == pos:
                hero.take_damage(damage)

    def check_area(self, row, collum_start, collum_end, damage):
        for hero in self.heros:
            hx, hy = hero.pos
            if row == hy:
                if collum_start < hx < collum_end:
                    if hero.state != 'dead':
                        hero.take_damage(damage)
                        return True
        return False