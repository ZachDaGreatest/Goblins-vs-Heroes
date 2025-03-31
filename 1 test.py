import pygame
from random import randint, choice

# all of the sprites are loaded in while the banner is resized to fit the screen
grass = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Ground\\Tilemap_Flat.png')
banner = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Banners\\Banner_Connection_Up.png')
banner = pygame.transform.scale(banner, (64,64))
bridge = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Bridge\\Bridge_All.png')

# 10 * 5.625 64 pixel squares
# the tile map shows the program where to draw everything and is inverted both horizontaly and verticaly
tile_map = [
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 0, 0, 0, 0, 0, 3, 3, 3, 3]
]

# go through bit map and blit images to screen
def render_forground(screen):
    # HEIGHT is 360 and WIDTH is 640
    row_num = 0
    for row in tile_map:
        collum_num = 0
        row_num += 1
        for collum in row:
            collum_num += 1
            # 2 is the placeable ground
            if collum == 2:
                # crop height and width is to change the sprite for the edges of the island
                crop_height = 0
                crop_width = 128
                if row_num != 3: crop_height = 64
                if collum_num != 4: crop_width = 64
                screen.blit(grass, (640-64*collum_num, 360-64*row_num), (crop_width, crop_height, 64, 64))
            # 1 is the bridge goblins run across
            if collum == 1:
                # if the bridge is at the end of the row it has poles in the sprite
                if collum_num == 3:
                    screen.blit(bridge, (640-64*collum_num, 360-64*row_num), (16, 0, 64, 64))
                else:
                    screen.blit(bridge, (640-64*collum_num, 360-64*row_num), (64, 0, 64, 64))
            # 3 is a place holder for the shop ui
            # if collum == 3:
            #     screen.blit(banner, (640-64*collum_num, 328-64*row_num), (0, 0, 64, 64))

# this iterating through the images of an animation where all sprites are on one png
def frame_count_check(fx, fy, ff, fx_min, fx_max, fy_min, fy_max):
    # the frame count is updated
    ff += 1
    # the sprite is changed every 6 frames
    if ff >= 6:
        ff = 0
        fx += 1
    # if the image is the last image in the row, the row is moved down and the collum is set to the beginning
    if fx > fx_max:
        fx = fx_min
        fy += 1
        if fy > fy_max:
            fy = fy_min
            # the frame that the image is set back to the beginning it returns true alongside the updated values
            return fx, fy, ff, True
    return fx, fy, ff, False

# this function takes pixel cords from a click and turns it into game cords
def convert_to_game_cords(pos, scale_factor):
    x = pos[0]
    y = pos[1]
    new_x = int(x/64/scale_factor)
    new_y = int(round((y-126)/64/scale_factor, 0) - 1*scale_factor)
    return (new_x, new_y)

# this function takes game cords from logic and turns it into pixel cords
# most sprites need an offset from the true tile position
def convert_to_pixel_cords(pos, scale_factor, x_offset, y_offset):
    x = pos[0]
    y = pos[1]
    new_x = int(x*64*scale_factor)+x_offset
    new_y = int((150+y*64)*scale_factor)+y_offset
    return (new_x, new_y)


# gen algorithm for a row
def row_spawns():
    spawns = []
    for spawn in range(180):
        if spawn < 20:
            num = randint(0,40)
            if num == 40:
                spawns.append('standard')
            else:
                spawns.append(False)
        elif spawn < 60:
            num = randint(0,20)
            if num >= 19:
                spawns.append('standard')
            elif num == 18:
                spawns.append('fast')
            else:
                spawns.append(False)
        elif spawn < 120:
            num = randint(0,10)
            if num >= 9:
                spawns.append('standard')
            elif num == 8:
                spawns.append('fast')
            elif num == 7:
                spawns.append('heavy')
            else:
                spawns.append(False)
        elif spawn <= 180:
            num = randint(0,10)
            if num >= 9:
                spawns.append('standard')
            elif num >= 7:
                spawns.append('fast')
            elif num >= 5:
                spawns.append('heavy')
            else:
                spawns.append(False)
    return spawns

