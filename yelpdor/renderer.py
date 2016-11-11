# pylint: skip-file
from collections import namedtuple

from tile import TileType

import lib.libtcodpy as libtcod

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)


Screen = namedtuple('Screen', ['width', 'height'])


TileDisp = namedtuple('TileDisp', ['char', 'bg', 'fg'])

TILE_DISPS = {
    TileType.floor: TileDisp(' ', libtcod.Color(200, 180, 50), None),
    TileType.wall: TileDisp(' ', libtcod.Color(130, 110, 50), None),
    TileType.street: TileDisp(' ', libtcod.Color(105, 105, 105), None),
    TileType.door: TileDisp('+', libtcod.Color(139, 69, 19), libtcod.Color(255, 255, 255)),
    TileType.rock: TileDisp('O', libtcod.Color(105, 105, 105), libtcod.Color(0, 0, 0)),
}


class Renderer:

    def __init__(self, console, screen, camera):
        self.console = console
        self.camera = camera
        self.screen = screen

        # map_console is completely redrawn, but no need to fully recreate it each frame
        self.map_console = libtcod.console_new(camera.width, camera.height)

    def draw_tile(self, x, y, tile, in_fov):
        con = self.map_console
        tile_disp = TILE_DISPS[tile.tile_type]

        if in_fov:
            tile.explored = True

        color_mult = 1.0 if in_fov else 0.5
        bg = tile_disp.bg * color_mult if tile_disp.bg else None
        fg = tile_disp.fg * color_mult if tile_disp.fg else None

        if tile.explored:
            if tile_disp.char == ' ':
                libtcod.console_set_char_background(con, x, y, bg, libtcod.BKGND_SET)
                libtcod.console_set_char(con, x, y, ' ')
            else:
                libtcod.console_set_char_background(con, x, y, bg, libtcod.BKGND_SET)
                libtcod.console_set_default_foreground(con, fg)
                libtcod.console_put_char(
                    con,
                    x,
                    y,
                    tile_disp.char,
                    libtcod.BKGND_NONE
                )
        else:
            libtcod.console_set_char_background(con, x, y, libtcod.black, libtcod.BKGND_SET)
            libtcod.console_set_char(con, x, y, ' ')

    def draw_obj(self, con, x, y, obj):
        # set the color and then draw the character that represents this object at its position

        if x is not None:
            # set the color and then draw the character that represents this object at its position
            libtcod.console_set_default_foreground(con, obj.color)
            libtcod.console_put_char(con, x, y, obj.char, libtcod.BKGND_NONE)

    def render_map(self, player, dmap):
        camera = self.camera
        con = self.map_console

        # Clear screen before redraw
        libtcod.console_clear(con)

        camera.move(player.x, player.y)
        dmap.recompute_fov(player.x, player.y)
        for x in range(camera.width):
            for y in range(camera.height):
                (map_x, map_y) = (camera.x + x, camera.y + y)

                tile = dmap[map_x][map_y]
                in_fov = libtcod.map_is_in_fov(dmap.fov_map, map_x, map_y)
                self.draw_tile(x, y, tile, in_fov)

        for obj in dmap.objects:
            if obj != player:
                if libtcod.map_is_in_fov(dmap.fov_map, obj.x, obj.y):
                    (x, y) = camera.convert_coordinates(obj.x, obj.y)
                    self.draw_obj(con, x, y, obj)
        (x, y) = camera.convert_coordinates(player.x, player.y)
        self.draw_obj(con, x, y, player)

        return con

    def render(self, player, dmap, amulet, stats):
        camera = self.camera
        con = self.console
        screen = self.screen

        map_console = self.render_map(player, dmap)
        libtcod.console_blit(map_console, 0, 0, camera.width, camera.height, con, 1, 1)

        if amulet.visible:
            # Draw amulet overlay
            amulet.draw(con)
        else:
            stats.draw(con)

        libtcod.console_blit(con, 0, 0, screen.width, screen.height, 0, 0, 0)
