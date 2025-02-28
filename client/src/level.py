import pygame
from config import *
from src.player import Player
from src.sprites import Generic, Plants
from src.fetching import get_players
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

            player_data = get_players()
            for i, player_info in enumerate(player_data["players"]):
                self.players.append(Player(
                    pos=(640, 360 + i * 50),
                    group=[self.all_sprites, self.collision_sprites],
                    name=player_info["name"]
                ))

    def run(self):
        while self.running:
            self.display_surface.fill('black')
            delta_time = max(0.001, min(0.1, pygame.time.Clock().tick(60) / 1000))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

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

    def plant_seed(self):
        print(f"DEBUG: attempting to plant seed in garden {self.selected_garden['id']}") # Debug

        # Endpoint for POST request
        url = "http://127.0.0.1:5000/cultivated-plants"

        # POST request data
        data ={
            "player_id": self.selected_player['id'],
            "garden_id": self.selected_garden['id'],
            "plant_id": 1 #plant_id # Adjust to be dynamic later
        }

        # Send the POST request to the API
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            print("DEBUG: Seed planted successfully!")

            # position plant based on player position
            player = self.players[0] 
            plant_pos = (player.rect.centerx - 32, player.rect.centery - 32) # adjust for center of plant img

            # Create new plant sprite, add tp plant sprite group
            plant_surface = pygame.image.load('src/assets/flower.png').convert_alpha()  # Load plant image
            new_plant = Plants(
                pos = plant_pos, 
                surface = plant_surface, 
                groups = [self.all_sprites, self.plants], # Add to both all_sprites and plants group
                z = LAYERS['main'] # Add to ain layer
            )  
            print(f"DEBUG: New plant created at {plant_pos}") # debug
        else:
            print(f"DEBUG: Error planting seed: {response.text}")

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
