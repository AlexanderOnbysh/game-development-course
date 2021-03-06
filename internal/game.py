import pygame

from internal.defense import Defense
from internal.level import Level
from internal.menu import Menu
from internal.enemy_wave import EnemyWave


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
                                   for name in ['Turret', 'Barrier', 'Defender']]

    def load_level(self, name):
        self.defenses.empty()
        self.bullets.empty()
        self.explosions.empty()
        self.level = Level(self, name)
        self.wave = EnemyWave(self, 1)
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
                self.bullets.update(delta)
                self.explosions.update(delta)
                self.wave.update(delta)
                if self.wave.done:
                    self.wave = EnemyWave(self, self.wave.number + 1)

            self.window.clear()
            self.level.configures.draw(self.window.screen)
            self.defenses.draw(self.window.screen)
            self.bullets.draw(self.window.screen)
            self.wave.enemies.draw(self.window.screen)
            self.explosions.draw(self.window.screen)
            self.menu.draw(self.window.screen)

    def quit(self):
        self.running = False

    def choose_defense(self, type):
        self.defense_type = type

    def set_defense(self, position):
        if self.defense_type < 0:
            return

        defense = self.defense_prototypes[self.defense_type]

        if self.level.money < defense.cost:
            return

        x = position[0] - position[0] % 32
        y = position[1] - position[1] % 32

        if self.level.collision.is_tile_blocked(x, y, defense.rect.width - 2, defense.rect.height - 2):
            return

        if hasattr(defense, 'block') and self.level.route_find.is_critical((x, y)):
            return

        self.defenses.add(Defense(
                self,
                defense.name,
                position[0] - position[0] % 32,
                position[1] - position[1] % 32,
            ),
        )
        self.level.money -= defense.cost
