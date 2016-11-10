from tile import Tile


class DungeonMap:
    width=128
    height=128
    __map__ = [] 
    rooms = []

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__map__ = [ [Tile(True) for y in range(height) ] for x in range(width) ]
 

    def __getitem__(self, key):
        return self.__map__[key]
