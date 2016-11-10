import libtcodpy as libtcod

from yelpdor.tile import Tile
from yelpdor.game_obj import GameObj
from yelpdor.simple_dungeon import make_map
from yelpdor.renderer import Camera


#size of the map
MAP_HEIGHT = 128
MAP_WIDTH = 128 
 
#actual size of the window
SCREEN_HEIGHT = 64 
SCREEN_WIDTH = 64

CAMERA_HEIGHT = 64 
CAMERA_WIDTH = 64
 
LIMIT_FPS = 20  #20 frames-per-second maximum
 
color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)
 
 
def render_all(camera, player):
    #go through all tiles, and set their background color

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
                    obj.draw(con)
            player.draw(con)

 

    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
 
def handle_keys():
    #key = libtcod.console_check_for_keypress()  #real-time
    key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(dmap, 0, -1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(dmap, 0, 1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(dmap, -1, 0)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(dmap, 1, 0)
 
 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('res/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
 
#create object representing the player
player = GameObj(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
 
#create an NPC
npc = GameObj(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, '@', libtcod.yellow)
 
#the list of objects with those two
objects = [npc, player]
 
#generate map (at this point it's not drawn to the screen)
dmap = make_map(player, MAP_WIDTH, MAP_HEIGHT)

camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT, dmap) 
 
while not libtcod.console_is_window_closed():
 
    #render the screen
    render_all(camera, player)
 
    libtcod.console_flush()
 
    #erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear(con)
 
    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
