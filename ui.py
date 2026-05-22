import pygame


class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 24)

    def display(self, surface, health):
        text = self.font.render(f"HP: {health}", True, (245, 245, 245))
        surface.blit(text, (16, 16))
