import pygame
from src.game import Game  # Import the Game class
from src.objects import MainMenuButton

pygame.init()

# Create game instance, inits display ( must be before loading imgs )
game = Game()

# Load button image
main_menu_button_img = pygame.image.load('assets/menu-button.png').convert_alpha()
main_menu_button_img = pygame.transform.scale(
    main_menu_button_img,
    (main_menu_button_img.get_width() * 4, main_menu_button_img.get_height() * 4)
)

# Create button object
main_menu_button = MainMenuButton(0, 0, main_menu_button_img)

# Start the game loop
game.run()

pygame.quit()
