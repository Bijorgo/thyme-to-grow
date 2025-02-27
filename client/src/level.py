import pygame
from config import *
from src.player import Player
from src.sprites import Generic

class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = CameraGroup()

        # Setup player
        self.setup()

    def setup(self):
        Generic(
            pos = (0,0),
            surface = pygame.image.load('src/assets/bg2.png').convert_alpha(),
            groups = self.all_sprites
        )
        # Create player and add to the all_sprites group
        self.player = Player((640, 360), self.all_sprites)  # Pass position, group

    def run(self, delta_time):
        self.display_surface.fill('green') # background
        #self.all_sprites.draw(self.display_surface) # Draw sprites on screen
        self.all_sprites.custom_draw()
        self.all_sprites.update(delta_time)  # Update all sprites

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)
        