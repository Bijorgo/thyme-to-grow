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
        # Load player img
        self.character_img = pygame.image.load("assets/charactersprite.png").convert_alpha()
        # Scale img
        self.character_img = pygame.transform.scale(self.character_img, 
            (self.character_img.get_width() * 4, self.character_img.get_height() * 4)
        )
        # init player w img
        self.player = Player(0, 320, self.character_img) # initial coordinates of Player + img

    def handle_events(self):
        for event in pygame.event.get():
            # Allow window to close
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_keys(event)  # Handle player movement

    def update(self, delta_time):
        self.player.move(delta_time)  # Update player movement
        
    def draw(self):
        self.screen.fill(BG_COLOR) # Fill BG
        self.player.draw(self.screen) # Draw player on screen
        pygame.display.flip() # Update display

    def run(self):
        while self.running:
            # Frame rate
            delta_time = self.clock.tick(60) / 1000 
            delta_time = max(0.001, min(0.1, delta_time))

            self.handle_events()  # Handle all events
            self.update(delta_time)  # Update game state (player movement)
            self.draw()  # Draw everything to the screen

        pygame.quit()

#if __name__ == '__main__':
    #game= Game ()
    #game.run()