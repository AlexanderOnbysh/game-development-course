import pygame
from internal.menu import Menu


class Game:
    def __init__(self, window):
        self.menu = ...

        self.running = None
        self.window = window
        self.clock = pygame.time.Clock()
        self.defenses = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.load_level()

    def load_level(self):
        self.menu = Menu(self)

    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.menu.clicked()

            self.menu.update()

            self.window.clear()
            self.menu.draw(self.window.screen)

    def quit(self):
        self.running = False
