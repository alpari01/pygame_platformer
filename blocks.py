import pygame

import player
from settings import *


class Block(pygame.sprite.Sprite):
    """
    Block object.

    Block is viewed here as an in-game obstacle.
    Block has two states: player can collide with it or cannot collide with it. (states NOT ADDED YET).
    """
    def __init__(self, pos, size, move_x, move_y, is_collision_active=True, block_type=None, texture='wall_stone'):
        super().__init__()
        self.block_type = block_type
        if texture == 'wall_stone_moss1':
            self.image = pygame.transform.scale(img_block_wall_stones_mossy1, (size, size))
        elif texture == 'wall_stone_moss2':
            self.image = pygame.transform.scale(img_block_wall_stones_mossy2, (size, size))
        # Else, Default texture.
        elif texture == 'wall_stone':
            self.image = pygame.transform.scale(img_block_wall_stones, (size, size))

        self.rect = self.image.get_rect(topleft=pos)
        self.move_direction = 1
        self.move_counter = 0
        self.move_x = move_x
        self.move_y = move_y

        self.is_collision_active = is_collision_active

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Ai(pygame.sprite.Sprite):
    """
    Interactable object - object, that player can interact with.

    E.g.: door, torch, vault, chest.
    """
    def __init__(self, pos, size, is_closed=True, is_collision_active=True, block_type=None, texture='door_metal_is_closed'):
        super().__init__()
        self.texture = texture
        if texture == 'door_metal_is_closed':
            self.image = pygame.transform.scale(img_door_metal_closed, (size, size))

        self.rect = self.image.get_rect(topleft=pos)
        self.is_collision_active = is_collision_active
        self.is_closed = is_closed
        self.block_type = block_type
        self.size = size

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift

        if self.texture == 'door_metal_is_opened':
            self.image = pygame.transform.scale(img_door_metal_opened, (self.size, self.size))
        if self.texture == 'door_metal_is_closed':
            self.image = pygame.transform.scale(img_door_metal_closed, (self.size, self.size))


class Lava(pygame.sprite.Sprite):
    """Deadly object."""
    def __init__(self, pos, size, is_collision_active=True, block_type='lava', texture='lava'):
        super().__init__()
        self.texture = texture
        if texture == 'lava':
            self.image = pygame.transform.scale(lava_img, (size, size))

        self.rect = self.image.get_rect(topleft=pos)
        self.is_collision_active = is_collision_active
        self.block_type = block_type
        self.size = size

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, is_collision_active=True):
        """Enemy init."""
        super().__init__()
        self.image = pygame.transform.scale(img_enemy, (57, 57))
        self.rect = self.image.get_rect(topleft=pos)

        self.is_collision_active = is_collision_active

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
