import pygame
from config import *
from src.player import Player

class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()

        # Setup player
        self.setup()

    def setup(self):
        # Create player and add to the all_sprites group
        image = pygame.Surface((64, 32))  # Just a placeholder for now
        image.fill('white')  # Use a white box as the player image (just for testing)
        self.player = Player(self.all_sprites, (640, 360))  # Pass group and position

    def run(self, delta_time):
        self.display_surface.fill('green')
        self.all_sprites.update()  # Update all sprites
        self.all_sprites.draw(self.display_surface) # Draw sprites on screen