# the sound handler makes sure that the same effect isn't played multiple times in a single frame
class sound_handler():
    def __init__(self):
        self.sound_effects = {
            'sword' : pygame.mixer.Sound('sound fx\\sword sound.wav'),
            'hammer' : pygame.mixer.Sound('sound fx\\hammer sound.wav'),
            'bow' : pygame.mixer.Sound('sound fx\\bow sound.wav'),
            'hit' : pygame.mixer.Sound('sound fx\\hit sound.wav'),
            'goblin spawn' : pygame.mixer.Sound('sound fx\\spawn sound.mp3'),
            'hero spawn' : pygame.mixer.Sound('sound fx\\troop spawn.mp3'),
            'death' : [pygame.mixer.Sound('sound fx\\lego death.mp3'), pygame.mixer.Sound('sound fx\\roblox death.mp3'), pygame.mixer.Sound('sound fx\\scream death.mp3')],
            'torch' : pygame.mixer.Sound('sound fx\\whip.wav')
        }

        self.sword_available = True
        self.hammer_available = True
        self.bow_available = True
        self.hit_available = True
        self.goblin_spawn_available = True
        self.hero_spawn_available = True
        self.death_available = True
        self.torch_available = True

    def reset_availability(self):
        self.sword_available = True
        self.hammer_available = True
        self.bow_available = True
        self.hit_available = True
        self.goblin_spawn_available = True
        self.hero_spawn_available = True
        self.death_available = True
        self.torch_available = True

    def play(self, sound_type):
        if sound_type == 'sword' and self.sword_available:
            self.sword_available = False
            self.sound_effects[sound_type].play()

        if sound_type == 'hammer' and self.hammer_available:
            self.hammer_available = False
            self.sound_effects[sound_type].play()

        if sound_type == 'bow' and self.bow_available:
            self.bow_available = False
            self.sound_effects[sound_type].play()

        if sound_type == 'hit' and self.hit_available:
            self.hit_available = False
            self.sound_effects[sound_type].play()

        if sound_type == 'goblin spawn' and self.goblin_spawn_available:
            self.goblin_spawn_available = False
            self.sound_effects[sound_type].play()

        if sound_type == 'hero spawn' and self.hero_spawn_available:
            self.hero_spawn_available = False
            self.sound_effects[sound_type].play()

        if sound_type == 'death' and self.death_available:
            self.death_available = False
            choice(self.sound_effects[sound_type]).play()

        if sound_type == 'torch' and self.torch_available:
            self.torch_available = False
            self.sound_effects[sound_type].play()

