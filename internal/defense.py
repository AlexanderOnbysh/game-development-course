from internal.configurable import Configurable


class Defense(Configurable):
    def __init__(self, game, name, x, y):
        super().__init__(name, x, y)

        self.attack_range = ...

        self.game = game
        self.fire_time = 0
        self.target = None

        if hasattr(self, 'images'):
            self.image = self.images[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        if hasattr(self, 'block'):
            self.game.level.collision.block_rect(x, y, self.rect.width, self.rect.height)

    def update(self, delta):
        raise NotImplemented

    def get_target(self):
        if self.target is not None and self.is_target_suitable(self.target):
            return self.target.rect.center

        return

    def is_target_suitable(self, target):
        if target not in self.game.wave.enemies:
            return False

        a, b = target.rect.center, self.rect.center
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 <= self.attack_range ** 2
