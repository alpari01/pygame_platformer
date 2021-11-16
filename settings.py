import pygame
import os

level_layout_intro = [
    '   B                        BBB              ',
    '   B                        B                ',
    '   B             B          BB               ',
    '   B                        B                ',
    '   B              B         B                ',
    '   B                     BBBB                ',
    '   B              P        B                 ',
    '   B    B            B     B                 ',
    '   B                                         ',
    '   B            B    B                       ',
    '   B                 B                       ',
    '                     B       B NNN           ',
    'BBBBBBBBBBBMMMMMMBBBMMBBBBBBBBBBBBBBBBBBBBBBB'
]
# Blocks types: B - stone block, N - stone mossy block1, M - stone mossy block2.
block_size = 48  # Size of a single block.

# Game main window's dimensions (in pixels).
WIDTH = 1200
HEIGHT = 720


# Game assets settings
game_folder = os.path.dirname(__file__)

img_folder = os.path.join(game_folder, 'images')  # All textures go here.

# Player action images.
img_player_running_0 = pygame.image.load(os.path.join(img_folder, 'running_0.png'))
img_player_running_1 = pygame.image.load(os.path.join(img_folder, 'running_1.png'))
img_player_running_2 = pygame.image.load(os.path.join(img_folder, 'running_2.png'))
img_player_running_3 = pygame.image.load(os.path.join(img_folder, 'running_3.png'))
img_player_running_4 = pygame.image.load(os.path.join(img_folder, 'running_4.png'))
img_player_running_5 = pygame.image.load(os.path.join(img_folder, 'running_5.png'))
img_player_running_6 = pygame.image.load(os.path.join(img_folder, 'running_6.png'))
img_player_running_7 = pygame.image.load(os.path.join(img_folder, 'running_7.png'))

img_player_jumping = pygame.image.load(os.path.join(img_folder, 'jumping.png'))


anim_running = [img_player_running_0, img_player_running_1, img_player_running_2,
                img_player_running_3, img_player_running_4, img_player_running_5,
                img_player_running_6, img_player_running_7]

# Player idle images.
img_player_idle_0 = pygame.image.load(os.path.join(img_folder, 'idle_0.png'))

# Background images.
img_background_menu = pygame.image.load(os.path.join(img_folder, 'bg_test.jpg'))  # CHANGE LATER
img_background_menu_rect = img_background_menu.get_rect()

img_background_first_level = pygame.image.load(os.path.join(img_folder, 'first_level_bg_test.jpg'))  # CHANGE LATER
img_background_first_level_rect = img_background_first_level.get_rect()

IMAGE_ADD_SCALE = 28  # Increase player scale of images by this value.

# Blocks textures.
img_block_wall_stones = pygame.image.load(os.path.join(img_folder, 'wall_stones.png'))
img_block_wall_stones_mossy1 = pygame.image.load(os.path.join(img_folder, 'wall_stones_mossy1.png'))
img_block_wall_stones_mossy2 = pygame.image.load(os.path.join(img_folder, 'wall_stones_mossy2.png'))

# Fonts used.
pygame.font.init()  # Calling font module.
font_player_message = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the main window.
