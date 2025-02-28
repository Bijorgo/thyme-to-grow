import pygame, random
from config import *
from src.player import Player
from src.sprites import Generic, Plants
from src.fetching import get_players, get_plants
import requests

class Level:
    def __init__(self, selected_player=None, selected_garden=None):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup() # Create a group of all sprites
        self.collision_sprites = pygame.sprite.Group() # Create a group of collidable sprites
        self.selected_player = selected_player
        self.selected_garden = selected_garden
        self.players = []
        self.plants = pygame.sprite.Group() # Create group of plant sprites
        self.running = True
        self.setup()
        print(f"Level initialized with player {selected_player} and garden {selected_garden}") # debug

    def setup(self):
        if self.selected_player:
            print(f"Player {self.selected_player['name']}, creating level")
            self.background = Generic((0, 0), pygame.image.load('src/assets/bg2.png').convert_alpha(),
                                      self.all_sprites, LAYERS['ground'])

            player_data = get_players() # Make the get request, function from fetching.py
            for i, player_info in enumerate(player_data["players"]):
                self.players.append(Player(
                    pos=(640, 360 + i * 50),
                    group=[self.all_sprites, self.collision_sprites],
                    name=player_info["name"]
                ))
            self.load_plants()

    # Retrieve the already planted plants 
    def load_plants(self):
        response = requests.get("http://127.0.0.1:5000/cultivated-plants")

        if response.status_code == 200:
            cultivated_plants = response.json().get("cultivated-plants", []) # Debug => use .get returns default(empty list) instead of error
            print(f"DEBUG: Loaded plants: {cultivated_plants}")

            for plant_data in cultivated_plants:
                plant_info = plant_data["plant"]
                x, y = plant_data["x"], plant_data["y"]  # Load position

                # Create plant sprite
                plant_surface = pygame.image.load('src/assets/flower.png').convert_alpha()
                new_plant = Plants(
                    pos=(x, y),
                    surface=plant_surface,
                    groups=[self.all_sprites, self.plants],  # Add to sprite groups
                    z=LAYERS['main'],
                    cultivate_plants=plant_data
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
        url = "http://127.0.0.1:5000/cultivated-plants"

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

            # position plant based on player position
            #player = self.players[0] 
            #plant_pos = (player.rect.centerx - 32, player.rect.centery - 32) # this should be the same as plant_pos line

            # Create new plant sprite, add tp plant sprite group
            plant_surface = pygame.image.load('src/assets/flower.png').convert_alpha()  # Load plant image
            # init plant sprite
            new_plant = Plants(
                pos = plant_pos, 
                surface = plant_surface, 
                groups = [self.all_sprites, self.plants], # Add to both all_sprites and plants group
                z = LAYERS['main'], # Add to main layer
                cultivate_plants = cultivate_plant
            )  
            print(f"DEBUG: New plant created at {plant_pos}") # debug
        else:
            print(f"DEBUG: Error planting seed: {response.text}")

    def harvest_seeds(self, plant):
        # Handle no plants
        #if not self.plants:
        #    print("DEBUG: No plants to harvest")
        #    return
        
        # Access cultivate plants object from sprite
        cultivate_plant = plant.cultivate_plants_obj

        if cultivate_plant:
            # Access related Plant and Garden
            plant_obj = cultivate_plant['plant']
            garden_obj = cultivate_plant['garden']
            cultivated_plant_id = cultivate_plant['id']
            #print(f"DEBUG: Harvesting plant {plant_obj['name']} (ID: {plant_obj['id']}) from garden {garden_obj['name']} (ID: {garden_obj['id']}) CP ID: {id}")

            # DELETE fetch request
            response = requests.delete(f"http://127.0.0.1:5000/cultivated-plants/{cultivated_plant_id}")

            if response.status_code == 200:
                print(f"DEBUG: Plant harvested and removed from the database")
                # Remove the plant sprite from the sprite groups
                self.plants.remove(plant)  # Remove from the plants sprite group
                self.all_sprites.remove(plant)  # Remove from all_sprites group
                del plant # Delete image
                print(f"DEBUG: Plant removed from the UI")
            else:
                print(f"DEBUG: Error harvesting plant ") #{response.text}
                
    # Game loop                
    def run(self):
            while self.running:
                self.display_surface.fill('black')
                delta_time = max(0.001, min(0.1, pygame.time.Clock().tick(60) / 1000))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_h:
                            player = self.players[0]
                            for plant in self.plants: # check for all sprites
                                if player.rect.colliderect(plant.rect): # Check if player is near plant
                                    self.harvest_seeds(plant) # Call harvest function
                                    break
                    

                    # Trigger planting by pressing p
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                        self.plant_seed()

                # Draw all sprites
                if self.players:
                    player = self.players[0]
                    self.all_sprites.custom_draw(player)
                    self.all_sprites.update(delta_time)

                # Draw the plants
                #self.plants.update(delta_time)  # Update all plant sprites
                #self.plants.draw(self.display_surface)  # Draw all plant sprites

                pygame.display.update()




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

    