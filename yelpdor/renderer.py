from collections import namedtuple

import lib.libtcodpy as libtcod
from tile import TileType


color_dark_wall = libtcod.Color(0,0,100)
color_dark_ground = libtcod.Color(50,50,150)


Screen = namedtuple('Screen', ['width','height'])


TileDisp = namedtuple('TileDisp', ['char', 'bg', 'fg'])

TILE_DISPS = {
    TileType.floor: TileDisp(' ', libtcod.Color(200, 180, 50), None),
    TileType.wall: TileDisp(' ', libtcod.Color(130, 110, 50), None),
    TileType.street: TileDisp(' ', libtcod.Color(105, 105, 105), None),
    TileType.door: TileDisp('+', libtcod.Color(130, 110, 50), libtcod.Color(139, 69, 19)),
}


class Renderer:

    def __init__(self, console, screen, camera):
        self.console = console
        self.camera = camera
        self.screen = screen


    def render_tile(self, x, y, tile, in_fov):
        con = self.console
        tile_disp = TILE_DISPS[tile.tile_type]

        color_mult = 1.0 if in_fov else 0.5
        bg = tile_disp.bg * color_mult if tile_disp.bg else None
        fg = tile_disp.fg * color_mult if tile_disp.fg else None

        if tile_disp.char == ' ':
            libtcod.console_set_char_background(con, x, y, bg, libtcod.BKGND_SET)
            libtcod.console_set_char(self.console, x, y, ' ')
        else:
            libtcod.console_set_char_background(con, x, y, bg, libtcod.BKGND_SET)
            libtcod.console_set_default_foreground(self.console, fg)
            libtcod.console_put_char(
                self.console,
                x,
                y,
                tile_disp.char,
                libtcod.BKGND_NONE
            )


    def render(self, player, objects, dmap):
        camera = self.camera
        con = self.console
        screen = self.screen

        camera.move(player.x, player.y)
        dmap.recompute_fov(player.x, player.y)
        for x in range(camera.width):
            for y in range(camera.height):
                (map_x, map_y) = (camera.x + x, camera.y + y)

                tile = dmap[map_x][map_y]
                in_fov = libtcod.map_is_in_fov(dmap.fov_map, map_x, map_y)
                self.render_tile(x, y, tile, in_fov)

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
