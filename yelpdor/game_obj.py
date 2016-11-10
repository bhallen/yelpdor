import libtcodpy as libtcod

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


    def draw(self, con, camera):
        #set the color and then draw the character that represents this object at its position
        (x, y) = camera.convert_coordinates(self.x, self.y)

        if x is not None:
            #set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, x, y, self.char, libtcod.BKGND_NONE)


    def clear(self, con, camera):
        (x, y) = camera.convert_coordinates(self.x, self.y)
        if x is not None:
            libtcod.console_put_char(con, x, y, ' ', libtcod.BKGND_NONE)
