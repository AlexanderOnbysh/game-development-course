
class Collision:
    def __init__(self, level, resolution, tile_size):
        self.level = level
        self.tile_size = tile_size
        self.width = resolution[0] // tile_size
        self.height = resolution[1] // tile_size
        self.blocked_tiles = []
        self.overlay = None

    def point_to_index(self, x, y):
        x_index = x // self.tile_size
        y_index = y // self.tile_size
        return (y_index * 1000) + x_index

    def point_blocked(self, x, y):
        return self.point_to_index(x, y) in self.blocked_tiles

    def block_point(self, x, y):
        index = self.point_to_index(x, y)

        if index not in self.blocked_tiles:
            self.blocked_tiles.append(index)
            self.overlay = None
            self.level.route_find.repair((x - (x % self.tile_size), y - (y % self.tile_size)))

    def unblock_point(self, x, y):
        index = self.point_to_index(x, y)
        if index in self.blocked_tiles:
            self.blocked_tiles.remove(index)
            self.overlay = None

    def rect_blocked(self, x, y, width, height):
        x_offset = x % self.tile_size
        y_offset = y % self.tile_size
        for x_position in range(x - x_offset, x + width, self.tile_size):
            for y_position in range(y - y_offset, y + height, self.tile_size):
                if self.point_blocked(x_position, y_position):
                    return True
        return False

    def block_rect(self, x, y, width, height):
        x_offset = x % self.tile_size
        y_offset = y % self.tile_size
        for x_position in range(x - x_offset, x + width - 2, self.tile_size):
            for y_position in range(y - y_offset, y + height - 2, self.tile_size):
                self.block_point(x_position, y_position)

    def unblock_rect(self, x, y, width, height):
        x_offset = x % self.tile_size
        y_offset = y % self.tile_size
        for x_position in range(x - x_offset, x + width, self.tile_size):
            for y_position in range(y - y_offset, y + height, self.tile_size):
                self.unblock_point(x_position, y_position)
