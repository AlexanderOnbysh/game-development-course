import pygame

from internal.enemy import Enemy


class EnemyWave:
    def __init__(self, game, number):
        self.game = game
        self.number = number
        self.started = False
        self.done = False
        self.enemies = pygame.sprite.Group()
        
        self.spawn_time = 0
        self.spawn_gap = 3 - (number ** 0.6)
        self.types = ('EnemySmall', 'EnemyMedium', 'EnemyLarge')
        self.proportions = [
            int(number ** 2.5),
            int(number ** 2 - number),
            int(number ** 1.7 - 4)
        ]

    def update(self, delta):
        self.enemies.update(delta)

        self.spawn_time -= delta
        if self.spawn_time > 0:
            return

        for i, (type, quantity) in enumerate(zip(self.types, self.proportions)):
            if self.started and quantity > 0:
                self.spawn(type)
                self.proportions[i] -= 1
        if not self.started:
            self.started = True
        self.spawn_time = self.spawn_gap

    def spawn(self, enemy_type):
        enemy = Enemy(self.game, enemy_type, 0, 0)
        self.enemies.add(enemy)

    def is_killed(self):
        if len(self.enemies) == 0 and sum(self.proportions) <= 0:
            self.done = True
