import pygame
from internal.defense import Defense
from internal.menu import Menu


class Game:
    def __init__(self, window):
        self.running = None

        self.window = window
        self.clock = pygame.time.Clock()
        self.defenses = pygame.sprite.Group()
        self.load_level()
        self.defense_type = 0
        self.defense_prototypes = [Defense(self, 'Defense' + name, -100, -100)
                                   for name in ['Pillbox', 'Wall']]

    def load_level(self):
        self.defenses.empty()
        self.menu = Menu(self)

    def run(self):
        self.running = True

        while self.running:
            delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.menu.visible:
                        self.place_defense(pygame.mouse.get_pos())
                    self.menu.clicked()

            self.menu.update()

            if not self.menu.visible:
                self.defenses.update(delta)

                self.wave.update(delta)
                if self.wave.done:
                    self.wave = Wave(self, self.wave.number + 1)

            self.window.clear()
            self.defenses.draw(self.window.screen)
            self.menu.draw(self.window.screen)

    def quit(self):
        self.running = False

    def select_defense(self, type):
        raise NotImplemented

    def place_defense(self, position):
        raise NotImplemented