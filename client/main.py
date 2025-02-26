# client/main.py
# Import Modules
import os
import pygame

# entry point for game
# from documentation- line by line chimp :
#main_dir = os.path.split(os.path.abspath(__file__))[0] #returns absolute path of current script(main.py), split into tuple (directory path, file name), [0] accesses first element of tuple
    # in short: sets main_dir to where main.py is located
#data_dir = os.path.join(main_dir, "data") # creates path to sub directory "data"

pygame.init()

# Create window, dimensions f window as a tuple
# set_mode creates the "surface" - img for user to see
screen = pygame.display.set_mode((640,640))

# load imgs
    # 'file path', .convert => converts img to format that matches the display surface's pixel format, also faser rendering
    # an image is represented as a Surface, loaded from a file or created dynamically 
    # alt: convert_alpga() => preserve transparancy if img has alpha layer
character_img = pygame.image.load('charactersprite.png').convert_alpha()
# Change img size by scale
character_img = pygame.transform.scale( character_img,
                                       (character_img.get_width() * 2,
                                        character_img.get_height() *2
                                        ))

# Color key to ignore while blitting: useful when not using alpha layer
# change tuple to desired rgb key
# character_img.set_colorkey((0,0,0))

# alt pixelart rendering methods:
# image.load -> transform.scale -> screen.blit
    # scale first, smoothest, slowest
# set_mode(dims, pygame.SCALED)
    # scale last, optimized
# image.load -> intermediate.blit -> transform.scale -> screen.blit
    # scale last, more control, oder versison

# you can blit 

# Game loop
running = True
x = 0
clock = pygame.time.Clock()
# Assists in frame rate for smooth 
delta_time = 0.1

while running:

    # Fill background in green:(0, 255, 0)
    screen.fill((0, 255, 0))

    screen.blit(character_img, (x, 30))
    x += 50 * delta_time

    # This allows game window to close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Takes what we've put on the screen surface and displays on window
    pygame.display.flip() 

    # desired frame rate, 60 pixels/second is generally fasted for most but not all displays
    # returns time in ms
    # more precise: time.time
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()