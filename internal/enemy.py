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
