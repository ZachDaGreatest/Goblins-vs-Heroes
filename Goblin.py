from commands import frame_count_check
import pygame

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