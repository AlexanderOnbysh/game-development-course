import pygame

from .menu import Interface


class Game:
    def __init__(self, window):
        self.running = True
        self.window = window
        self.clock = pygame.time.Clock()
        self.menu = Interface(self)

    def run(self):
        while self.running:
            self.clock.tick(60)

            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            # redraw screen
            self.window.clear()
            self.menu.draw(self.window.screen)

    def quit(self):
        self.running = False
