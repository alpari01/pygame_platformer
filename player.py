import pygame
from pygame import mixer
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        """Player init."""
        super().__init__()
        self.image = pygame.transform.scale(img_player_idle_0,  (block_size, block_size))
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.moving_speed = 5  # Player moving speed.
        self.direction = pygame.math.Vector2(0, 0)  # Player moving direction.
        self.gravity = 0.8
        self.jump_height = -20

        # Animations
        self.image_index = 0
        self.idle_direction = 'right'

    def get_input(self):
        """Handle user input from keyboard and animations."""
        keys = pygame.key.get_pressed()  # Get all the keys that are currently pressed.

        # If user presses 'right arrow' => player move right.
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = self.moving_speed

            # Change animation to running (do loop through running poses).
            self.image = pygame.transform.scale(anim_running[int(self.image_index)], (block_size, block_size))
            self.image_index += 0.1  # Animation frames changing speed.
            if self.image_index >= len(anim_running):
                self.image_index = 0

            self.idle_direction = 'right'
            return 'move_right'

        # If user presses 'left arrow' => player move left.
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -self.moving_speed

            # Change animation to running left (do loop through running poses)..
            self.image = pygame.transform.scale(anim_running[int(self.image_index)], (block_size, block_size))
            self.image = pygame.transform.flip(self.image, True, False)
            self.image_index += 0.1  # Animation frames changing speed.
            if self.image_index >= len(anim_running):
                self.image_index = 0

            self.idle_direction = 'left'
            return 'move_left'

        # If user pressed both (left and right arrows) or does not press whether right or left arrow by once => player stop moving.
        elif keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            self.direction.x = 0

            return 'move_stop'

        # Other key cases => player do not move.
        else:
            self.direction.x = 0

            # Show idle pose.
            if self.idle_direction == 'left':
                self.image = pygame.transform.scale(img_player_idle_0, (block_size, block_size))
                self.image = pygame.transform.flip(self.image, True, False)

            if self.idle_direction == 'right':
                self.image = pygame.transform.scale(img_player_idle_0, (block_size, block_size))

    def jump(self):
        """Handle jumping."""
        # If user presses 'Space' => player jump.
        keys = pygame.key.get_pressed()  # Get all the keys that are currently pressed.
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            jumping = pygame.mixer.Sound('jump.wav')
            jumping.set_volume(0.5)
            jumping.play()
            self.direction.y = self.jump_height

    def message(self, text: str):
        """Handle player messages (aka player's thoughts)."""
        text_player = font_message.render(text, False, (0, 0, 0))  # Crete text object.
        screen.blit(text_player, (self.rect.x - (len(text) * 10 // 2), self.rect.y - 50))  # Show text on the screen.

    def update(self):
        """Player update."""
        self.get_input()
