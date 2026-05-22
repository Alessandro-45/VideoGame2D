import pygame

from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    RENDER_WIDTH,
    RENDER_HEIGHT,
    FPS,
)
from level import Level


class Game:
    def __init__(self):
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2D RPG")
        self.render_surface = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level(self.render_surface)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

    def _draw_to_window(self):
        window_w, window_h = self.display_surface.get_size()
        render_w, render_h = self.render_surface.get_size()
        scale = min(window_w / render_w, window_h / render_h)

        target_size = (int(render_w * scale), int(render_h * scale))
        scaled_surface = pygame.transform.smoothscale(self.render_surface, target_size)

        self.display_surface.fill((10, 10, 12))
        offset_x = (window_w - target_size[0]) // 2
        offset_y = (window_h - target_size[1]) // 2
        self.display_surface.blit(scaled_surface, (offset_x, offset_y))

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self.level.run(dt)
            self._draw_to_window()
            pygame.display.update()
