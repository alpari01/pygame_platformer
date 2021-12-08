import pygame
from settings import *


class Block(pygame.sprite.Sprite):
    """
    Block object.

    Block is viewed here as an in-game obstacle.
    Block has two states: player can collide with it or cannot collide with it. (states NOT ADDED YET).
    """
    def __init__(self, pos, size, move_x, move_y, texture='wall_stone'):
        super().__init__()
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

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class IterObject(pygame.sprite.Sprite):
    """
    Interactable object - object, that player can interact with.

    E.g.: door, torch, vault, chest.
    """
    def __init__(self, pos, size, texture='door_metal_is_closed'):
        super().__init__()
        if texture == 'door_metal_is_closed':
            self.image = pygame.transform.scale(img_door_metal_closed, (size, size))
        if texture == 'door_metal_is_opened':
            self.image = pygame.transform.scale(img_door_metal_opened, (size, size))

        self.rect = self.image.get_rect(topleft=pos)

    def message(self, text: str):
        """Display message near the object if player has approach it and pressed interaction button 'E'."""
        text_iter_object = font_message.render(text, False, (0, 0, 0))  # Crete text object.
        screen.blit(text_iter_object, (self.rect.x - (len(text) * 10 // 2), self.rect.y - 50))  # Show text on the screen.

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        """Enemy init."""
        super().__init__()
        self.image = pygame.transform.scale(img_enemy, (57, 57))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift
