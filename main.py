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

FPS = 60  # Game frames per second.

# Movement parameters.
ACC = 0.5  # Linear speed while moving.
FRIC = -0.12  # Friction. While running player won't stop immediately (add some slide effect).
vec = pygame.math.Vector2  # Constant 2 vector to handle movement in both directions (horizontally and vertically).

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
        super().__init__()  # Run built-in class 'Sprite' initializer.

        # Test image
        #self.image = player_img
        #self.image.set_colorkey((255, 255, 255))  # Ignore white color (works bad).

        self.surf = pygame.Surface((50, 50))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()  # Set object border (aka collision). Border is calculated based on image.

        self.pos = vec((WIDTH / 2, HEIGHT / 2))
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

    def move(self):
        """Player movement."""
        self.acc = vec(0, 0.5)  # By default player's speed is zero.

        # Player does not move until certain buttons is pressed.
        keystate = pygame.key.get_pressed()  # Get dict with all buttons available in pygame.
        if keystate[pygame.K_LEFT]:
            # If 'LeftArrow' is pressed, player move left.
            self.acc.x = -ACC
        if keystate[pygame.K_RIGHT]:
            # If 'RightArrow' is pressed, player move right.
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, sprites_platforms, False)  # Do not jump while already jumping (avoid double-jump).
        if hits:
            self.vel.y = -15  # Assign the negative value since the jump goes up, not down.

    def update(self):
        """Handle hits (collisions) with other game objects (sprites)."""
        hits = pygame.sprite.spritecollide(player, sprites_platforms, False)  # False - do not delete sprite after collision.
        if player.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

    def move(self):
        pass

# Sprites
sprites_player = pygame.sprite.Group()  # Create group of sprites.
sprites_platforms = pygame.sprite.Group()  # Create another group of sprites.

player = Player()  # Create player object.
platform = Platform()  # Create platform object.

sprites_player.add(player)  # Add new 'player' object (instance of 'Player' class) to sprites group.

sprites_platforms.add(platform)


def draw_background():
    # Draw background while main menu is displayed.
    screen.blit(background_img, (0, 0))


def menu_close():
    # Close the menu and start the game. Invoke while 'Play' button is pressed.
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

# Show the main menu ar start
menu_show()

# Main loop.
running = True  # True - game is running, False - quit (end) the game.
while running:

    # Handel keyboard actions.
    for event in pygame.event.get():
        # Handle pressing "X (close window)" in the window's upper panel.
        if event.type == pygame.QUIT:
            # Stop the game => Exit.
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Jump by pressing 'Spacebar' or 'UpArrow'
                player.jump()

    screen.fill((120, 120, 120))
    player.move()
    player.update()

    # Update objects on the screen.
    for sprite in sprites_player:
        screen.blit(sprite.surf, sprite.rect)
    for sprite in sprites_platforms:
        screen.blit(sprite.surf, sprite.rect)


    clock.tick(FPS)  # Maintain the constant FPS.
    pygame.display.flip()  # Update screen.


pygame.quit()  # Close the game application (constructor).
