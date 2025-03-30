from commands import frame_count_check

# the hero class is the base object for all heros
class hero():
    # a hero needs its type, handler, and game pos
    def __init__(self, type, handler, pos):
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

    def frame_check(self, goblin_handler):
        # checks to make sure the hero is still alive
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
            if self.state_frames == self.attack_speed-36:
                self.arrows.append(self.pos)
            if self.state_frames > self.attack_speed-60:
                max_x = 7
            else:
                max_x = 5
        else:
            max_x = 5
        if self.is_ranged:
            temp_arrows = self.arrows
            self.arrows = []
            for arrow in temp_arrows:
                x, y = arrow
                x += 1/10
                if not goblin_handler.check_area(y, x, x+.5, self.arrow_damage):
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
            if goblin_handler.check_area(y, x, x_max, self.damage):
                self.attack()

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