import pygame
import pygame_menu
import os
import threading
import random

pygame.init()  # Initialize game constructor.

# Game main window's dimensions (in pixels).
WIDTH = 1200
HEIGHT = 700

FPS = 60  # Game frames per second.

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set up the main window.
pygame.display.set_caption("My test")  # Set the name of the game window.

clock = pygame.time.Clock()


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

# Player idle images
img_player_idle_0 = pygame.image.load(os.path.join(img_folder, 'idle_0.png'))

# Background images.
img_background_menu = pygame.image.load(os.path.join(img_folder, 'bg_test.jpg')).convert()  # CHANGE LATER
img_background_menu_rect = img_background_menu.get_rect()

img_background_first_level = pygame.image.load(os.path.join(img_folder, 'first_level_bg_test.jpg')).convert()  # CHANGE LATER
img_background_first_level_rect = img_background_first_level.get_rect()

IMAGE_ADD_SCALE = 32  # Increase scale of images by this value.

# Movement parameters.
ACC = 5  # Linear speed while moving.
FRIC = -0.12  # Friction. While running player won't stop immediately (add some slide effect).
vec = pygame.math.Vector2  # Constant 2 vector to handle movement in both directions (horizontally and vertically).



# Colors used
color_dark_gray = (100, 100, 100)
color_light_gray = (170, 170, 170)

# Fonts used
pygame.font.init()  # Calling font module.
font_player_message = pygame.font.SysFont('Comic Sans MS', 30)


