import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, transferable_sprites, obstacle_sprites):
        super().__init__(groups)
        self.surface_list = []
        self.image = pygame.image.load('assets/textures/player/right/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
        self.old_rect = self.rect.copy()
        self.jump_available = True
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 300
        self.gravity = 0
        self.transferable_sprites = transferable_sprites
        self.obstacle_sprites = obstacle_sprites
        self.attacking = False
        self.attack_cd = 100
        self.attack_time = 0
        self.idling = False
        self.idle_time = 0
        self.idle_limit = 60000
        self.status = 'static_right'
        self.last_pressed = ''
        self.collided = False
        self.frame_index = 0
        self.animation_speed = 0.15
        self.import_player_assets()

    def import_player_assets(self):
        character_path = 'assets/textures/player/'
        # Missing animations:
        # Push left / right
        # Attack left / right
        # Big attack left / right
        # Death left / right
        self.animations = {'static_left': [], 'static_right': [], 'left': [], 'right': [], 'jump_left': [], 'jump_right': [], 'idle_left': [], 'idle_right': [],
        'jump_hit_left': [], 'jump_hit_right': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        if self.last_pressed == 'right':
            if self.jump_available == False:
                if self.collided == True:
                    self.status = 'jump_hit_right'
                else:    
                    self.status = 'jump_right'
            else:
                if round(self.direction.x) > 0:
                    self.status = 'right'
                elif round(self.direction.x) == 0:
                    self.status = 'static_right'

        elif self.last_pressed == 'left':
            if self.jump_available == False:
                if self.collided == True:
                    self.status = 'jump_hit_left'
                else:
                    self.status = 'jump_left'
            else:
                if round(self.direction.x) < 0:
                    self.status = 'left'
                elif round(self.direction.x) == 0:
                    self.status = 'static_left'

        if self.idling == True:
            if self.status == 'static_right':
                self.status = 'idle_right'
            elif self.status == 'static_left':
                self.status = 'idle_left'

    def input(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_UP] and self.jump_available == True:
            self.jump_available = False
            self.gravity = -96
            self.idling = False
            self.idle_time = 0

        if key[pygame.K_RIGHT]:
            self.direction.x = 1
            self.idling = False
            self.idle_time = 0
            self.last_pressed = 'right'
        elif key[pygame.K_LEFT]:
            self.direction.x = -1
            self.idling = False
            self.idle_time = 0
            self.last_pressed = 'left'
        else:
            self.direction.x = 0

        if key[pygame.K_a] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.idling = False
            self.idle_time = 0

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        attack_elapsed_time = current_time - self.attack_time

        if 'static' in self.status:
            self.idle_time += 1

        if self.attacking:
            if attack_elapsed_time >= self.attack_cd:
                self.attacking = False

        if self.idle_time > self.idle_limit:
            self.idling = True

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
                        self.collided = False

                    # Collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.pos.y = self.rect.y
                        self.collided = True

        if transferable_sprites:
            if direction == 'vertical':
                for sprite in transferable_sprites:
                    # Collision on the bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.pos.y = self.rect.y
                        self.gravity = 0
                        self.jump_available = True
                        self.collided = False

                    # Collision on the top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        if self.direction.y > sprite.rect.top:
                            self.rect.bottom = sprite.rect.top
                            self.pos.y = self.rect.y
                            self.collided = False
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

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(topleft = self.rect.topleft)

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed, dt)