import pygame
import pygame_menu
import os
import random

# Game assets settings
game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'images')
player_img = pygame.image.load(os.path.join(img_folder, 'player_test.jpg'))
background_img = pygame.image.load(os.path.join(img_folder, 'bg_test.jpg'))  # CHANGE LATER

# Game main window's dimensions (in pixels).
WIDTH = 1200
HEIGHT = 700

FPS = 30  # Game frames per second.


pygame.init()  # Initialize game constructor.
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the main window.
pygame.display.set_caption("My test")  # Set the name of the game window.
clock = pygame.time.Clock()


# Colors used
color_dark_gray = (100, 100, 100)
color_light_gray = (170, 170, 170)

# Fonts used
font_main_menu = pygame.font.SysFont('Corbel', 35)


# Classes. Every class in pygame mush have 'image' and 'rect' settings.
class Player(pygame.sprite.Sprite):
    """Player class."""
    def __init__(self):
        """Init."""
        pygame.sprite.Sprite.__init__(self)  # Run built-in class 'Sprite' initializer.

        """Test"""
        self.image = player_img
        self.image.set_colorkey((255, 255, 255))  # Ignore white color (works bad).

        self.rect = self.image.get_rect()  # Set object border (aka collision). Border is calculated based on image.
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        """Player actions."""
        pass


# Sprites
all_sprites = pygame.sprite.Group()  # Create group of sprites.
player = Player()  # Create player object.
all_sprites.add(player)  # Add new 'player' object (instance of 'Player' class) to sprites group.


def draw_background():
    # Draw background while main menu is displayed.
    screen.blit(background_img, (0, 0))


def start_the_game():
    # Run the game.
    pass

# Menu
menu_theme = pygame_menu.themes.Theme()  # Main menu object.
menu_theme.background_color = (110, 110, 11)
menu = pygame_menu.Menu('Menu Test', 400, 300, mouse_enabled=True, mouse_motion_selection=True, theme=menu_theme)
menu.add.button('Play', start_the_game())
menu.add.button('Quit', pygame_menu.events.EXIT)

# Main loop.
running = True  # True - game is running, False - quit (end) the game.
while running:
    """
    clock.tick(FPS)  # Maintain the constant FPS.

    all_sprites.update()
    screen.fill((150, 150, 150))
    all_sprites.draw(screen)  # Draw all sprites of group 'all_sprites'.
    """
    menu.mainloop(screen, bgfun=draw_background)

    # Quit the game.
    for event in pygame.event.get():
        # Handle pressing "X (close window)" in the window's upper panel.
        if event.type == pygame.QUIT:
            running = False

    #pygame.display.flip()  # Update screen.
    pygame.display.update()
pygame.quit()  # Close the game application (constructor).
