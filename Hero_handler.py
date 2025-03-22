import pygame
from Hero import hero
from commands import convert_to_game_cords, convert_to_pixel_cords

# the hero handeler is for doing things with every hero
# Ex: drawing sprites, checking occupied spaces, preforming frame checks
class hero_handler():
    def __init__(self):
        # all images have to be loaded and scaled down by 50%
        self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Warrior\\Blue\\Warrior_Blue.png')
        self.knight_image = pygame.transform.scale_by(self.knight_image, .5)
        self.skull_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Dead\\Dead.png')
        self.skull_image = pygame.transform.scale_by(self.skull_image, .5)
        self.pawn_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Pawn\\Blue\\Pawn_Blue.png')
        self.pawn_image = pygame.transform.scale_by(self.pawn_image, .5)

        # heros is the list of all hero objects
        self.heros = []

        # this dictionary gives all info for hero types that doesn't change 
        # Ex: health changes depending on the hero so it isn't included, max health is constant across a type so it is included
        self.hero_types = {
            'standard' : {
                'max_health' : 100,
                'image' : self.knight_image,
                'attack_speed' : 120,
                'damage' : 20
            }
        }

    # this should be called by the shop
    def make_hero(self, pos, type):
        self.heros.append(hero(type, self, pos))

    # the hero.frame_check returns false if they have 0 health or less
    def frame_check(self):
            for hero in self.heros:
                if hero.frame_check() == False:
                    self.heros.remove(hero)

    # if the hero is dead the image is smaller so it needs a different blit command
    def render_heros(self, screen):
        for hero in self.heros:
            if hero.state != 'dead':
                screen.blit(hero.image, convert_to_pixel_cords(hero.pos, 1, -16, 0), (96*hero.fx, 96*hero.fy, 96, 96))
            else:
                screen.blit(self.skull_image, (convert_to_pixel_cords(hero.pos, 1, 0, 16)), (64*hero.fx, 64*hero.fy, 64, 64))

    # this command is for debugging
    def attack(self):
         for hero in self.heros:
            hero.attack()
    
    # feed a click pos (pixel based) and it will check if there is a hero at that pos
    # if a hero is at the position it returns false since the space is not empty
    # everything based on screen units needs to be multiplied by a scale factor (sf)
    def check_empty(self, pos, sf):
        for hero in self.heros:
            if convert_to_game_cords(pos, sf) == hero.pos:
                return False
        return True