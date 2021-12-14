import pygame.mouse
from settings import *


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (10, 160, 60)
        self.active_color = (20, 200, 60)

    def draw(self, x, y, message, action=None, font_size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if (x < mouse[0] < x + self.width) and (y < mouse[1] < y + self.height):
            pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))

            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))

        self.print_text(message, x + 10, y + 10)

    def print_text(self, text, x, y, font_color=(0, 0, 0), font_size=30):
        font_type = pygame.font.SysFont('8BIT', font_size)
        text = font_type.render(text, True, font_color)
        screen.blit(text, (x, y))
