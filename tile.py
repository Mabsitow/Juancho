import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load('assets/textures/levels/1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()