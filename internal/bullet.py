import math
import random
import pygame
from internal.configurable import Configurable


class Bullet(Configurable):
    def __init__(self, game, origin, target):
        super().__init__("AttackBullet", origin[0], origin[1])
        self.game = game

        dx = target[0] - origin[0]
        dy = target[1] - origin[1]

        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        self.xSpeed = (dx / magnitude) * self.speed * random.randint(200, 500)
        self.ySpeed = (dy / magnitude) * self.speed * random.randint(200, 500)
        self.life = magnitude / math.sqrt(self.xSpeed ** 2 + self.ySpeed ** 2)
        self.current_life = 0

        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = origin
