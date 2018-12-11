from internal.configurable import Configurable
from internal.route_searching import RouteSearching
from pygame.sprite import OrderedUpdates


class Level:
    def __init__(self, game, name):
        self.route_find = ...
        self.configures = ...
        self.collision = ...
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
        # TODO: initialize collision
        self.configures = OrderedUpdates()
        self.route_find = RouteSearching(self.game, self.collision)

        for args in self.data:
            self.configures.add(Configurable(args[0], int(args[1]), int(args[2])))

        self.route_find.setup(30)
        self.lives = 20
        self.money = 600
        self.time = 0

    def get_sint(self):
        # TODO: implement
        return 0
