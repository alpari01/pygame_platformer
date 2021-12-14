import pygame
from pygame import mixer
from settings import *
from support import import_folder
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size, surface, create_jump_particles):
        """Player init."""
        super().__init__()
        self.image = pygame.transform.scale(img_player_idle_0, (block_size, block_size))
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.moving_speed = 5  # Player moving speed.
        self.direction = pygame.math.Vector2(0, 0)  # Player moving direction.
        self.gravity = 0.8
        self.jump_height = -20

        # Animations
        self.image_index = 0
        self.idle_direction = 'right'

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

    def import_dust_run_particles(self):
        path = os.getcwd()
        self.dust_run_particles = import_folder(path + '/images/dust_run')

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle, pos)

            else:
                pos = pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False) # horizontal flip/vertical flip
                self.display_surface.blit(flipped_dust_particle, pos)


    def get_input(self):
        """Handle user input from keyboard and animations."""
        keys = pygame.key.get_pressed()  # Get all the keys that are currently pressed.

        # If user presses 'right arrow' => player move right.
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 1
            self.facing_right = True

            # Change animation to running (do loop through running poses).
            self.image = pygame.transform.scale(anim_running[int(self.image_index)], (block_size, block_size))
            self.image_index += 0.1  # Animation frames changing speed.
            if self.image_index >= len(anim_running):
                self.image_index = 0

            self.idle_direction = 'right'
            return 'move_right'

        # If user presses 'left arrow' => player move left.
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
            self.facing_right = False

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

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):  # working kinda weird
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """Handle jumping."""
        # If user presses 'Space' => player jump.
        keys = pygame.key.get_pressed()  # Get all the keys that are currently pressed.
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            jumping = pygame.mixer.Sound('jump.wav')
            jumping.set_volume(0.5)
            jumping.play()
            self.direction.y = self.jump_height
            # self.create_jump_particles(self.rect.midbottom)

    def message(self, text: str):
        """Handle player messages (aka player's thoughts)."""
        text_player = font_message.render(text, False, (0, 0, 0))  # Create text object.
        screen.blit(text_player, (self.rect.x - (len(text) * 10 // 2), self.rect.y - 50))  # Show text on the screen.

    def update(self):
        """Player update."""
        self.get_input()
        self.rect.x += self.direction.x
        # self.apply_gravity()
        self.get_status()
        self.run_dust_animation()
