import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.menu import MenuPage

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Thyme to Grow")
        self.running = True

    def run(self):
        while self.running:
            menu = MenuPage()
            menu.run()  # Start menu loop

            # After menu loop exits, check if the game should continue
            if not menu.running:
                self.running = False

        pygame.quit()
