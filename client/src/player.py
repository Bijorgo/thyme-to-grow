# player.py
import pygame
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, group, pos): #, x, y, character_img
        super().__init__(group)

        # Set up sprite img and rect
        self.image = pygame.Surface((64, 32)) # for testing
        self.image.fill('black') # for testing
        #self.image = character_img
        # Ensure pos is a tuple with two integers (x, y) coordinates
        
        self.rect = self.image.get_rect( center = pos )  # Set rect with position
 
        self.rect = self.image.get_rect()
        group.add(self) 

        #self.x = x
        #self.y = y
        
        #self.moving_right = False
        #self.moving_left = False
        #self.moving_up = False
        #self.moving_down = False

        #group.add_internal(self) # add this player instance to its group

    #def handle_keys(self, event):
        #"""Handle key events to move the player."""
        # Consider replacing movement with pygame.math => Vector 2
        #if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_RIGHT:
                #self.moving_right = True
            #if event.key == pygame.K_LEFT:
                #self.moving_left = True
            #if event.key == pygame.K_UP:
                #self.moving_up = True
            #if event.key == pygame.K_DOWN:
                #self.moving_down = True

        #if event.type == pygame.KEYUP:
            #if event.key == pygame.K_RIGHT:
                #self.moving_right = False
            #if event.key == pygame.K_LEFT:
                #self.moving_left = False
            #if event.key == pygame.K_UP:
                #self.moving_up = False
            #if event.key == pygame.K_DOWN:
                #self.moving_down = False

    #def move(self, delta_time):
        #"""Update player position based on movement flags."""
        #if self.moving_right:
            #self.rect.x += 100 * delta_time
        #if self.moving_left:
            #self.rect.x -= 100 * delta_time
        #if self.moving_down:
            #self.rect.y += 100 * delta_time
        #if self.moving_up:
            #self.rect.y -= 100 * delta_time

    #def draw(self, screen):
        #"""Draw the player character on the screen."""
        #screen.blit(self.image, self.rect)  # Blit image at its rect position
