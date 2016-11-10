import libtcodpy as libtcod

from tile import Tile
from tile import Rect


class DungeonMap:
    MAP_WIDTH=128
    MAP_HEIGHT=128
    __map__ = [] 
    rooms = []

    def __init__(self, width, height):
        self.MAP_WIDTH = width
        self.MAP_HEIGHT = height

        self.__map__ = [ [Tile(True) for y in range(height) ] for x in range(width) ]
 

    def __getitem__(self, key):
        return self.__map__[key]
