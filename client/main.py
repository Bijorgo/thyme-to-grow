# client/main.py
# Import Modules
import os
import pygame
import requests
from src.player import Player

pygame.init()

# Game settings
# Create window, dimensions f window as a tuple
screen = pygame.display.set_mode((1920,1080))
    # top left = (0,0)
    # middle = (960, 540) => x/2, y/2
clock = pygame.time.Clock()
# Assists in frame rate for smooth 
delta_time = 0.1

# load imgs
character_img = pygame.image.load('assets/charactersprite.png').convert_alpha()

main_menu_button = pygame.image.load('assets/menu-button.png').convert_alpha()

# Change img size by scale
character_img = pygame.transform.scale( character_img,
                                       (character_img.get_width() * 8,
                                        character_img.get_height() * 8
                                        ))
main_menu_button = pygame.transform.scale( main_menu_button,
                                          (main_menu_button.get_width() * 4,
                                           main_menu_button.get_height() * 4))

# Create player object
player = Player(x=100, y=100, character_img=character_img)

# Game loop
running = True


# Starting coodinates
x = 0
y = 320



while running:

    # Fill background in green:(0, 255, 0)
    screen.fill((0, 255, 0))

    # desired frame rate
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

    screen.blit(main_menu_button, (0, 0))

    # Events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_keys(event)  # Handle key events for movement

    # Character movement and drawing 
    player.move(delta_time) # Move character 
    player.draw(screen)  # Draw the player character

    # Takes what we've put on the screen surface and displays on window
    pygame.display.flip() 

    

pygame.quit()