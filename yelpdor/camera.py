import lib.libtcodpy as libtcod


class Camera:
    width = 0
    height = 0
    x = 0
    y = 0
    dmap = None  

    def __init__(self, width, height, dungeon_map):
        self.width = width
        self.height = height
        self.x = width / 2
        self.y = width / 2
        self.dmap = dungeon_map


    def convert_coordinates(self, x, y):
        (x, y) = (x - self.x, y - self.y)
 
        if (x < 0 or y < 0 or x >= self.width or y >= self.height):
            return (None, None)
 
        return (x, y)

    def move(self, tx, ty):
        nx = tx - self.width / 2
        ny = ty - self.height / 2

        # camera boundaries
        if nx < 0:
            nx = 0
        if ny < 0:
            ny = 0
        if nx > self.dmap.width - self.width:
            nx = self.dmap.width - self.width
        if ny > self.dmap.height - self.height:
            ny = self.dmap.height - self.height
 
        if nx != self.x or ny != self.y: fov_recompute = True

        self.x = nx 
        self.y = ny
