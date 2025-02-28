import pygame
from config import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Menu(pygame.sprite.Sprite):
    def __init__ (self, pos, surface, groups, z = LAYERS['ground']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Plants(pygame.sprite.Sprite):
    def __init__ (self, pos, surface, groups, cultivate_plants, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.image.fill((0, 255, 0))  # Green square for the plant for testing
        self.cultivate_plants_obj = cultivate_plants # Store cultivate plant object 