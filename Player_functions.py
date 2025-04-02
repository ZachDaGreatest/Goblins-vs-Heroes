import pygame
from random import choice

class player_functions():
    def __init__(self, goblin_handler, hero_handler, game_clock):
        self.goblin_handler = goblin_handler
        self.hero_handler = hero_handler
        self.game_clock = game_clock

        self.health = 3
        self.gold = 30
        self.previous_elims = 0
        self.state = ''
        self.gpe = 5    # gold per elim
    
        self.gold_mine_inactive = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Resources\\Gold Mine\\GoldMine_Inactive.png')
        self.gold_mine_active = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Resources\\Gold Mine\\GoldMine_Active.png')
        self.gold_mine = self.gold_mine_inactive

    def gold_check(self):
        self.gold += self.gpe*(self.goblin_handler.elims-self.previous_elims)
        self.previous_elims = self.goblin_handler.elims

    def payment_check(self, selected_troop):
        cost = self.hero_handler.hero_types[selected_troop]['cost']
        if cost <= self.gold:
            self.gold -= cost
            return True
        else:
            return False

    def debug_menu(self, screen, font):
        # this line is for testing frame rate based on object amounts
        info = [
            f'{self.goblin_handler.elims} elims',
            f'{len(self.hero_handler.heros)} knights',
            f'{len(self.goblin_handler.goblins)} goblins',
            f'{round(self.game_clock.get_fps(), 8)} fps',
            f'wave count {self.goblin_handler.iteration}',
            f'{self.gold} gold',
            f'{self.health} health',
            f'{pygame.mouse.get_pos()}',
            self.state
        ]
        for num in range(len(info)):
            item = info[num]
            stat = font.render(item, False, (255,0,0))
            screen.blit(stat, (640-200, 20*num))
    
    def make_heros(self):
        for x in range(7):
            for y in range(3):
                if x < 5:
                    self.hero_handler.make_hero((x,y), 'archer')
                elif x == 5:
                    self.hero_handler.make_hero((x,y), 'standard')
                else:
                    self.hero_handler.make_hero((x,y), 'pawn')

    def make_goblins(self):
        goblins = ['standard', 'heavy', 'fast']
        for y in range(3):
            self.goblin_handler.spawn_goblin((10,y), choice(goblins))

    def health_check(self):
        for goblin in self.goblin_handler.goblins:
            if goblin.pos[0] < -1:
                self.goblin_handler.goblins.remove(goblin)
                self.health -= 1
        if self.health <= 0:
            self.state = 'dead'

    def frame_check(self):
        self.health_check()
        self.gold_check()