import pygame


class TextMenu(pygame.sprite.Sprite):
    """Pop-up menu class. Used in quests."""

    def __init__(self, font, text):
        super().__init__()
        self.image = pygame.Surface((200, 200))
        self.image.fill(pygame.Color('white'))

    def update(self):
        pass