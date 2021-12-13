import pygame
import pygame_menu
from pygame import mixer

from enemy_quest import EnemyQuest
from settings import *
from level import Level

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()  # Initialize game constructor.


FPS = 60  # Game frames per second.


pygame.display.set_caption("My test")  # Set the name of the game window.

clock = pygame.time.Clock()



# Sprites
sprites_player = pygame.sprite.Group()  # Create group of sprites.
sprites_blocks = pygame.sprite.Group()  # Create another group of sprites.
sprites_enemy = pygame.sprite.Group()

# Quests
enemy_quest = EnemyQuest(WIDTH // 2, HEIGHT // 2, img_quest_background)

# Sounds
jumping = pygame.mixer.Sound('jump.wav')
jumping.set_volume(0.5)
play = pygame.mixer.Sound('play.wav')
play.set_volume(0.5)


def draw_background(level: int = 0):
    """
    Draw background image according to the current level.

    :param level: current level. This variable sets which type of image to render at background.
    :return: None
    """
    screen.blit(img_background_menu, img_background_menu_rect) # Menu
    if level == 1:
        # First (intro) level.
        screen.blit(img_background_first_level, img_background_first_level_rect)


def menu_close():
    # Close the menu and start the game. Invoke while 'Play' button is pressed.
    play.play()
    menu.disable()


def menu_show():
    """Show the main menu at start."""
    menu.mainloop(screen, bgfun=draw_background)


# Menu
menu_theme = pygame_menu.themes.Theme()  # Main menu object.
menu_theme.background_color = (110, 110, 11)
menu = pygame_menu.Menu('Menu Test', 400, 300, mouse_enabled=True, mouse_motion_selection=True, theme=menu_theme)
menu.add.button('Play', menu_close)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Show the main menu at start
menu_show()

# Level
level = Level(level_layout_intro, screen)  # Create level object.

# Main loop.
running = True  # True - game is running, False - quit (end) the game.
while running:
    # Handel keyboard actions.
    for event in pygame.event.get():
        # Handle pressing "X (close window)" in the window's upper panel.
        if event.type == pygame.QUIT:
            # Stop the game => Exit.
            running = False
        # Handle 'jumping' action.

    # Update objects on the screen.
    draw_background(1)


    # DO NOT remove these :)
    level.run()
    clock.tick(FPS)  # Maintain the constant FPS.
    pygame.display.flip()  # Update screen.


pygame.quit()  # Close the game application (constructor).
