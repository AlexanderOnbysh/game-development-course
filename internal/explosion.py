from internal.configurable import Configurable


class Explosion(Configurable):
    def __init__(self, game, position, radius, damage):
        super().__init__("AttackExplosion", position[0], position[1])
        self.rect.center = position

        max_magnitude = radius ** 2
        for enemy in game.wave.enemies:
            dx = enemy.rect.centerx - self.rect.centerx
            dy = enemy.rect.centery - self.rect.centery
            magnitude = (dx ** 2) + (dy ** 2)

            if magnitude < max_magnitude:
                enemy.take_damage(damage * (1 - (magnitude / max_magnitude)))

    def update(self, delta):
        super().update_animation(delta)
