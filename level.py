import pygame
from blocks import *
from settings import *
from player import Player

class Level:
    """Level init."""
    def __init__(self, level_data, surface):
        """Level settings."""
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift_horizontal = 0
        self.world_shift_vertical = 0
        self.current_x = 0

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()

    def create_jump_particles(self, pos):
        pass

    def setup_level(self, layout):
        self.sprites_blocks = pygame.sprite.Group()
        self.sprites_player = pygame.sprite.GroupSingle()
        # Iterate through level layout.
        for row_index, row in enumerate(layout):
            for column_index, block_type in enumerate(row):
                x = column_index * block_size
                y = row_index * block_size

                if block_type == 'B':
                    # Add stone block.
                    block = Block((x, y), block_size, 0, 0, is_collision_active=True)
                    self.sprites_blocks.add(block)

                if block_type == 'S':
                    # Add another stone block.
                    block = Block((x, y), block_size, 1, 0, is_collision_active=True)
                    self.sprites_blocks.add(block)

                if block_type == 'K':
                    # Add another stone block.
                    block = Block((x, y), block_size, 0, 1, is_collision_active=True)
                    self.sprites_blocks.add(block)

                if block_type == 'N':
                    # Add mossy stone block1.
                    block = Block((x, y), block_size, 0, 0, is_collision_active=True, texture='wall_stone_moss1')
                    self.sprites_blocks.add(block)

                if block_type == 'M':
                    # Add mossy stone block2.
                    block = Block((x, y), block_size, 0, 0, is_collision_active=True, texture='wall_stone_moss2')
                    self.sprites_blocks.add(block)

                if block_type == 'D':
                    # Add door.
                    door = IterObject((x, y), block_size, is_collision_active=True, texture='door_metal_is_closed')
                    self.sprites_blocks.add(door)

                if block_type == 'P':
                    player = Player((x, y), (block_size, block_size), self.display_surface, self.create_jump_particles)
                    self.sprites_player.add(player)

                if block_type == 'E':
                    enemy = Enemy((x, y), block_size, is_collision_active=True)
                    self.sprites_blocks.add(enemy)

    def scroll_x(self):
        """Scroll the level horizontally while player is moving."""
        player = self.sprites_player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # Scroll world right if player moving left.
        if player_x < WIDTH / 2 and direction_x < 0 and player.get_input() == 'move_left':
            self.world_shift_horizontal = 5
            player.moving_speed = 0
        # Scroll world left if player moving right.
        elif player_x > WIDTH / 2 and direction_x > 0 and player.get_input() == 'move_right':
            self.world_shift_horizontal = -5
            player.moving_speed = 0

        elif not player.get_input() or player.get_input() == 'move_stop':
            self.world_shift_horizontal = 0
            player.moving_speed = 5

    def collision_horizontal(self):
        """Handle player and objects collision with horizontal movement."""
        player = self.sprites_player.sprite
        player.rect.x += player.direction.x * player.moving_speed

        for block in self.sprites_blocks.sprites():
            # If player collides with any block.
            if block.rect.colliderect(player.rect) and block.is_collision_active == True:
                # If player is moving left and colliding some block => collision happens on the left side of player.
                if player.direction.x < 0:
                    player.rect.left = block.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                # If player is moving right and colliding some block => collision happens on the right side of player.
                elif player.direction.x > 0:
                    player.rect.right = block.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False


    def collision_vertical(self):
        """Handle player and objects collision with vertical movement."""
        player = self.sprites_player.sprite
        # Add gravity
        player.direction.y += player.gravity
        player.rect.y += player.direction.y

        for block in self.sprites_blocks.sprites():
            # If player collides with any block.
            if block.rect.colliderect(player.rect) and block.is_collision_active == True:
                # If player is moving down (falling) and colliding some block => collision happens on the bottom side of player.
                if player.direction.y > 0:
                    player.rect.bottom = block.rect.top
                    player.direction.y = 0  # Set vertical movement to zero when player is standing on something.
                    player.on_ground = True
                    # Player can jump only if it standing on something (avoid double-jump).
                    player.jump()

                elif player.direction.y < 0:
                    player.rect.top = block.rect.bottom
                    player.direction.y = 0  # If player hits something with its head => cancel jumping (avoid sliding while jumping and hitting e.g. ceiling).
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: # if player is jumping or falling, then he isn't on the floor.
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

        player.message(str(player.rect.width))  # TEST, remove later

    def enemy_collision(self):
        """Handle player and enemy collision."""
        pass

    def check_win(self):
        if pygame.sprite.spritecollide(self.sprites_player, self.sprites_blocks(img_door_metal_closed, False)):
            self.setup_level(level_2)


    def run(self):
        """Run (i.e. draw i.e. render) the level."""
        self.sprites_blocks.update(self.world_shift_horizontal, self.world_shift_vertical)
        self.sprites_blocks.draw(self.display_surface)
        self.scroll_x()

        self.sprites_player.update()
        self.collision_horizontal()
        self.collision_vertical()
        self.sprites_player.draw(self.display_surface)
