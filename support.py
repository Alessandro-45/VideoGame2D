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


def extract_sprites_from_atlas(path, alpha_threshold=1, min_size=(2, 2)):
    # Finds distinct opaque regions inside a single atlas image and returns
    # each region as its own surface, avoiding manual sprite slicing.
    try:
        atlas = pygame.image.load(path).convert_alpha()
    except pygame.error:
        return [_placeholder_surface((TILE_SIZE, TILE_SIZE))]

    width, height = atlas.get_size()
    has_transparency = False
    for y in range(height):
        for x in range(width):
            if atlas.get_at((x, y)).a <= alpha_threshold:
                has_transparency = True
                break
        if has_transparency:
            break

    if not has_transparency:
        background_color = atlas.get_at((0, 0))
        atlas = atlas.convert()
        atlas.set_colorkey(background_color)
        atlas = atlas.convert_alpha()

    mask = pygame.mask.from_surface(atlas, alpha_threshold)
    rects = mask.get_bounding_rects()
    rects.sort(key=lambda rect: (rect.top, rect.left))

    sprites = []
    for rect in rects:
        if rect.width < min_size[0] or rect.height < min_size[1]:
            continue
        sprites.append(atlas.subsurface(rect).copy())

    return sprites


def _placeholder_surface(size):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill((35, 35, 35))
    pygame.draw.rect(surface, (200, 70, 70), surface.get_rect(), 3)
    pygame.draw.line(surface, (200, 70, 70), (0, 0), (size[0], size[1]), 2)
    pygame.draw.line(surface, (200, 70, 70), (0, size[1]), (size[0], 0), 2)
    return surface