# Classes. Every class in pygame mush have 'image' and 'rect' settings.
class Player(pygame.sprite.Sprite):
    """Player class."""
    def __init__(self):
        """Init."""
        super().__init__()  # Run built-in class 'Sprite' initializer.

        self.image = pygame.transform.scale(img_player_idle_0, (19 + IMAGE_ADD_SCALE, 20 + IMAGE_ADD_SCALE))
        self.rect = self.image.get_rect()

        self.pos = vec((WIDTH / 2, HEIGHT / 2))
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)

        self.image_index = 0
        self.idle_direction = 'right'  # 'Left' - player watches left side while stops, 'Right' - player watches right.

    def move(self):
        """Player movement."""
        self.acc = vec(0, 0.5)  # By default player's speed is zero.

        # Player does not move until certain buttons is pressed.
        keystate = pygame.key.get_pressed()  # Get dict with all buttons available in pygame.
        if keystate[pygame.K_LEFT]:
            # If 'LeftArrow' is pressed, player move left.
            self.vel.x = -ACC

            # If player is in the air (does not touch other objects), then show jumping pose.
            if not pygame.sprite.spritecollide(self, sprites_obstacles, False):
                self.image = pygame.transform.scale(img_player_jumping, (19 + IMAGE_ADD_SCALE, 20 + IMAGE_ADD_SCALE))
                self.image = pygame.transform.flip(self.image, True, False)

            # If player is moving left and touching other objects (e.g. ground).
            if pygame.sprite.spritecollide(self, sprites_obstacles, False):
                # Change animation to running.
                self.image = pygame.transform.scale(anim_running[self.image_index], (19 + IMAGE_ADD_SCALE, 20 + IMAGE_ADD_SCALE))
                self.image = pygame.transform.flip(self.image, True, False)
                self.image_index += 1
                if self.image_index + 1 == len(anim_running):
                    self.image_index = 0
                self.idle_direction = 'left'

        if keystate[pygame.K_RIGHT]:
            # If 'RightArrow' is pressed, player move right.
            self.vel.x = ACC

            # If player is in the air (does not touch other objects), then show jumping pose.
            if not pygame.sprite.spritecollide(self, sprites_obstacles, False):
                self.image = pygame.transform.scale(img_player_jumping, (19 + IMAGE_ADD_SCALE, 20 + IMAGE_ADD_SCALE))

            if pygame.sprite.spritecollide(self, sprites_obstacles, False):
                # Change animation to running (do loop through running poses).
                self.image = pygame.transform.scale(anim_running[self.image_index], (19 + IMAGE_ADD_SCALE, 20 + IMAGE_ADD_SCALE))
                self.image_index += 1
                if self.image_index + 1 == len(anim_running):
                    self.image_index = 0
                self.idle_direction = 'right'

        if not keystate[pygame.K_RIGHT] and not keystate[pygame.K_LEFT]:
            # If moving buttons are not pressed => player stop, show idle animation.
            self.vel.x = 0

            if self.idle_direction == 'left':
                self.image = pygame.transform.scale(img_player_idle_0, (19 + IMAGE_ADD_SCALE, 20 + IMAGE_ADD_SCALE))
                self.image = pygame.transform.flip(self.image, True, False)

            if self.idle_direction == 'right':
                self.image = pygame.transform.scale(img_player_idle_0, (19 + IMAGE_ADD_SCALE, 20 + IMAGE_ADD_SCALE))

        self.vel += self.acc
        self.pos += self.vel

        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, sprites_obstacles, False)  # Handle player sprite collision with other sprites (e.g. obstacle sprites).
        # Do not jump while already jumping (avoid double-jump).
        if hits:
            self.vel.y = -15  # Assign the negative value since the jump goes up, not down.

    def message(self, text: str):
        """Handle player messages (aka player's thoughts)."""
        text_player = font_player_message.render(text, False, (0, 0, 0))  # Crete text object.
        screen.blit(text_player, (self.rect.x - (len(text) * 10 // 2), self.rect.y - 50))  # Show text on the screen.

    def update(self):
        """Handle hits (collisions) with other game objects (sprites)."""
        hits = pygame.sprite.spritecollide(player, sprites_obstacles, False)  # False - do not delete sprite after collision.
        if player.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0


class Platform(pygame.sprite.Sprite):
    """Ground. Player cannot go beyond the world's absolute ground."""
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 5))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

    def move(self):
        pass


class Obstacle(pygame.sprite.Sprite):
    """
    Obstacle class.

    Can be 1x1 square, 1x0.5 square, triangle, rectangle of fixed types.
    Rectangle fixed types: 1x2, 2x2, 2x4, 4x4 ???
    """
    def __init__(self, width, height, pos_x, pos_y, move_x, move_y):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect()
        self.surf.fill((0, 150, 0))

        self.pos = vec((pos_x, pos_y))
        self.rect.midbottom = self.pos
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x  # if move_x value is not 0, the obstacle moves right and left
        self.move_y = move_y  # if move_y value is not 0, the obstacle moves up and down

    def update(self):
        self.rect.x += self.move_direction * self.move_x  # move_direction is now manipulated by move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


# Sprites
sprites_player = pygame.sprite.Group()  # Create group of sprites.
sprites_obstacles = pygame.sprite.Group()  # Create another group of sprites.

player = Player()  # Create player object.
platform_world_ground = Platform()  # Create platform object.
obstacle2 = Obstacle(100, 100, 800, 700, 1, 0)
obstacle1 = Obstacle(100, 50, 500, 500, 0, 1)


sprites_player.add(player)  # Add new 'player' object (instance of 'Player' class) to sprites group.

sprites_obstacles.add(platform_world_ground)
sprites_obstacles.add(obstacle2)
sprites_obstacles.add(obstacle1)


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
        # Handle 'jumping' action.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Jump by pressing 'Spacebar' or 'UpArrow'
                player.jump()
    # Update objects on the screen.
    draw_background(1)

    player.message("Hello, world!")  # TEST, remove later

    for sprite in sprites_player:
        screen.blit(sprite.image, sprite.rect)
    for sprite in sprites_obstacles:
        screen.blit(sprite.surf, sprite.rect)

    # Scroll screen while player is moving.
    if player.rect.right >= WIDTH / 2:
        # If player's position is far right from middle of the screen.
        player.pos.x -= abs(player.vel.x)  # Update player's position (remove negative value, use abs for this).
        # Update obstacles' positions.
        for obstacle in sprites_obstacles:
            obstacle.rect.x -= abs(player.vel.x)
    if player.rect.left < WIDTH / 2:
        # If player's position is far left from middle of the screen.
        player.pos.x += abs(player.vel.x)
        for obstacle in sprites_obstacles:
            obstacle.rect.x += abs(player.vel.x)

    # DO NOT remove these :)
    obstacle1.update()
    obstacle2.update()
    player.move()
    player.update()
    clock.tick(FPS)  # Maintain the constant FPS.
    pygame.display.flip()  # Update screen.


pygame.quit()  # Close the game application (constructor).
