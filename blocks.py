import pygame
from settings import *

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, size, texture='wall_stone'):
        super().__init__()
        #self.image = pygame.Surface((size, size))
        if texture == 'wall_stone_moss1':
            self.image = pygame.transform.scale(img_block_wall_stones_mossy1, (size, size))
        elif texture == 'wall_stone_moss2':
            self.image = pygame.transform.scale(img_block_wall_stones_mossy2, (size, size))
        # Else, Default texture.
        elif texture == 'wall_stone':
            self.image = pygame.transform.scale(img_block_wall_stones, (size, size))

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift