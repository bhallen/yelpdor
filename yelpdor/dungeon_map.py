import random

import lib.libtcodpy as libtcod
from tile import Tile
from tile import Rect


FOV_ALGO = 0  #default FOV algorithm
FOV_LIGHT_WALLS = True
VIEW_RADIUS = 20


class DungeonMap:
    width=128
    height=128
    __map__ = [] 
    rooms = []
    spawn = (0, 0)
    objects = []

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__map__ = [ [Tile(True) for y in range(height) ] for x in range(width) ]

    def __getitem__(self, key):
        return self.__map__[key]

    def within_map(self, x, y):
        return 0 <= x and x < self.width and 0 <= y and y < self.height

    def init_fov_map(self):
        self.fov_map = libtcod.map_new(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                libtcod.map_set_properties(
                    self.fov_map,
                    x,
                    y,
                    not self[x][y].block_sight,
                    not self[x][y].blocked
                )
        self.fov_x = None
        self.fov_y = None

    def recompute_fov(self, x, y):
        if x != self.fov_x or y != self.fov_y:
            libtcod.map_compute_fov(self.fov_map, x, y, VIEW_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
            self.fov_x = x
            self.fov_y = y


class Room:
    
    def __init__(self, rect, door=None):
        self.rect = rect
        self.door = door

    def contains(self, x, y):
        return self.rect.contains(x, y)
