import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR
from src.player import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            # top left = (0,0)
            # middle = (960, 540) => x/2, y/2
        pygame.display.set_caption("Thyme to Grow")
        self.clock = pygame.time.Clock()
        self.running = True
        #self.player = Player(300, 300)

    def handle_events(self):
        for event in pygame.event.get():
            # Allow window to close
            if event.type == pygame.QUIT:
                self.running = False