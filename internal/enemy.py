from internal.configurable import Configurable
import math
import random


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

