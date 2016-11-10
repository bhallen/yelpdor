import libtcodpy as libtcod

from yelpdor.tile import Tile
from yelpdor.game_obj import GameObj
from yelpdor.simple_dungeon import make_map



#size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 45
 
#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
 
LIMIT_FPS = 20  #20 frames-per-second maximum
 
 
color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)
 
 
def render_all():
    global color_light_wall
    global color_light_ground
 
    #go through all tiles, and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = dmap[x][y].block_sight
            if wall:
                libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
            else:
                libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
 
    #draw all objects in the list
    for go in objects:
        go.draw(con)
 
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
dmap = make_map(player, MAP_HEIGHT, MAP_WIDTH)
 
 
while not libtcod.console_is_window_closed():
 
    #render the screen
    render_all()
 
    libtcod.console_flush()
 
    #erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear(con)
 
    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
