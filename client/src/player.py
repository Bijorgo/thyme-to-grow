# player.py
import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group): 
        super().__init__(group)

        # Set up sprite img and rect
        self.image = pygame.Surface((32, 64)) # for testing
        self.image.fill('black') # for testing
        self.rect = self.image.get_rect( center = pos )  # Set rect with position

        # movement
        self.direction = pygame.math.Vector2() # default () = (0,0)
        self.pos = pygame.math.Vector2(self.rect.center) # store in vector to avoid float issue 
        self.speed = 250

    def input(self):
        keys = pygame.key.get_pressed()

        # define movement up/down
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # define movement left/right
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        

    def move(self, delta_time):
        # Movement in diagonal direction is faster than l/r/u/d...I'm fine with it for now, consider changing
        # normalize vector 

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * delta_time
        self.rect.centerx = self.pos.x
        # Vertical movement 
        self.pos.y += self.direction.y * self.speed * delta_time
        self.rect.centery = self.pos.y


    def update(self, delta_time):
        self.input()
        self.move(delta_time)
 

       