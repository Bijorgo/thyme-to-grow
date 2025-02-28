import pygame
from config import *
from src.player import Player
from src.sprites import Menu
from src.fetching import *
from src.buttons import Button
from src.level import Level

class MenuPage:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.buttons = []
        self.garden_buttons = []  # Will hold buttons for gardens that appear after player selection
        self.selected_player = None  # Track selected player for garden buttons
        self.in_game = False
        self.ui_sprites = pygame.sprite.Group()  # Group for UI elements
        self.setup()

    def setup(self):
        menu_bg = Menu(
            pos = (0,0),
            surface = pygame.image.load('src/assets/menubg.png').convert_alpha(),
            groups = self.ui_sprites,
            z = LAYERS['ground']
            )
        
        # Fetch player data
        player_data = get_players()

        # Create buttons for each player
        for i, player in enumerate(player_data["players"]):
            button = Button(
                pos=(100, 100 + i * 60),  # Adjust position for player buttons
                width=200, height=50,
                text=f"Player {player['name']}",
                action=lambda player=player: self.show_gardens(player)  # Show gardens for selected player
            )
            self.buttons.append(button)

    def show_gardens(self, player):
        self.selected_player = player
        self.garden_buttons = []  # Reset garden buttons

        # Create garden buttons for the selected player
        for garden in player["gardens"]:
            garden_button = Button(
                pos=(500, 200 + len(self.garden_buttons) * 60),
                width=200, height=50,
                text=f"Garden {garden['name']}",
                action=lambda garden=garden: self.launch_game(garden)  # Launch game after clicked 
            )
            self.garden_buttons.append(garden_button)

    def show_garden_details(self, garden):
        # Print the garden details, mostly for debugging
        print(f"Showing details for Garden: {garden['name']}")

    def launch_game(self, garden):
        # This method will be called when a garden button is clicked
        print(f"Launching game for Garden: {garden['name']}")  # debug
        self.in_game = True  # Set flag to indicate game is ready to start
        self.level = Level(selected_player=self.selected_player)  # Pass selected player

    def run(self, delta_time):
        self.display_surface.fill('black')  # Background

        # Update and draw all UI elements (including menu background)
        self.ui_sprites.update(delta_time)  # Update UI sprites
        self.ui_sprites.draw(self.display_surface)  # Draw UI elements

        # Draw the main menu buttons
        for button in self.buttons:
            button.draw(self.display_surface)

        # If a player has been selected, show garden buttons
        if self.selected_player:
            for button in self.garden_buttons:
                button.draw(self.display_surface)

        # Check for button clicks
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.is_clicked(mouse_pos):
                            button.click()

                    for button in self.garden_buttons:
                        if button.is_clicked(mouse_pos):
                            button.click()

            if event.type == pygame.QUIT:
                pygame.quit()  # Ensure quit event is handled here too
                exit()

