import libtcodpy as libtcod


class Camera:
    width = 0
    height = 0
    x = 0
    y = 0
    dmap = None  

    def __init__(self, width, height, dungeon_map):
        self.width = width
        self.height = height
        self.dmap = dungeon_map


    def move(self, tx, ty):
        nx = tx - self.width / 2
        ny = ty - self.height / 2

        # camera boundaries
        if nx < 0:
            nx = 0
        if ny < 0:
            ny = 0
        if nx > self.dmap.width - self.width - 1:
            nx = self.dmap.width - self.width - 1
        if ny > self.dmap.height - self.height- 1:
            ny = self.dmap.height - self.height - 1
 
        #if x != camera_x or y != camera_y: fov_recompute = True

        self.x = nx 
        self.y = ny
