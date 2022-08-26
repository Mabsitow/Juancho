import pygame, time
from sys import exit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init

pygame.display.set_caption('Juancho')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = pygame.image.load('assets/textures/player/1.png').convert_alpha()
        self.limit_x = SCREEN_WIDTH - self.texture.get_width()
        self.limit_y = SCREEN_HEIGHT - (self.texture.get_height() * 2)
        self.horizontal_steps = 2
        self.speed = 200
        self.gravity = 0
        self.jump_distance = self.texture.get_height() * 2
        self.image = self.texture
        self.rect = self.image.get_rect(topleft = (20 + self.texture.get_width(), self.limit_y))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def apply_gravity(self, dt):
        self.gravity += 1
        self.pos.y += (self.gravity * self.speed * dt)
        self.rect.y = round(self.pos.y)

        if self.gravity == 0:
            display_text(f'Current position: {self.pos.y}', 'White', 10, 40)

        if self.rect.y >= self.limit_y:
            self.pos.y = self.limit_y
            self.rect.y = self.limit_y

        display_text(f'Current gravity: {self.gravity}', 'White', 10, 20)
        display_text(f'Pos Y: {self.pos.y}', 'White', 10, 30)

    def player_input(self, dt):
        key = pygame.key.get_pressed()

        if key[pygame.K_UP] and self.rect.y >= self.limit_y:
            self.gravity = -10

        elif key[pygame.K_LEFT]:
            self.pos.x -= (self.horizontal_steps * self.speed * dt)
            self.rect.x = round(self.pos.x)
            display_text('Moving left', 'White', 10, 10)
            if self.pos.x <= 0:
                self.pos.x = 0

        elif key[pygame.K_RIGHT]:
            self.pos.x += (self.horizontal_steps * self.speed * dt)
            self.rect.x = round(self.pos.x)
            display_text('Moving right', 'White', 10, 10)
            if self.pos.x >= self.limit_x:
                self.pos.x = self.limit_x
                    
    def update(self, dt):
        self.player_input(dt)
        self.apply_gravity(dt)

font = pygame.font.init()

def display_text(text, color, pos_x, pos_y):
    score = pygame.font.Font(font, 16)
    score_texture = score.render(f'{text}', False, color)
    score_rectangle = score_texture.get_rect(topleft = (pos_x, pos_y))
    screen.blit(score_texture, score_rectangle)

player = pygame.sprite.GroupSingle()
player.add(Player())

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

    player.update(dt)
    player.draw(screen)

    pygame.display.update()
    clock.tick(60)