# the hero class is the base object for all heros
class hero():
    # a hero needs its type, handler, and game pos
    def __init__(self, type, handler, pos, sound_handler):
        # type info is the dictionary with all type info
        self.type_info = handler.hero_types[type]
        # if it starts with an f it is for frame logic (animations)
        self.fx = 0
        self.fy = 0
        self.ff = 0
        # sets the hero type to the fed in type
        self.type = type
        # sets all info to the info difined in the type dictionary
        self.health = self.type_info['max_health']
        self.image = self.type_info['image']
        self.attack_speed = self.type_info['attack_speed']
        self.damage = self.type_info['damage']
        self.range = self.type_info['range']
        self.is_ranged = self.type_info['is ranged']
        self.sound = self.type_info['sound']
        # sets pos to the fed game cordinates (not based on pixels)
        self.pos = pos
        # sets state and state_frames to the default of 'idle' and 0
        self.state = 'idle'
        self.state_frames = 0
        # if the hero is ranged they have an arrow position, visibility, and damage
        if self.is_ranged:
            self.arrows = []
            self.arrow_damage = self.damage
            self.damage = 0
        # using the handler prevents overlap of sound attacks between objects
        self.sound_handler = sound_handler

    def frame_check(self, goblin_handler):
        # checks to make sure the hero is still alive
        if self.state != 'dead':
            self.health_check()
        # if the hero is idle it runs an attack check
        if self.state == 'idle':
            self.attack_check(goblin_handler)
        # if the hero isn't idle then tick down the frames left in that state
        if self.state != 'idle':
            self.state_frames -= 1
        # the dead state is the only state that needs multiple lines of animation
        # so if the state is dead then the max pos is increased
        if self.state == 'dead':
            min_y = 0
            max_y = 1
        else:
            min_y = 0
            max_y = 0
        if self.is_ranged and self.state == 'attacking':
            if self.state_frames == self.attack_speed-32:
                self.arrows.append(self.pos)
                self.sound_handler.play(self.sound)
            if self.state_frames > self.attack_speed-60:
                max_x = 7
            else:
                max_x = 5
        else:
            max_x = 5
        if self.state == 'attacking' and self.state_frames == self.attack_speed-18 and not self.is_ranged:
            self.sound_handler.play(self.sound)
            x, y = self.pos
            x_max = x + self.range
            goblin_handler.check_area(y, x, x_max, self.damage)
        if self.is_ranged:
            temp_arrows = self.arrows
            self.arrows = []
            for arrow in temp_arrows:
                x, y = arrow
                x += 1/10
                if not goblin_handler.check_area(y, x, x+.5, self.arrow_damage) and x < 11:
                    self.arrows.append((x,y))
                
        # the frame pos is updated
        self.fx, self.fy, self.ff, animation_reset = frame_count_check(self.fx, self.fy, self.ff, 0, max_x, min_y, max_y)
        # if the animation reset and the hero is dead it returns false which removes the hero
        if animation_reset == True and self.state == 'dead':
            return False
        # if the hero isn't idle, there are no more frames in its state, and it isn't dead it is set to idle
        if self.state != 'idle' and self.state_frames <= 0 and self.state != 'dead':
            self.state = 'idle'
        # if the hero didn't just finish the dead animation it will return true keeping the hero around
        return True
    
    def attack(self):
        # if the hero isn't doing anything it is now attacking
        if self.state == 'idle':
            self.state = 'attacking'
            self.fx = 0
            self.fy = 2
            if self.is_ranged:
                self.fy = 4
            # state_frames is the amount of frames before the hero returns to idle
            self.state_frames = self.attack_speed

    def attack_check(self, goblin_handler):
        if self.state == 'idle':
            x, y = self.pos
            x_max = x + self.range
            if goblin_handler.check_area(y, x, x_max, 0):
                self.attack()

    def health_check(self):
        # if the hero's health is 0 or less the state is set to dead and the animation pos is reset
        if self.health <= 0:
            if self.state != 'dead':
                self.fx = 0
                self.fy = 0
                self.state = 'dead'
                self.sound_handler.play('death')
    
    # this allows outside functions to interact with the health of a hero
    def take_damage(self, damage):
        self.sound_handler.play('hit')
        self.health -= damage

