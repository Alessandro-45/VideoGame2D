import os
import pygame

from settings import GRAPHICS_PATH
from support import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, map_rect):
        super().__init__(groups)
        self.animations = self._load_animations()
        self.status = "down_idle"
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-12, -12)
        self.obstacle_sprites = obstacle_sprites
        self.map_rect = map_rect

        self.direction = pygame.math.Vector2()
        self.speed = 220

        self.health = 100

    def _load_animations(self):
        animation_path = os.path.join(GRAPHICS_PATH, "player")
        animations = {}
        scale_factor = 1.6
        frame_size = (48, 48)

        def load_sequence(prefix):
            frames = []
            for index in range(1, 4):
                file_name = f"{prefix}{index}.png"
                file_path = os.path.join(animation_path, file_name)
                image = load_image(file_path, fallback_size=frame_size)
                new_size = (
                    int(image.get_width() * scale_factor),
                    int(image.get_height() * scale_factor),
                )
                frames.append(pygame.transform.smoothscale(image, new_size))
            return frames

        animations["up"] = load_sequence("personback")
        animations["down"] = load_sequence("persontop")
        animations["left"] = load_sequence("personleft")
        animations["right"] = load_sequence("personright")

        animations["up_idle"] = [animations["up"][0]]
        animations["down_idle"] = [animations["down"][0]]
        animations["left_idle"] = [animations["left"][0]]
        animations["right_idle"] = [animations["right"][0]]

        return animations

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_d] - keys[pygame.K_a]
        self.direction.y = keys[pygame.K_s] - keys[pygame.K_w]

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

    def _update_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.status:
                self.status = f"{self.status}_idle"
        else:
            if "idle" in self.status:
                self.status = self.status.replace("_idle", "")

            if abs(self.direction.x) > abs(self.direction.y):
                self.status = "right" if self.direction.x > 0 else "left"
            else:
                self.status = "down" if self.direction.y > 0 else "up"

    def _animate(self, dt):
        animation = self.animations[self.status]
        self.frame_index += 8 * dt
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def _move(self, dt):
        if self.direction.length_squared() == 0:
            return

        previous_hitbox = self.hitbox.copy()
        self.hitbox.x += self.direction.x * self.speed * dt
        self._collision("horizontal")
        self._stay_in_map()
        self.hitbox.y += self.direction.y * self.speed * dt
        self._collision("vertical")
        self._stay_in_map()
        if self._is_colliding():
            self.hitbox = previous_hitbox
        self.rect.center = self.hitbox.center

    def _stay_in_map(self):
        if self.map_rect is None:
            return
        self.hitbox.clamp_ip(self.map_rect)

    def _collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def _is_colliding(self):
        return any(sprite.hitbox.colliderect(self.hitbox) for sprite in self.obstacle_sprites)

    def update(self, dt):
        self.input()
        self._update_status()
        self._move(dt)
        self._animate(dt)
