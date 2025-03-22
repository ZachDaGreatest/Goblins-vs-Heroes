from commands import frame_count_check

# the hero class is the base object for all heros
class hero():
    # a hero needs its type, handeler, and game pos
    def __init__(self, type, handeler, pos):
        # type info is the dictionary with all type info
        self.type_info = handeler.hero_types[type]
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
        # sets pos to the fed game cordinates (not based on pixels)
        self.pos = pos
        # sets state and state_frames to the default of 'idle' and 0
        self.state = 'idle'
        self.state_frames = 0

    def frame_check(self):
        # checks to make sure the hero is still alive
        self.health_check()
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
        # the frame pos is updated
        self.fx, self.fy, self.ff, animation_reset = frame_count_check(self.fx, self.fy, self.ff, min_y, max_y)
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
            # state_frames is the amount of frames before the hero returns to idle
            self.state_frames = self.attack_speed

    def health_check(self):
        # if the hero's health is 0 or less the state is set to dead and the animation pos is reset
        if self.health <= 0:
            if self.state != 'dead':
                self.fx = 0
                self.fy = 0
                self.state = 'dead'
    
    # this allows outside functions to interact with the health of a hero
    def take_damage(self, damage):
        self.health -= damage