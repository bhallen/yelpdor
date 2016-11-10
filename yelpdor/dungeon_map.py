import random

from tile import Tile


class DungeonMap:
    width=128
    height=128
    __map__ = [] 
    rooms = []
    spawn = (0, 0)

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__map__ = [ [Tile(True) for y in range(height) ] for x in range(width) ]

    def __getitem__(self, key):
        return self.__map__[key]

    def within_map(self, x, y):
        return 0 <= x and x < self.width and 0 <= y and y < self.height
