import pygame


class Window:
    def __init__(self, width: int, height: int):
        self.resolution = (width, height)
        self.screen = pygame.display.set_mode(self.resolution)
        self.set_background(0, 0, 0)

    def set_title(self, title):
        pygame.display.set_caption(title)

    def set_background(self, r, g, b):
        self.background = pygame.Surface(self.resolution)
        self.background.fill(pygame.Color(r, g, b))
        self.background = self.background.convert()

    def clear(self):
        pygame.display.flip()
        self.screen.blit(self.background, (0, 0))
