from internal.configurable import Configurable
from internal.enemy_wave import EnemyWave
from internal.route_searching import RouteSearching
from pygame.sprite import OrderedUpdates
from internal.collision import Collision


class Level:
    def __init__(self, game, name):
        self.route_find = ...
        self.configures = ...
        self.data = ...
        self.lives = ...
        self.money = ...
        self.time = ...

        self.game = game
        self.name = name
        self.load_data()
        self.start()

    def load_data(self):
        with open(f'levels/{self.name}.level', 'r') as file:
            self.data = [line.strip().split(" ") for line in file.readlines()
                         if len(line.strip()) > 0 and line[0] != '#']

    def start(self):
        self.collision = Collision(self, self.game.window.resolution, 32)
        self.configures = OrderedUpdates()
        self.route_find = RouteSearching(self.game, self.collision)

        for args in self.data:
            obj = Configurable(args[0], int(args[1]), int(args[2]))
            self.configures.add(obj)

            if hasattr(obj, "block"):
                self.collision.block_tile(int(args[1]), int(args[2]), obj.rect.width - 1, obj.rect.height - 1)

        self.route_find.setup(30)
        self.wave = EnemyWave(self.game, 1)
        self.lives = 20
        self.money = 600
        self.time = 0

    def get_sint(self):
        return int((self.time / 5) ** 1.4 + (self.game.wave.number - 1) ** 3)
