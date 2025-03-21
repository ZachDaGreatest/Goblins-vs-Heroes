from commands import frame_count_check

class hero():
    def __init__(self, type, handeler, pos):
        self.type_info = handeler.knight_types[type]

        self.fx = 0
        self.fy = 0
        self.ff = 0
        self.type = type
        self.health = self.type_info['max_health']
        self.image = self.type_info['image']
        self.attack_speed = self.type_info['attack_speed']
        self.damage = self.type_info['damage']
        self.pos = pos
        self.state = 'idle'

    def frame_check(self):
        self.health_check()
        if self.state == 'idle': 
            min_y = 0
            max_y = 0
        if self.state == 'attacking':
            min_y = 0
            max_y = 0
        if self.state == 'dead':
            min_y = 0
            max_y = 1
        self.fx, self.fy, self.ff, animation_reset = frame_count_check(self.fx, self.fy, self.ff, min_y, max_y)
        if animation_reset == True and self.state == 'dead':
            return False
        if animation_reset == True and self.state != 'idle':
            self.state = 'idle'
        return True
    
    def attack(self):
        if self.state == 'idle':
            self.state = 'attacking'
            self.fx = 0
            self.fy = 2

    def health_check(self):
        if self.health <= 0:
            if self.state != 'dead':
                self.fx = 0
                self.fy = 0
                self.state = 'dead'
        
    def take_damage(self, damage):
        self.health -= damage