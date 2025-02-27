# player.py
import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos): #, x, y, character_img
        super().__init__(group)

        # Set up sprite img and rect
        self.image = pygame.Surface((64, 32)) # for testing
        self.image.fill('black') # for testing
        
        self.rect = self.image.get_rect( center = pos )  # Set rect with position
 
        self.rect = self.image.get_rect()
        group.add(self) 

       