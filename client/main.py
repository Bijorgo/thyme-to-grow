import pygame
from src.game import Game  # Import the Game class
from src.objects import MainMenuButton
#from src.level import Level

if __name__ == '__main__':
    game= Game () #Create game instance, inits display ( must be before loading imgs )
    game.run()

pygame.quit()
