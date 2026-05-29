import os
import pygame

from settings import GRAPHICS_PATH, RENDER_WIDTH, RENDER_HEIGHT
from support import extract_sprites_from_atlas, load_image
from player import Player
from ui import UI


class CameraGroup(pygame.sprite.Group):
    def __init__(self, render_surface):
        super().__init__()
        self.render_surface = render_surface
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player, background=None, background_rect=None):
        self.offset.x = player.rect.centerx - (RENDER_WIDTH / 2)
        self.offset.y = player.rect.centery - (RENDER_HEIGHT / 2)

        if background is not None and background_rect is not None:
            background_pos = background_rect.topleft - self.offset
            self.render_surface.blit(background, background_pos)

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.render_surface.blit(sprite.image, offset_pos)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(midbottom=pos)
        self.hitbox = self.rect.inflate(-18, -18)


class Level:
    def __init__(self, render_surface):
        self.render_surface = render_surface
        self.visible_sprites = CameraGroup(render_surface)
        self.obstacle_sprites = pygame.sprite.Group()
        self.ui = UI()

        self._create_map()

    def _create_map(self):
        background_path = os.path.join(GRAPHICS_PATH, "grassland3.png")
        background = load_image(background_path)
        self.background = pygame.transform.smoothscale(
            background,
            (background.get_width() * 12, background.get_height() * 12),
        )
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        # Atlas-driven decorations: auto-extract each tree/trunk from one image,
        # then place them around the map without manual slicing.
        decorations_path = os.path.join(GRAPHICS_PATH, "grasslands decorative.png")
        decorations = extract_sprites_from_atlas(decorations_path)
        decorations = [
            surface
            for surface in decorations
            if surface.get_width() * surface.get_height() >= 120
        ]
        self._place_decorations(decorations)

        player_pos = (
            self.background_rect.width * 0.5,
            self.background_rect.height * 0.55,
        )
        self.player = Player(
            player_pos,
            [self.visible_sprites],
            self.obstacle_sprites,
            self.background_rect,
        )

    def _place_decorations(self, decorations):
        if not decorations:
            return

        map_w, map_h = self.background_rect.size
        points = [
            (0.10, 0.16), (0.18, 0.28), (0.12, 0.42), (0.08, 0.62), (0.16, 0.78),
            (0.28, 0.18), (0.32, 0.36), (0.26, 0.56), (0.30, 0.72), (0.24, 0.88),
            (0.42, 0.14), (0.46, 0.32), (0.40, 0.48), (0.44, 0.66), (0.38, 0.82),
            (0.52, 0.22), (0.56, 0.38), (0.50, 0.54), (0.54, 0.70), (0.48, 0.86),
            (0.62, 0.12), (0.68, 0.30), (0.64, 0.50), (0.70, 0.68), (0.60, 0.84),
            (0.76, 0.20), (0.82, 0.36), (0.78, 0.54), (0.84, 0.72), (0.74, 0.88),
            (0.90, 0.24), (0.92, 0.44), (0.88, 0.60), (0.90, 0.78),
            (0.50, 0.44), (0.52, 0.60), (0.46, 0.58), (0.58, 0.46),
        ]

        coords = [(int(map_w * px), int(map_h * py)) for px, py in points]

        for index, pos in enumerate(coords):
            if not decorations:
                break
            surface = decorations[index % len(decorations)]
            scaled = pygame.transform.smoothscale(
                surface,
                (surface.get_width() * 2, surface.get_height() * 2),
            )
            sprite = Decoration(pos, [self.visible_sprites, self.obstacle_sprites], scaled)
            sprite.rect.clamp_ip(self.background_rect)
            sprite.hitbox.center = sprite.rect.center

    def run(self, dt):
        self.render_surface.fill((24, 24, 28))
        self.visible_sprites.update(dt)
        self.visible_sprites.custom_draw(self.player, self.background, self.background_rect)
        self.ui.display(self.render_surface, self.player.health)
