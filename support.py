import os
import pygame

from settings import TILE_SIZE


def import_folder(path):
    frames = []
    if not os.path.exists(path):
        return frames

    for file_name in sorted(os.listdir(path)):
        if not file_name.lower().endswith(".png"):
            continue
        full_path = os.path.join(path, file_name)
        frames.append(pygame.image.load(full_path).convert_alpha())

    return frames


def load_image(path, size=None, fallback_size=None):
    try:
        image = pygame.image.load(path).convert_alpha()
    except pygame.error:
        return _placeholder_surface(size or fallback_size or (TILE_SIZE, TILE_SIZE))

    if size:
        image = pygame.transform.smoothscale(image, size)

    return image


def _placeholder_surface(size):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill((35, 35, 35))
    pygame.draw.rect(surface, (200, 70, 70), surface.get_rect(), 3)
    pygame.draw.line(surface, (200, 70, 70), (0, 0), (size[0], size[1]), 2)
    pygame.draw.line(surface, (200, 70, 70), (0, size[1]), (size[0], 0), 2)
    return surface
