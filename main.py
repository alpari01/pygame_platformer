import pygame
import pygame_menu
from pygame import mixer

import player
from blocks import Lava
from settings import *
from level import Level

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()  # Initialize game constructor.


FPS = 60  # Game frames per second.


pygame.display.set_caption("Project 004")  # Set the name of the game window.

clock = pygame.time.Clock()

# Level
level1 = Level(level_layout_intro, screen)  # Create level object.
level2 = Level(level_2, screen)

# Sprites
sprites_player = pygame.sprite.Group()  # Create group of sprites.
sprites_blocks = pygame.sprite.Group()  # Create another group of sprites.
sprites_enemy = pygame.sprite.Group()
sprites_ai = pygame.sprite.Group()

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
font = pygame_menu.font.FONT_8BIT
menu_theme = pygame_menu.themes.Theme(widget_font=font, title_font=pygame_menu.font.FONT_8BIT,
                                      title_font_antialias=True, title_background_color=(0, 0, 0, 0),
                                      title_offset=(116, 50))  # Main menu object.
menu_theme.background_color = (0, 0, 0, 0)
menu = pygame_menu.Menu('Menu', 400, 300, mouse_enabled=True, mouse_motion_selection=True, theme=menu_theme)

menu.add.button('Play', menu_close)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Show the main menu at start
menu_show()


def choose_level_close():
    choose_level.disable()
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
        level1.run()
        clock.tick(FPS)  # Maintain the constant FPS.
        pygame.display.flip()  # Update screen.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    draw_background(1)
                    level1.setup_level(level_2)
                    choose_level_close_2()
                    clock.tick(FPS)
                    pygame.display.flip()


def choose_level_close_2():
    choose_level.disable()
    running = True  # True - game is running, False - quit (end) the game.
    while running:
        # Handle keyboard actions.
        for event in pygame.event.get():
            # Handle pressing "X (close window)" in the window's upper panel.
            if event.type == pygame.QUIT:
                # Stop the game => Exit.
                running = False
            # Handle 'jumping' action.

        # Update objects on the screen.
        draw_background(1)

        # DO NOT remove these :)
        level2.run()
        clock.tick(FPS)  # Maintain the constant FPS.
        pygame.display.flip()  # Update screen.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    draw_background(1)
                    level2.setup_level(level_end)
                    clock.tick(FPS)
                    pygame.display.flip()


def choose_level_show():
    """Show the main menu at start."""
    choose_level.mainloop(screen, bgfun=draw_background)


font = pygame_menu.font.FONT_8BIT
theme = pygame_menu.themes.Theme(widget_font=font, title_font=pygame_menu.font.FONT_8BIT,
                                      title_font_antialias=True, title_background_color=(0, 0, 0, 0),
                                      title_offset=(0, 50))  # Main menu object.
theme.background_color = (0, 0, 0, 0)
choose_level = pygame_menu.Menu('Choose level', 400, 300, mouse_enabled=True, mouse_motion_selection=True, theme=theme)

choose_level.add.button('Level 1', choose_level_close)
choose_level.add.button('Level 2', choose_level_close_2)

choose_level_show()

pygame.quit()  # Close the game application (constructor).
