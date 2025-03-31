import pygame
from random import choice

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