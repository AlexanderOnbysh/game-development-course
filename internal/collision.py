
class Collision:
    def __init__(self, level, resolution, tile_size):
        self.level = level
        self.tile_size = tile_size
        self.width = resolution[0] // tile_size
        self.height = resolution[1] // tile_size
        self.blocked_tiles = []
        self.overlay = None

    def point_to_index(self, x, y):
        xIndex = x // self.tile_size
        yIndex = y // self.tile_size

        return (yIndex * 1000) + xIndex

    def point_blocked(self, x, y):
        return self.point_to_index(x, y) in self.blocked_tiles

    def block_point(self, x, y):
        index = self.point_to_index(x, y)

        if index not in self.blocked_tiles:
            self.blocked_tiles.append(index)
            self.overlay = None
            self.level.pathfinding.repair((x - (x % self.tile_size), y - (y % self.tile_size)))

    def unblock_point(self, x, y):
        index = self.point_to_index(x, y)

        if index in self.blocked_tiles:
            self.blocked_tiles.remove(index)
            self.overlay = None

    def rect_blocked(self, x, y, width, height):
        xOffset = x % self.tile_size
        yOffset = y % self.tile_size

        for xPos in range(x - xOffset, x + width, self.tile_size):
            for yPos in range(y - yOffset, y + height, self.tile_size):
                
                if self.point_blocked(xPos, yPos):
                    return True

        return False

    def block_rect(self, x, y, width, height):
        xOffset = x % self.tile_size
        yOffset = y % self.tile_size

        for xPos in range(x - xOffset, x + width - 2, self.tile_size):
            for yPos in range(y - yOffset, y + height - 2, self.tile_size):
                self.block_point(xPos, yPos)

    def unblock_rect(self, x, y, width, height):
        xOffset = x % self.tile_size
        yOffset = y % self.tile_size

        for xPos in range(x - xOffset, x + width, self.tile_size):
            for yPos in range(y - yOffset, y + height, self.tile_size):
                
                self.unblock_point(xPos, yPos)
