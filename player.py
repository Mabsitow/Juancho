import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, transferable_sprites, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/textures/player/1.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()
        self.jump_available = True
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 600
        self.gravity = 0
        self.transferable_sprites = transferable_sprites
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_UP] and self.jump_available == True:
            self.jump_available = False
            self.gravity = -96

        if key[pygame.K_RIGHT]:
            self.direction.x = 1
        elif key[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed, dt):
        if self.direction.magnitude_squared() != 0:
            self.direction = self.direction.normalize()

        self.gravity += speed * dt
        self.direction.y += self.gravity * dt
        
        self.pos.x += self.direction.x * speed * dt
        self.rect.x = round(self.pos.x)
        self.collision('horizontal')

        self.pos.y += self.direction.y * speed * dt
        self.rect.y = round(self.pos.y)
        self.collision('vertical')

    def collision(self, direction):
        obstacle_sprites = pygame.sprite.spritecollide(self, self.obstacle_sprites, False)
        transferable_sprites = pygame.sprite.spritecollide(self, self.transferable_sprites, False)

        if obstacle_sprites:
            if direction == 'horizontal':
                for sprite in obstacle_sprites:
                    # Collision on the right
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.pos.x = self.rect.x

                    # Collision on the left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.pos.x = self.rect.x

            if direction == 'vertical':
                for sprite in obstacle_sprites:
                    # Collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.gravity = 0
                        self.jump_available = True

                    # Collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y

        if transferable_sprites:
            # Left this here if I need it in the near future, for now I don't
            # if direction == 'horizontal':
            #     for sprite in transferable_sprites:
            #         # Collision on the right
            #         if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
            #             if self.direction.y >= sprite.rect.top:
            #                 self.rect.right = sprite.rect.left
            #                 self.pos.x = self.rect.x

            #         # Collision on the left
            #         if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
            #             if self.direction.y >= sprite.rect.top:
            #                 self.rect.left = sprite.rect.right
            #                 self.pos.x = self.rect.x

            if direction == 'vertical':
                for sprite in transferable_sprites:
                    # Collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.gravity = 0
                        self.jump_available = True

                    # Collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        if self.direction.y > sprite.rect.top:
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(self.speed, dt)