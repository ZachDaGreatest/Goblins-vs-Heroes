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
        self.image_state = 'idle'

        print(self.health)

    def frame_check(self):
        if self.image_state == 'idle': 
            min_y = 0
            max_y = 0
        self.fx, self.fy, self.ff = frame_count_check(self.fx, self.fy, self.ff, min_y, max_y)