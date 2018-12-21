import random

import math

from internal.configurable import Configurable


class Enemy(Configurable):
    def __init__(self, game, name, x, y):
        super().__init__(name, x, y)

        self.game = game
        self.path = game.level.pathfinding.get_path()
        self.target = self.path.start
        self.rect.topleft = self.target
        self.x = self.target[0]
        self.y = self.target[1]
        self.speed += random.randint(-25, 25)

        self.speed += random.randint(0, self.game.wave.number * 2)
        self.health = self.health ** (1 + (self.game.wave.number / 35))

    def update(self, delta):
        self.update_position(delta)

    def update_position(self, delta):
        current = self.rect.topleft
        target = self.target

        dx = target[0] - current[0]
        dy = target[1] - current[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        max = delta * self.speed

        if distance < max:
            self.x = target[0]
            self.y = target[1]
            self.reached_target()
        else:
            proportion = max / distance
            self.x += dx * proportion
            self.y += dy * proportion

        self.rect.x = self.x
        self.rect.y = self.y

    def reached_target(self):
        if not self.path.done:

            if self.target[0] < self.game.window.resolution[0] and self.path.points is not None and self.target in self.path.points:
                self.path, self.target = self.game.level.pathfinding.get_partial_path(self.target)

            return

        self.target = self.path.next(self.target)
        if not self.target:
            self.game.level.lives -= 1
            if (self.game.level.lives == 0):
                self.game.menu.show_lose_screen()

            self.kill()

    def take_damage(self, damage):
        self.health -= damage

        if self.health <= 0:
            self.kill()

    def kill(self):
        super().kill()

        self.game.wave.enemy_killed()

        if self.rect.x > 1:
            self.game.level.money += self.money
