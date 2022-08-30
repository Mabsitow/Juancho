import pygame, time
from sys import exit
from settings import *
from levels import Level

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Juancho')
        self.font = pygame.font.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_time = time.time()
        self.level = Level()

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

            self.level.run(dt)

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()