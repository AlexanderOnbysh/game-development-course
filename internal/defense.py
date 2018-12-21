import math

from internal.configurable import Configurable


class Defense(Configurable):
    def __init__(self, game, name, x, y):
        super().__init__(name, x, y)

        self.game = game
        self.fire_time = 0
        self.target = None

        if hasattr(self, 'images'):
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def update(self, delta):
        if self.attack == 'none':
            return

        target = self.get_target()

        self.fire_time += delta
        while self.fire_time >= self.attack_rate:
            self.fire_time -= self.attack_rate

            if target is not None and target != self.rect.center:
                if hasattr(self, 'flash_offset'):
                    self.game.explosions.add(DefenseLight(self.rect.center, target, self.flash_offset))

                if self.attack_rate <= 0:
                    self.kill()

            if self.attack_rate <= 0:
                break

        if self.rotate:
            center = self.rect.center

            if self.target is None:
                self.image = self.images[0]
            else:
                dx = self.target.rect.center[0] - center[0]
                dy = self.target.rect.center[1] - center[1]
                angle = math.degrees(math.atan2(-dy, dx))
                if angle < 0:
                    angle += 360

                self.image = self.images[int(angle // 5)]

            self.rect = self.image.get_rect()
            self.rect.center = center

    def get_target(self):
        if self.target is not None and self.is_target_suitable(self.target):
            return self.target.rect.center

        for t in self.game.wave.enemies:
            if self.is_target_suitable(t):
                self.target = t
                return t.rect.center

        return None

    def is_target_suitable(self, target):
        if target not in self.game.wave.enemies:
            return False

        a, b = target.rect.center, self.rect.center
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 <= self.attack_range ** 2


class DefenseLight(Configurable):
    def __init__(self, defense_position, target, offset):
        dx = target[0] - defense_position[0]
        dy = target[1] - defense_position[1]
        magnitude = math.sqrt(dx * dx + dy * dy)
        dx *= (offset / magnitude)
        dy *= (offset / magnitude)

        super().__init__('DefenseLight', defense_position[0] + dx - 16, defense_position[1] + dy - 16)

    def update(self, delta):
        super().update_animation(delta)
