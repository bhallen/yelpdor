from collections import namedtuple

import lib.libtcodpy as libtcod


color_dark_wall = libtcod.Color(0,0,100)
color_dark_ground = libtcod.Color(50,50,150)


Screen = namedtuple('Screen', ['width','height'])


class Renderer:

    def __init__(self, console, screen, camera):
        self.console = console
        self.camera = camera
        self.screen = screen


    def render(self, player, objects, dmap):
        camera = self.camera
        con = self.console
        screen = self.screen

        camera.move(player.x, player.y)
        for x in range(camera.width):
            for y in range(camera.height):
                (map_x, map_y) = (camera.x + x, camera.y + y)

                wall = dmap[map_x][map_y].block_sight
                if wall:
                    libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET)

                for obj in objects:
                    if obj != player:
                        self.draw_obj(obj)
                self.draw_obj(player)

        libtcod.console_blit(con, 0, 0, screen.width, screen.height, 0, 0, 0)


    def clear(self, objects):
        for obj in objects:
            self.clear_obj(obj)


    def draw_obj(self, obj):
        #set the color and then draw the character that represents this object at its position
        (x, y) = self.camera.convert_coordinates(obj.x, obj.y)

        if x is not None:
            #set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(self.console, obj.color)
            libtcod.console_put_char(self.console, x, y, obj.char, libtcod.BKGND_NONE)


    def clear_obj(self, obj):
        (x, y) = self.camera.convert_coordinates(obj.x, obj.y)
        if x is not None:
            libtcod.console_put_char(self.console, x, y, ' ', libtcod.BKGND_NONE)
