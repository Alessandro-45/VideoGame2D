import os
import pygame

from settings import GRAPHICS_PATH, RENDER_WIDTH, RENDER_HEIGHT, TILE_SIZE
from support import load_image
from tile import Tile
from player import Player
from ui import UI


class CameraGroup(pygame.sprite.Group):
    def __init__(self, render_surface):
        super().__init__()
        self.render_surface = render_surface
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - (RENDER_WIDTH / 2)
        self.offset.y = player.rect.centery - (RENDER_HEIGHT / 2)

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.render_surface.blit(sprite.image, offset_pos)


class Level:
    def __init__(self, render_surface):
        self.render_surface = render_surface
        self.visible_sprites = CameraGroup(render_surface)
        self.obstacle_sprites = pygame.sprite.Group()
        self.ui = UI()

        self._create_map()

    def _create_map(self):
        layout = [
            "xxxxxxxxxxxxxxxxxxxx",
            "x..................x",
            "x..xx........xx....x",
            "x..................x",
            "x.......p..........x",
            "x..................x",
            "x..xx........xx....x",
            "x..................x",
            "x..................x",
            "xxxxxxxxxxxxxxxxxxxx",
        ]

        floor_path = os.path.join(GRAPHICS_PATH, "tiles", "floor.png")
        floor_tile = load_image(floor_path, size=(TILE_SIZE, TILE_SIZE))
        wall_path = os.path.join(GRAPHICS_PATH, "tiles", "wall.png")
        wall_tile = load_image(wall_path, size=(TILE_SIZE, TILE_SIZE))

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if cell == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], wall_tile)
                else:
                    Tile((x, y), [self.visible_sprites], floor_tile)

                if cell == "p":
                    player_pos = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
                    self.player = Player(player_pos, [self.visible_sprites], self.obstacle_sprites)

    def run(self, dt):
        self.render_surface.fill((24, 24, 28))
        self.visible_sprites.update(dt)
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.render_surface, self.player.health)
