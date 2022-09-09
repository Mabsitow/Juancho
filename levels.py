import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self, index):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.transferable_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map(index)

    def create_map(self, index):
        for row_index, row in enumerate(world_data[index]):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                # Non-transferable tiles
                if col == 1:
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                # Transferable tiles
                if col == 2:
                    Tile((x, y), [self.visible_sprites, self.transferable_sprites])
                # Player starting point in the map
                if col == 'P':
                    self.player = Player((x, y), [self.visible_sprites], self.transferable_sprites, self.obstacle_sprites)

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
    