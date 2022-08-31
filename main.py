import pygame, time
from sys import exit
from settings import *
from levels import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Juancho')
        pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.level = Level(0)

    # Probably move this out to settings.py
    def display_text(self, text, pos_x, pos_y, color):
        # System font will be changed later for a custom font
        # pygame.font.Font(FONT_FAMILY, FONT_SIZE)
        font = pygame.font.SysFont('Trebuchet MS', 13, True)
        text_image = font.render(f'FPS: {text}', False, color)
        text_rect = text_image.get_rect(topleft = (pos_x, pos_y))
        self.screen.blit(text_image, text_rect)

    # Not gonna use this (for now)
    # def change_level(self, index):
    #     self.level = Level(index)

    def run(self):
        previous_time = time.time()
        
        while True:
            dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill('black')

            self.display_text(str(int(self.clock.get_fps())), 10, 10, 'White')

            self.level.run(dt)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()