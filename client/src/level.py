import pygame
from config import *
from src.player import Player
from src.sprites import Generic
from src.fetching import *

class Level:
    def __init__(self, selected_player=None):
        # Get display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        # Setup player
        self.selected_player = selected_player  # Store selected player
        self.players= [] # init player list
        self.setup() # init players + elements

    def setup(self):
        if self.selected_player:
            print(f"Player {self.selected_player['name']}, creating level")

            # Load background
            background = pygame.image.load('src/assets/bg2.png').convert_alpha()
            self.background = Generic(pos=(0, 0), surface=background, groups=self.all_sprites, z = LAYERS['ground'])

            # Fetch players from API
            player_data = get_players()

            print("Debug Fetched player data comeplte")

            # Create player instance and add to the all_sprites group
            #self.player = Player((640, 360), self.all_sprites)  # Pass position, group
            #self.players = []
            for i, player_info in enumerate(player_data["players"]):
                player_name = player_info["name"]
                player = Player(
                    pos=(640, 360 + i +50), # avoids overlap
                    group=[self.all_sprites, self.collision_sprites], # assigns sprite groups
                    name=player_name # sets player name
                )
                self.players.append(player) # add player to list
            print(f"Players created: {len(self.players)}") # debug 


    def run(self, delta_time):
        self.display_surface.fill('black') # background
        #self.all_sprites.draw(self.display_surface) # Draw sprites on screen
        if self.players:
            player = self.players[0]
            if player:
                self.all_sprites.custom_draw(player) # custom_draw from level
                self.all_sprites.update(delta_time)  # Update all sprites
                for player in self.players:
                    player.draw(self.display_surface)
            else:
                print("No valid player found, skipping drawing.")
        else:
            print("Players are not ready yet, waiting...")


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        #Camera
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2 
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        # Layring sprites
        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
        