# the hero handler is for doing things with every hero
# Ex: drawing sprites, checking occupied spaces, preforming frame checks
class hero_handler():
    def __init__(self, sound_handler):
        # all images have to be loaded and scaled down by 50%
        self.knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Warrior\\Blue\\Warrior_Blue.png')
        self.knight_image = pygame.transform.scale_by(self.knight_image, .5)
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
                'is ranged' : False
            },
            'pawn' : {
                'max_health' : 60,
                'image' : self.pawn_image,
                'sound' : 'hammer',
                'attack_speed' : 60,
                'damage' : 10,
                'range' : 1,
                'is ranged' : False
            },
            'archer' : {
                'max_health' : 25,
                'image' : self.archer_image,
                'sound' : 'bow',
                'attack_speed' : 120,
                'damage' : 10,
                'range' : 10,
                'is ranged' : True
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

class goblin():
    # a goblin needs its type, handler, and game pos
    def __init__(self, type, handler, pos, sound_handler):
        # type info is the dictionary with all type info
        self.type_info = handler.goblin_types[type]
        # if it starts with an f it is for frame logic (animations)
        self.fx = 0
        self.fy = 1
        self.ff = 0
        # sets the goblin type to the fed in type
        self.type = type
        # sets all info to the info difined in the type dictionary
        self.health = self.type_info['max_health']
        self.image = self.type_info['image']
        self.attack_speed = self.type_info['attack_speed']
        self.damage = self.type_info['damage']
        self.speed = self.type_info['speed']
        self.range = self.type_info['range']
        # sets pos to the fed game cordinates (not based on pixels)
        self.pos = pos
        # sets state and state_frames to the default of 'idle' and 0
        self.state = 'idle'
        self.state_frames = 0
        # animation inverted is to play the running animation
        self.animation_invert = False
        # using the handler prevents overlap of sound attacks between objects
        self.sound_handler = sound_handler

    def frame_check(self, hero_handler):
        # checks to make sure the goblin is still alive
        if self.state != 'dead':
            self.health_check()
        # if the goblin is idle it runs an attack check
        if self.state == 'idle':
            self.attack_check(hero_handler)
        # if the goblin isn't idle then tick down the frames left in that state
        if self.state != 'idle':
            self.state_frames -= 1
        else:
            self.move(self.speed)
        # the attack sound and damage are delayed from the start of the animation
        if self.state == 'attacking' and self.state_frames == self.attack_speed-18:
            self.sound_handler.play('torch')
            x_max, y = self.pos
            x = x_max - self.range
            hero_handler.check_area(y, x, x_max, self.damage)
        # the dead state is the only state that needs multiple lines of animation
        # so if the state is dead then the max pos is increased
        if self.state == 'dead':
            min_y = 0
            max_y = 1
        elif self.state == 'attacking':
            min_y = 0
            max_y = 0
        else:
            min_y = 1
            max_y = 1
        if self.animation_invert:
            max_x = 3
        else:
            max_x = 5
        # the frame pos is updated
        self.fx, self.fy, self.ff, animation_reset = frame_count_check(self.fx, self.fy, self.ff, 1, max_x, min_y, max_y)
        # if the animation reset and the goblin is dead it returns false which removes the goblin
        if animation_reset == True and self.state == 'dead':
            return False
        if animation_reset == True and self.state == 'idle':
            self.animation_invert = not self.animation_invert
        # if the goblin isn't idle, there are no more frames in its state, and it isn't dead it is set to idle
        if self.state != 'idle' and self.state_frames <= 0 and self.state != 'dead':
            self.state = 'idle'
            self.fy = 1
        if self.pos[0] < -1:
            self.state = 'dead'
            # TODO make it so this damages the player
        # if the goblin didn't just finish the dead animation it will return true keeping the goblin around
        return True
    
    def attack(self):
        # if the goblin isn't doing anything it is now attacking
        if self.state == 'idle':
            self.state = 'attacking'
            self.fx = 1
            self.fy = 2
            # state_frames is the amount of frames before the goblin returns to idle
            self.state_frames = self.attack_speed
            self.animation_invert = False
    
    def attack_check(self, hero_handler):
        if self.state == 'idle':
            x_max, y = self.pos
            x = x_max - self.range
            if hero_handler.check_area(y, x, x_max, 0):
                self.attack()

    def health_check(self):
        # if the goblin's health is 0 or less the state is set to dead and the animation pos is reset
        if self.health <= 0:
            if self.state != 'dead':
                self.fx = 0
                self.fy = 0
                self.state = 'dead'
                self.animation_invert = False
                self.sound_handler.play('death')
    
    # this allows outside functions to interact with the health of a goblin
    def take_damage(self, damage):
        self.health -= damage
    
    def move(self, speed):
        x,y = self.pos
        self.pos = (x-speed, y)

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

# this file will eventually be turned into a funtion for the menu to call

# FIXME there are random stuters, 
'''
I have individualy commented out every line in the program and it still happens
if event handler is commented out the program crashes when there would be a lag spike
the old code runs fine
seems like it is caused by poor optomization since it only occurs when on battery and not when plugged in
'''

# TODO include the seed here at the top with random.seed()

# all functions/classes are initiated
pygame.init()
pygame.font.init()
font = pygame.font.Font('slkscr.ttf', 18)
pygame.mixer.init()
sound_manager = sound_handler()
troop_handler = hero_handler(sound_manager)
enemy_handler = goblin_handler(sound_manager)
game_clock = pygame.time.Clock()
pygame.mixer.music.load('music\\fear.mp3')
pygame.mixer.music.set_volume(.8)
pygame.mixer.music.play()


gold_mine_inactive = pygame.image.load('Tiny Swords\Tiny Swords (Update 010)\Resources\Gold Mine\GoldMine_Inactive.png')
gold_mine_active = pygame.image.load('Tiny Swords\Tiny Swords (Update 010)\Resources\Gold Mine\GoldMine_Active.png')
gold_mine = gold_mine_inactive


def make_heros():
    for x in range(7):
        for y in range(3):
            if x < 5:
                troop_handler.make_hero((x,y), 'archer')
            else:
                troop_handler.make_hero((x,y), 'standard')

goblins = ['standard', 'heavy', 'fast']
def make_goblins():
    for y in range(3):
        enemy_handler.spawn_goblin((10,y), choice(goblins))

# all screen initiation is temporary and will be moved to main
# screen is the object that gets drawn on, then it is scaled onto display
# 360 * 640 is the standard ratio which is 16/9
# scale factor is used for anything that uses screen units
# getting display info before setup gets monitor screen size which is used for auto fill fullscreen
WIDTH = pygame.display.Info().current_w
HEIGHT = WIDTH*9/16
scale_factor = HEIGHT/360
display = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface((640, 360))
pygame.display.set_caption('Heros vs Goblins')
pygame.display.toggle_fullscreen()
frame = 0
f_goal = 60
iteration = 0

top_row = row_spawns()
middle_row = row_spawns()
bottom_row = row_spawns()

# the while loop is whaere the game happens
gamin = True
while gamin:
    # if the music isn't playing it is started again
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
    # tick sets the fps, the game is built around 60 fps
    game_clock.tick(60)

    # this is a basic enemy spawn system
    # TODO move into goblin handler and add seeds
    frame += 1
    if frame % f_goal == 0 and iteration < 180:
        # make_goblins()
        goblin_type = top_row[iteration]
        if goblin_type != False:
            enemy_handler.spawn_goblin((10,0), goblin_type)
        goblin_type = middle_row[iteration]
        if goblin_type != False:
            enemy_handler.spawn_goblin((10,1), goblin_type)
        goblin_type = bottom_row[iteration]
        if goblin_type != False:
            enemy_handler.spawn_goblin((10,2), goblin_type)
        iteration += 1

    # use this section for economy code
    if iteration > 20:
        gold_mine = gold_mine_active

    # event handeler is for all imputs
    for event in pygame.event.get():
        # pressing escape stops the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gamin = False
            # using v to spawn knights and space to make them attack is used for debugging
            if event.key == pygame.K_v:
                make_heros()
                # using v to spawn goblins and space to make them attack is used for debugging
            if event.key == pygame.K_b:
                make_goblins()
            if event.key == pygame.K_SPACE:
                troop_handler.attack()
                enemy_handler.attack()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x, y = convert_to_game_cords((x,y), scale_factor)
            if troop_handler.check_empty((x,y), scale_factor, True):
                troop_handler.make_hero((x,y), 'pawn')
            # example of using check empty, prints false if hero is in square/it isn't swapnable
            # animation testing, if you click near a hero they die, otherwise places hero
            # could be an example of the way a shop place function would work
            elif not troop_handler.check_empty(pygame.mouse.get_pos(), scale_factor, False):
                for hero in troop_handler.heros:
                    if hero.pos == (x,y):
                        hero.attack()
                        hero.take_damage(100)
            for goblin in enemy_handler.goblins:
                x, y = pygame.mouse.get_pos()
                gx, gy = convert_to_pixel_cords(goblin.pos, scale_factor, 32, 48)
                if x-24 < gx < x+24 and y-24 < gy < y+24:
                    goblin.take_damage(40)
            
        # clicking the x stops the game
        if event.type == pygame.QUIT:
            gamin = False

    # frame check is where most game functions occur
    troop_handler.frame_check(enemy_handler)
    enemy_handler.frame_check(troop_handler)

    # the screen is drawn over with a solid color and then all objects are drawn on
    screen.fill((0,255,255))
    render_forground(screen)
    screen.blit(gold_mine, (0, 88))
    troop_handler.render_heros(screen)
    enemy_handler.render_goblins(screen)

    # this line is for testing frame rate based on object amounts
    info = f'{enemy_handler.elims} elims : {len(troop_handler.heros)} knights and {len(enemy_handler.goblins)} goblins : {round(game_clock.get_fps(), 8)} fps'
    stats = font.render(info, False, (255,0,0))
    screen.blit(stats, (0,0))
    
    s = font.render(str(iteration), False, (0,0,0))
    screen.blit(s, (0,20))

    # the screen that has everything drawn on it is scaled and put on the actual display
    # temp_screen stores the transformed screen without changing the scale of screen
    temp_screen = pygame.transform.scale_by(screen, scale_factor)
    display.blit(temp_screen, (0,0))

    # this alows all sound fx that have been played to be played next frame
    if frame % 5 == 0:
        sound_manager.reset_availability()

    # this updates the screen to all of the changes
    pygame.display.flip()