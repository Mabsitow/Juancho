import pygame
from os import walk

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
FPS = 60
TILE_SIZE = 64
FONT_FAMILY = 'assets/font/Silkscreen-Regular.ttf'
FONT_SIZE = 32

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

world_data = [
[
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,2,2,2,2,0,0,0],
    [0,'P',0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1]
],
[
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,2,2,2,2,2,2,0,0],
    [0,'P',0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1]
]
]