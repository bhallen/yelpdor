from lib import libtcodpy as libtcod



class GameObj:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dmap, dx, dy):
        #move by the given amount, if the destination is not blocked
        if not dmap[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy
