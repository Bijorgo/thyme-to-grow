import pygame, random
from config import *
from src.player import Player
from src.sprites import Generic, Plants
from src.fetching import get_players, get_plants
from src.buttons import Button, MainMenuButton
import requests

class Level:
    def __init__(self, selected_player=None, selected_garden=None):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup() # Create a group of all sprites
        self.collision_sprites = pygame.sprite.Group() # Create a group of collidable sprites
        self.selected_player = selected_player
        self.selected_garden = selected_garden
        self.dragging_plant = None
        self.plant_initial_pos = None
        self.players = []
        self.plants = pygame.sprite.Group() # Create group of plant sprites
        self.running = True
        self.buttons = []
        self.setup()
        print(f"Level initialized with player {selected_player} and garden {selected_garden}") # debug

    def setup(self):
        # Check for given player / garden combo
        if self.selected_garden and self.selected_garden:
            print(f"Player {self.selected_player['name']}, garden {self.selected_garden['name']}, garden id {self.selected_garden['id']} creating level") # debug

            # Set background => this will need to change for unique backgrounds per level            
            background_img = pygame.image.load('src/assets/bg2.png').convert_alpha() # All garden backgrounds are currently generic (found in sprites.py)
            resized_bg = pygame.transform.scale(background_img, (2000, 2000)) # resized
            self.background = Generic((0, 0), resized_bg,
                                      self.all_sprites, LAYERS['ground'])
            
            # Create player sprite
            player_data = get_players() # Make the get request, function from fetching.py
            
            for i, player_info in enumerate(player_data["players"]):

                # Assign character image
                if self.selected_player['name'] == "Fern":
                    char_img = pygame.image.load('src/assets/fern.png')
                elif self.selected_player['name'] == "Fernando":
                    char_img = pygame.image.load('src/assets/fernando.png')
                else:
                    char_img = pygame.image.load('src/assets/default_char.png')
                # Resize char_img
                new_width = char_img.get_width() * 3
                new_height = char_img.get_height() * 3
                char_img_resize = pygame.transform.smoothscale(char_img, (new_width, new_height))

                # Init Player instance 
                if self.selected_player['id'] == player_info['id']:
                    self.players.append(Player(
                        pos=(640, 360 + i * 50),
                        group=[self.all_sprites, self.collision_sprites],
                        image=char_img_resize,
                        name=player_info["name"]
                ))
                    
            # Load planted plants from database         
            self.load_plants()

            # Load menu button 
            self.menu_button = Button(
                    pos=(0, 0), 
                    width=140, 
                    height=50,
                    text=f"Main Menu",
                    action=self.return_to_menu
            )
            self.buttons.append(self.menu_button)

    # Retrieve the already planted plants 
    def load_plants(self):
        # DEBUG THIS FUNCTION
        # Need to retrieve plants by garden id? not all cultivated plants
        #for sprite in self.plants:
         #   self.all_sprites.remove(sprite)  # Remove plant from all_sprites
        #self.plants.empty()  # Clears plant group only
            
        response = requests.get("http://127.0.0.1:5000/cultivated-plants") #GET

        if response.status_code == 200:
            all_currently_planted = response.json().get("cultivated-plants", []) # Debug => use .get returns default(empty list) instead of error
            print(f"DEBUG: Loaded plants: {all_currently_planted}")

            for one_plant in all_currently_planted:
                plant_info = one_plant["plant"] # Plant object 
                x, y = one_plant["x"], one_plant["y"]  # Load x,y position
                garden_obj = one_plant["garden"] # Garden object

                # If current garden id matches the planted plant's garden id, create sprites
                print(f"self.selected_garden['id]: {self.selected_garden['id']}") # debug
                print(f" garden_obj: {garden_obj}")

                if garden_obj['id'] == self.selected_garden['id']:
                    resized_plant = None 
                    print(f"~~~~~~~~~~~~plant[]: {plant_info['name']}, plant.name plant_info.name, plant info: {plant_info} ")
                    if plant_info["name"] == "Tulip":
                        plant_surface = pygame.image.load('src/assets/tulip.png').convert_alpha()                     
                    elif plant_info["name"] == "Thyme":                   
                        plant_surface = pygame.image.load('src/assets/thyme.png').convert_alpha()                        
                    elif plant_info["name"] == "Carrot":       
                        plant_surface = pygame.image.load('src/assets/carrot.png').convert_alpha()
                    else:
                        print(f"Warning: No image found for plant {plant_info['name']}, using default.")
                        plant_surface = pygame.image.load('src/assets/flower.png').convert_alpha()  # Provide a fallback image

                    # Resize the plant image only if it's set
                    if plant_surface:
                        new_width = plant_surface.get_width() * 2  
                        new_height = plant_surface.get_height() * 2
                        resized_plant = pygame.transform.smoothscale(plant_surface, (new_width, new_height))
                                                 
                    # init plant sprite
                    new_plant = Plants(
                        pos=(x, y),
                        surface=resized_plant,
                        groups=[self.all_sprites, self.plants],  # Add to sprite groups
                        z=LAYERS['main'],
                        cultivate_plants=one_plant
                    )
                    print(f"DEBUG: Planted {plant_info['name']} at ({x}, {y})")
        else:
            print("DEBUG: Error fetching planted flowers:", response.text)
            

    def plant_seed(self):
        print(f"DEBUG: attempting to plant seed in garden {self.selected_garden['id']}") # Debug

        # Fetch plants from API
        plants = get_plants() # Fetch function in fetching.py

        if not plants:
            print("DEBUG: No available plants (written from level)")
            return
        
        # Select a random plant
        plant = random.choice(plants)  # Choose a random plant
        plant_id = plant["id"]  # Store id

        # Determine position: used for persisting plants
        player = self.players[0]
        plant_pos = (player.rect.centerx - 32, player.rect.centery - 32) # Adjust for center of plant img, Debug these nubers?

        # POST request data
        data ={
            "player_id": self.selected_player['id'],
            "garden_id": self.selected_garden['id'],
            "plant_id": plant_id,
            "x" : plant_pos[0],
            "y" : plant_pos[1],
        }
        # Endpoint for POST request
        url = "http://127.0.0.1:5000/cultivated-plants" # POST
        # Send the POST request to the API
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            print(f"DEBUG: Seed planted successfully! (Plant id {plant_id})")

            # Print response JSON for debugging
            try:
                cultivate_plant = response.json()  # Get the JSON response
                print(f"DEBUG: API Response: {cultivate_plant}")  # Debugging step
            except Exception as exc:
                print(f"DEBUG: Failed to parse JSON response - {exc}")
                return
            
            # Ensure cultivate_plant is correctly structured and accessible
            if not isinstance(cultivate_plant, dict) or 'id' not in cultivate_plant:
                print("DEBUG: Cultivate plant object missing or invalid.")
                return
            
            # Assign image
            if plant['name'] == "Tulip": 
                plant_surface = pygame.image.load('src/assets/tulip.png').convert_alpha()                     
            elif plant['name'] == "Thyme":                  
                plant_surface = pygame.image.load('src/assets/thyme.png').convert_alpha()                        
            elif plant['name'] == "Carrot": 
                plant_surface = pygame.image.load('src/assets/carrot.png').convert_alpha()
            else:
                print(f"Warning: No image found for plant {plant['name']}, using default.")
                plant_surface = pygame.image.load('src/assets/flower.png').convert_alpha()  # Provide a fallback image

            # Resize the plant image only if it's set
            if plant_surface:
                new_width = plant_surface.get_width() * 2  
                new_height = plant_surface.get_height() * 2
                resized_plant = pygame.transform.smoothscale(plant_surface, (new_width, new_height))

            # init plant sprite
            new_plant = Plants(
                pos = plant_pos, 
                surface = resized_plant, 
                groups = [self.all_sprites, self.plants], # Add to both all_sprites and plants group
                z = LAYERS['main'], # Add to main layer
                cultivate_plants = cultivate_plant
            )  
            print(f"DEBUG: New plant created at {plant_pos}") # debug
        else:
            print(f"DEBUG: Error planting seed: {response.text}")

    def harvest_seeds(self, plant):
        # Access cultivate plants object from sprite
        cultivate_plant = plant.cultivate_plants_obj

        if cultivate_plant:
            # Access related Plant and Garden
            plant_obj = cultivate_plant['plant']
            garden_obj = cultivate_plant['garden']
            cultivated_plant_id = cultivate_plant['id']
            print(f"DEBUG: Harvesting plant ID = {cultivated_plant_id}")  # debug


            # DELETE fetch request
            response = requests.delete(f"http://127.0.0.1:5000/cultivated-plants/{cultivated_plant_id}") # DELETE

            if response.status_code == 200:
                print(f"DEBUG: Plant harvested and removed from the database")
                # Remove the plant sprite from the sprite groups
                self.plants.remove(plant)  # Remove from the plants sprite group
                self.all_sprites.remove(plant)  # Remove from all_sprites group
                del plant # Delete image
                print(f"DEBUG: Plant removed from the UI")
            else:
                print(f"DEBUG: Error harvesting plant ") #{response.text}

    # Exit this loop, return to menu
    def return_to_menu(self):
        print("Return to main menu")
        self.running=False
                
    # Game loop                
    def run(self):
            while self.running:
                self.display_surface.fill('black') # Black background
                delta_time = max(0.001, min(0.1, pygame.time.Clock().tick(60) / 1000)) # Frame rate ?

                # Draw all sprites
                if self.players:
                    player = self.players[0]
                    self.all_sprites.custom_draw(player)
                    self.all_sprites.update(delta_time)

                # Draw all buttons
                for button in self.buttons:
                    button.draw(self.display_surface)

                # Handle plant dragging if 'm' key is held
                if self.dragging_plant:
                    self.handle_plant_dragging(player)

                # Look for events
                for event in pygame.event.get():
                    # Quit event
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    # Key down event 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:  # 'm' key is pressed
                            for plant in self.plants:
                                if player.rect.colliderect(plant.rect):  # If player collides with plant
                                    self.dragging_plant = plant  # Start dragging this plant
                                    self.plant_initial_pos = plant.rect.center  # Save initial position
                                    break
                        # Key h = harvest/delete plant
                        if event.key == pygame.K_h:
                            player = self.players[0]
                            for plant in self.plants: # check for all sprites
                                if player.rect.colliderect(plant.rect): # Check if player is near plant
                                    self.harvest_seeds(plant) # Call harvest function
                                    break
                        # Key p = plant/create plant
                        if event.key == pygame.K_p:
                            self.plant_seed()
                    # Key up event 
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_m:  # 'm' key is released
                            self.place_dragged_plant()  # Place the plant and update the database
                        
                    # Click events       
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        for button in self.buttons:
                            if button.is_clicked(pygame.mouse.get_pos()):
                                button.click()  # Call button's action

                pygame.display.update()

    # Add this function to handle dragging of plants
    def handle_plant_dragging(self, player):
        if self.dragging_plant:
            # Update the plant's position to follow the player
            self.dragging_plant.rect.center = player.rect.center
            self.dragging_plant.update()  # Make sure to update the plant's sprite

    def place_dragged_plant(self):
        if self.dragging_plant:
            # Update the plant's position in the database
            plant_data = {
                "x": self.dragging_plant.rect.centerx,
                "y": self.dragging_plant.rect.centery
            }

            response = requests.patch(f"http://127.0.0.1:5000/cultivated-plants/{self.dragging_plant.cultivate_plants_obj['id']}", json=plant_data)
            
            if response.status_code == 200:
                print(f"DEBUG: Plant placed at new position ({self.dragging_plant.rect.centerx}, {self.dragging_plant.rect.centery})")
            else:
                print(f"DEBUG: Error placing plant: {response.text}")

            self.dragging_plant = None  # Reset dragging state




# Consider moving this somewhere else?
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

    