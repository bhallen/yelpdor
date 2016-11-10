from lib import libtcodpy as libtcod

from yelpdor.camera import Camera
from yelpdor.city_map_generator import generate_city_map
from yelpdor.game_obj import GameObj
from yelpdor.renderer import Renderer
from yelpdor.renderer import Screen 
from yelpdor.simple_dungeon import make_map

#size of the map
MAP_HEIGHT = 256
MAP_WIDTH = 256 
 
#actual size of the window
SCREEN_HEIGHT = 64 
SCREEN_WIDTH = 64

CAMERA_HEIGHT = 64 
CAMERA_WIDTH = 64
 
LIMIT_FPS = 20  #20 frames-per-second maximum
 
 
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
        player.move(dungeon_map, 0, -1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(dungeon_map, 0, 1)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(dungeon_map, -1, 0)
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(dungeon_map, 1, 0)
 
 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('res/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
console = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
 
player = GameObj(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
 
dungeon_objects = [player]

dungeon_map = generate_city_map(MAP_WIDTH, MAP_HEIGHT)
player.x, player.y = dungeon_map.spawn
screen = Screen(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT, dungeon_map) 
renderer = Renderer(console, screen, camera)
 
while not libtcod.console_is_window_closed():
    renderer.render(player, dungeon_objects, dungeon_map)
    libtcod.console_flush()
    renderer.clear(dungeon_objects) 
    exit = handle_keys()
    if exit:
        break
