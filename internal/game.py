import pygame

from internal.defense import Defense
from internal.level import Level
from internal.menu import Menu
from internal.wave import Wave


class Game:
    def __init__(self, window):
        self.running = None

        self.window = window
        self.clock = pygame.time.Clock()
        self.defenses = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.load_level('path')
        self.defense_type = 0
        self.defense_prototypes = [Defense(self, 'Defense' + name, -100, -100)
                                   for name in ['Pillbox', 'Wall', 'Mines', 'Artillery']]

    def load_level(self, name):
        self.defenses.empty()
        self.bullets.empty()
        self.explosions.empty()
        self.level = Level(self, name)
        self.wave = Wave(self, 1)
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
                        self.set_defense(pygame.mouse.get_pos())
                    self.menu.clicked()

            self.menu.update()
            self.level.route_find.update()

            if not self.menu.visible:
                self.level.time += delta
                self.defenses.update(delta)

            self.window.clear()
            self.level.configures.draw(self.window.screen)
            self.defenses.draw(self.window.screen)
            self.menu.draw(self.window.screen)

    def quit(self):
        self.running = False

    def choose_defense(self, type):
        self.defense_type = type

    def set_defense(self, position):
        if self.defense_type < 0:
            return

        defense = self.defense_prototypes[self.defense_type]

        self.defenses.add(Defense(
                self,
                defense.name,
                position[0] - position[0] % 32,
                position[1] - position[1] % 32,
            ),
        )
        self.level.money -= defense.cost
