from tkinter import CENTER
import pygame, time
from sys import exit
from levels import world_data

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640

current_level = 0

pygame.init

pygame.display.set_caption('Juancho')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class World():
    def __init__(self, world):
        super().__init__()
        self.levels = []
        self.image = pygame.image.load('assets/textures/levels/1.png')
        self.tile_size = 64

        level_count = 0
        for level in world:
            tile_list = []
            row_count = 0
            for row in level:
                col_count = 0
                for tile in row:
                    if tile == 1:
                        img = pygame.transform.scale(self.image, (self.tile_size, self.tile_size))
                        img_rect = img.get_rect(topleft = (col_count * self.tile_size, row_count * self.tile_size))
                        tile = (img, img_rect)
                        tile_list.append(tile)
                    else:
                        tile_list.append(0)
                    col_count += 1
                row_count += 1
            self.levels.append(tile_list)
            level_count += 1

    def draw(self, level_index):
        for tile in self.levels[level_index]:
            if tile != 0:
                screen.blit(tile[0], tile[1])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/textures/player/1.png').convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.limit_x = SCREEN_WIDTH - self.image.get_width()
        self.limit_y = SCREEN_HEIGHT - (self.image.get_height() * 2)
        self.speed = 200
        self.gravity = 1
        self.vel_y = 0
        self.jump = False
        self.rect = self.image.get_rect(topleft = (self.width, self.limit_y))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def input(self, dt):
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0
        current_tile = 0

        if key[pygame.K_UP] and self.jump == False:
            self.jump = True
            self.vel_y = -10

        if key[pygame.K_RIGHT]:
            dx = 2
        elif key[pygame.K_LEFT]:
            dx = -2

        # Gravity
        self.vel_y += self.gravity
        dy += self.vel_y

        # Borders from the screen
        if self.rect.right + dx >= SCREEN_WIDTH:
            dx = +self.rect.right
        if self.rect.left + dx <= 0:
            dx = -self.rect.left

        # Collisions
        for tile in world.levels[current_level]:
            if tile != 0:
                # collision in vertical axis
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # if player head is higher than block bottom
                    if self.rect.top < tile[1].bottom:
                        tmp_tile = current_tile - 9
                        if world.levels[current_level][tmp_tile] != 0:
                            # block player from jumping
                            self.rect.top = tile[1].bottom
                        else:
                            # put player feets into block top
                            self.rect.bottom = tile[1].top
                            dy = 0
                            self.vel_y = 0
                            self.jump = False

                    # collision in horizontal axis
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        if self.rect.right > tile[1].left:
                            print('Left tile')
                            dx = 0
                            self.rect.right = tile[1].left - 1
                        elif self.rect.left < tile[1].right:
                            print('Right tile')
                            dx = 0
                            self.rect.left = tile[1].right + 1

            current_tile += 1

        # if self.rect.top + dy > self.limit_y:
        #     dy = 0

        self.rect.x += round(dx * self.speed * dt)
        self.rect.y += round(dy * self.speed * dt)

    def update(self, dt):
        self.input(dt)

font = pygame.font.init()

def display_text(text, color, pos_x, pos_y):
    score = pygame.font.Font(font, 16)
    score_texture = score.render(f'{text}', False, color)
    score_rectangle = score_texture.get_rect(topleft = (pos_x, pos_y))
    screen.blit(score_texture, score_rectangle)

player = pygame.sprite.Group()
player.add(Player())
world = World(world_data)

previous_time = time.time()

run = True
while run:
    dt = time.time() - previous_time
    previous_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill('Black')

    world.draw(current_level)

    player.update(dt)
    player.draw(screen)

    pygame.display.update()
    clock.tick(60)
