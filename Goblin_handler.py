import pygame
from commands import convert_to_pixel_cords
from Goblin import goblin

class goblin_handler():
    def __init__(self, sound_handler):
        # all images have to be loaded and scaled down by 50%, goblins need to be flipped to face the right way
        self.blue_goblin_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Goblins\\Troops\\Torch\\Blue\\Torch_Blue.png')
        self.blue_goblin_image = pygame.transform.scale_by(self.blue_goblin_image, .5)
        self.blue_goblin_image = pygame.transform.flip(self.blue_goblin_image, True, False)
        self.purple_goblin_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Goblins\\Troops\\Torch\\Purple\\Torch_Purple.png')
        self.purple_goblin_image = pygame.transform.scale_by(self.purple_goblin_image, .5)
        self.purple_goblin_image = pygame.transform.flip(self.purple_goblin_image, True, False)
        self.red_goblin_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Goblins\\Troops\\Torch\\Red\\Torch_Red.png')
        self.red_goblin_image = pygame.transform.scale_by(self.red_goblin_image, .5)
        self.red_goblin_image = pygame.transform.flip(self.red_goblin_image, True, False)
        self.skull_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Dead\\Dead.png')
        self.skull_image = pygame.transform.scale_by(self.skull_image, .5)
        self.skull_image = pygame.transform.flip(self.skull_image, True, False)
        
        self.sound_handler = sound_handler

        self.elims = 0

        # goblins is the list of all goblin objects
        self.goblins = []

        # this dictionary gives all info for goblins types that doesn't change 
        # Ex: health changes depending on the goblin so it isn't included, max health is constant across a type so it is included
        self.goblin_types = {
            'standard' : {
                'max_health' : 40,
                'image' : self.blue_goblin_image,
                'attack_speed' : 120,
                'damage' : 5,
                'speed' : 1/120,
                'range' : 1
            },
            'fast' : {
                'max_health' : 10,
                'image' : self.purple_goblin_image,
                'attack_speed' : 60,
                'damage' : 5,
                'speed' : 1/45,
                'range' : 1
            },
            'heavy' : {
                'max_health' : 80,
                'image' : self.red_goblin_image,
                'attack_speed' : 180,
                'damage' : 30,
                'speed' : 1/180,
                'range' : 1
            }
        }
    
    def spawn_goblin(self, pos, type):
        self.goblins.append(goblin(type, self, pos, self.sound_handler))
        self.sound_handler.play('goblin spawn')

    def frame_check(self, hero_handler):
        for goblin in self.goblins:
            if goblin.frame_check(hero_handler) == False:
                self.goblins.remove(goblin)
                self.elims += 1

    # if the goblin is dead the image is smaller so it needs a different blit command
    def render_goblins(self, screen):
        for goblin in self.goblins:
            if goblin.state != 'dead':
                if goblin.animation_invert:
                    screen.blit(goblin.image, convert_to_pixel_cords(goblin.pos, 1, -16, 0), ((96*goblin.fx)+192, 96*goblin.fy, 96, 96))
                else:
                    screen.blit(goblin.image, convert_to_pixel_cords(goblin.pos, 1, -16, 0), (672-(96*goblin.fx), 96*goblin.fy, 96, 96))
            else:
                screen.blit(self.skull_image, (convert_to_pixel_cords(goblin.pos, 1, 0, 16)), (384-64*goblin.fx, 64*goblin.fy, 64, 64))
    
    def attack(self):
        for goblin in self.goblins:
            goblin.attack()

    def damage_goblin(self, pos, damage):
        for goblin in self.goblins:
            if goblin.pos == pos:
                goblin.take_damage(damage)

    def check_area(self, row, collum_start, collum_end, damage):
        for goblin in self.goblins:
            gx, gy = goblin.pos
            if row == gy:
                if collum_start < gx < collum_end:
                    if goblin.state != 'dead':
                        goblin.take_damage(damage)
                        if damage > 0:
                            self.sound_handler.play('hit')
                        return True
        return False