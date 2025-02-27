import pygame
from src.game import Game  # Import the Game class

pygame.init()

# Create the game object
game = Game()

# Start the game loop
game.run()

pygame.quit()
