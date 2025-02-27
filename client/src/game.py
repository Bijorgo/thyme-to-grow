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

        # Create player with image
        #self.character_img = pygame.image.load("assets/charactersprite.png").convert_alpha() # load img
        #self.character_img = pygame.transform.scale(self.character_img, 
            #(self.character_img.get_width() * 4, self.character_img.get_height() * 4) # Scale img
        #)
        #self.player = Player(0, 320, self.character_img) #init player w img, initial coordinates of Player

    def handle_events(self):
        for event in pygame.event.get():
            # Allow window to close
            if event.type == pygame.QUIT:
                self.running = False
            self.player.handle_keys(event)  # Handle player movement

    def update(self, delta_time):
        self.player.move(delta_time)  # Update player movement
        
    def draw(self):
        #self.screen.fill(BG_COLOR) # Fill BG
        #self.player.draw(self.screen) # Draw player on screen
        #pygame.display.flip() # Update display
        pass

    def run(self):
        while self.running:
            # Frame rate
            delta_time = self.clock.tick(60) / 1000 
            delta_time = max(0.001, min(0.1, delta_time))

            self.level.run(delta_time) # before updating display, run level

            self.handle_events()  # Handle all events including exit
            self.update(delta_time)  # Update game state (player movement)
            self.draw()  # Draw everything to the screen

        pygame.quit()

