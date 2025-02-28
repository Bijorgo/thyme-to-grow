# player.py
import pygame
from config import *
from src.fetching import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, name="Player"): 
        super().__init__(group)

        # Set up sprite img and rect
        self.image = pygame.Surface((32, 64)) # for testing
        self.image.fill('black') # for testing
        self.rect = self.image.get_rect( center = pos )  # Set rect with position
        self.z = LAYERS['main'] # Refers to layer in config, ref x, y, z pos

        # player attributes
        self.name = name 
        self.font = pygame.font.Font(None, 24)  # Font for displaying names
        self.text_surface = self.font.render(self.name, True, (255, 255, 255))  # Render text in white
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.top - 10)) #position name above player  # Position text

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

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Draw the player sprite
        surface.blit(self.text_surface, self.text_rect)  # Draw the player's name above the player


    def update(self, delta_time):
        self.input()
        self.move(delta_time)
 