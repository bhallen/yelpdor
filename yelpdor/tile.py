class Rect:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
 
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)
 
    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 < other.x2 and self.x2 > other.x1 and
                self.y1 < other.y2 and self.y2 > other.y1)

    def contains(self, x, y):
        # returns true if this rectangle contains the given point
        return (self.x1 <= x and x < self.x2 and
                self.y1 <= y and y < self.y2)

    @property
    def w(self):
        return self.x2 - self.x1
    
    @property
    def h(self):
        return self.y2 - self.y1


class TileType:
    floor = 1
    wall = 2
    street = 3
    door = 4
    

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None, tile_type=TileType.floor):
        self.blocked = blocked

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

        self.tile_type = tile_type

# creates a tile based on the type
def create_tile(tile_type):
    blocked = False
    block_sight = None

    if tile_type == TileType.wall:
        blocked = True
    elif tile_type == TileType.door:
        block_sight = True

    return Tile(blocked, block_sight, tile_type)
