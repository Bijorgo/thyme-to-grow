import pygame
from config import *
from src.sprites import Menu
from src.fetching import get_players
from src.buttons import Button
from src.level import Level
import requests

class MenuPage:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.buttons = []
        self.garden_buttons = []
        self.selected_player = None
        self.running = True  # Control loop
        self.ui_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 60) # Default font, size 60
        self.setup()

    def setup(self):
        # Window size
        SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

        # Background image load and resize
        menu_bg = pygame.image.load('src/assets/menubg.png').convert_alpha()
        menu_bg_resized = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        menu_bg_rect = menu_bg_resized.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # Rect for centering THIS MAY BE REDUNANT => REVISIT
        Menu(menu_bg_rect.topleft, menu_bg_resized, self.ui_sprites, LAYERS['ground'])

        player_data = get_players() # Fetch request 

        # Dynamic positioning 
         # Button centering
        button_width, button_height = 300, 60
        button_y_start = SCREEN_HEIGHT // 3 # Start below title
        button_spacing = 80

        # Create player buttons 
        for i, player in enumerate(player_data["players"]):
            # enumerate tracks index (i), i is used to position buttons so they dont overlap
            self.buttons.append(Button(
                pos=(SCREEN_WIDTH//2 - button_width//2, button_y_start + i * button_spacing), # Centered
                width=button_width,
                height=button_height, 
                text=f"{player['name']}",
                action=lambda player=player: self.show_gardens(player) 
                # lambda captures player and 
                    # delays execution of self.show_gardens(player) until after button is clicked 
                # player = player ensures button "remembers" the player it was created with
                    # rather than the last player of the loop
            ))

    def show_gardens(self, player):
        self.selected_player = player
        button_width, button_height = 400, 60
        button_y_start = SCREEN_HEIGHT // 2  # Gardens appear below player buttons

        self.garden_buttons = [
            Button(
                   pos=(SCREEN_WIDTH//2 - button_width//2, button_y_start + i * 70), # Centered
                   width=button_width,
                   height=button_height,
                   text=f"{self.selected_player['name']}: {garden['name']}",
                   action=lambda garden=garden: self.run_game(garden)
            )
            for i, garden in enumerate(player["gardens"])
        ]

    def run_game(self, garden):
        garden_id = garden.get("id")  # Ensure garden has an ID
        print(f"DEBUG: Running game for garden ID {garden_id}")  # Debugging

        try:
            # Fetch garden from API
            response = requests.get(f"http://127.0.0.1:5000/gardens/{garden_id}")
            print(f"DEBUG: Response status = {response.status_code}, text = {response.text}")  # Debugging

            if response.status_code == 200:
                selected_garden = response.json()
                print(f"DEBUG: Fetched Garden: {selected_garden}")  # Debugging

                pygame.event.clear() # Clear lingering events
                self.running=False # Stop menu loop

                # Create new level with clean state
                level = Level(self.selected_player, selected_garden)  # Pass garden to level
                level.run()  # Switch to level loop

                self.running = True  # Restart menu for when level loop ends

            else:
                print(f"ERROR: Failed to fetch garden ID {garden_id}. Status {response.status_code}, Response: {response.text}")
        except requests.exceptions.JSONDecodeError:
            print(f"ERROR: JSON decoding failed for response from /gardens/{garden_id}. Raw text: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed for /gardens/{garden_id}. Exception: {e}")

    # Game loop
    def run(self):
        while self.running:
            # Create background 
            self.display_surface.fill('black')
            self.ui_sprites.update(0)  
            self.ui_sprites.draw(self.display_surface)

            # "Main Menu" text
            title_surface = self.font.render("Main Menu", True, (0,0,0))
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.display_surface.blit(title_surface, title_rect)

            # Create buttons
            for button in self.buttons + self.garden_buttons:
                button.draw(self.display_surface)

            # Events listeners 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                # Mouse clicks    
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons + self.garden_buttons:
                        if button.is_clicked(pygame.mouse.get_pos()):
                            button.click()

            pygame.display.update()
