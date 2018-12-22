import pygame
from typing import Tuple


class Window:
    def __init__(self, resolution: Tuple[int, int]):
        self.resolution = resolution
        self.screen = pygame.display.set_mode(self.resolution)
        self.set_background(0, 0, 0)

    @staticmethod
    def set_title(title):
        pygame.display.set_caption(title)

    def set_background(self, r, g, b):
        self.background = pygame.Surface(self.resolution)
        self.background.fill(pygame.Color(r, g, b))
        self.background = self.background.convert()

    def clear(self):
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
