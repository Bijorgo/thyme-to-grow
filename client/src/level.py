import pygame
from config import *
from src.player import Player
from src.sprites import Generic
from src.fetching import get_players

class Level:
    def __init__(self, selected_player=None, selected_garden=None):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.selected_player = selected_player
        self.selected_garden = selected_garden
        self.players = []
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

            if self.players:
                player = self.players[0]
                self.all_sprites.custom_draw(player)
                self.all_sprites.update(delta_time)

            pygame.display.update()

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
