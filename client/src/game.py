import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from src.player import Player
from src.level import Level

class Game:
    def __init__(self):
        pygame.init() # inits modules required to run (display, mixer, font, joystick, image, key, mouse)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # top left = (0,0) middle = x/2, y/2
        pygame.display.set_caption("Thyme to Grow") # Set title in window bar
        self.clock = pygame.time.Clock() # Create game clock
        self.running = True
        self.level = Level()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                # Allow window to close
                if event.type == pygame.QUIT:
                    self.running = False
            # Frame rate
            delta_time = self.clock.tick(60) / 1000 
            delta_time = max(0.001, min(0.1, delta_time))
            self.level.run(delta_time) # before updating display, run level
            pygame.display.update()

        pygame.quit()

