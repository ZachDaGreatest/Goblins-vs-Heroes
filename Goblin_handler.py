import pygame
from commands import convert_to_pixel_cords
from Goblin import goblin

class goblin_handler():
    def __init__(self):
        # all images have to be loaded and scaled down by 50%, goblins need to be flipped to face the right way
        self.goblin_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Goblins\\Troops\\Torch\\Blue\\Torch_Blue.png')
        self.goblin_image = pygame.transform.scale_by(self.goblin_image, .5)
        self.goblin_image = pygame.transform.flip(self.goblin_image, True, False)
        self.skull_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Dead\\Dead.png')
        self.skull_image = pygame.transform.scale_by(self.skull_image, .5)

        # goblins is the list of all goblin objects
        self.goblins = []

        # this dictionary gives all info for goblins types that doesn't change 
        # Ex: health changes depending on the goblin so it isn't included, max health is constant across a type so it is included
        self.goblin_types = {
            'standard' : {
                'max_health' : 40,
                'image' : self.goblin_image,
                'attack_speed' : 120,
                'damage' : 5,
                'speed' : 1/120,
                'range' : 1
            }
        }
    
    def spawn_goblin(self, pos, type):
        self.goblins.append(goblin(type, self, pos))

    def frame_check(self, hero_handler):
        for goblin in self.goblins:
            if goblin.frame_check(hero_handler) == False:
                self.goblins.remove(goblin)

    # if the goblin is dead the image is smaller so it needs a different blit command
    def render_goblins(self, screen):
        for goblin in self.goblins:
            if goblin.state != 'dead':
                if goblin.animation_invert:
                    screen.blit(goblin.image, convert_to_pixel_cords(goblin.pos, 1, -16, 0), ((96*goblin.fx)+192, 96*goblin.fy, 96, 96))
                else:
                    screen.blit(goblin.image, convert_to_pixel_cords(goblin.pos, 1, -16, 0), (672-(96*goblin.fx), 96*goblin.fy, 96, 96))
            else:
                screen.blit(self.skull_image, (convert_to_pixel_cords(goblin.pos, 1, 0, 16)), (64*goblin.fx, 64*goblin.fy, 64, 64))
    
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
                    goblin.take_damage(damage)
                    return True
        return False