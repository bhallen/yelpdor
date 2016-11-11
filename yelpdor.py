import random

from lib import libtcodpy as libtcod
from yelpdor.camera import Camera
from yelpdor.city import District
from yelpdor.city_map_generator import generate_city_map
from yelpdor.gui.messenger import Messenger
from yelpdor.menu.amulet import Amulet
from yelpdor.player import Player
from yelpdor.renderer import Renderer
from yelpdor.renderer import Screen


MAP_WIDTH = 256
MAP_HEIGHT = 256

SCREEN_HEIGHT = 64
SCREEN_WIDTH = 80

CAMERA_HEIGHT = 60
CAMERA_WIDTH = 48

MESSENGER_WIDTH = SCREEN_WIDTH
MESSENGER_HEIGHT = 16


LIMIT_FPS = 20  # 20 frames-per-second maximum


def handle_keys():
    # key = libtcod.console_check_for_keypress()  #real-time
    key = libtcod.console_wait_for_keypress(True)  # turn-based

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True  # exit game

    elif key.c == ord('y') or key.c == ord('Y'):
        # Show/hide amulet
        amulet.toggle_mode()

    elif (amulet.mode == amulet.AMULET_MODE
          and key.vk >= libtcod.KEY_0
          and key.vk <= libtcod.KEY_KP9):
        # If amulet is displayed, redirect numeric input to amulet
        amulet.keyboard_input(key.vk)

    # movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(dungeon_map, 0, -1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(dungeon_map, 0, 1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(dungeon_map, -1, 0)

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(dungeon_map, 1, 0)

    # TEMPORARY: press r to review a business
    elif key.c == ord('r'):
        biz = random.choice(district.businesses)
        biz.visit(player)

    # check position for events
    player_business = district.find_business_containing_player(player)
    if player_business and player.current_business != player_business:
        player.current_business = player_business
        Messenger().message('You are inside the business {}.'.format(player_business.name))


#############################################
# Initialization & Main Loop
#############################################

libtcod.console_set_custom_font(
    'res/arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                          'Amulet of Yelpdor', False)
libtcod.sys_set_fps(LIMIT_FPS)
console = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)


district = District()
dungeon_map = generate_city_map(MAP_WIDTH, MAP_HEIGHT, district)
dungeon_map.init_fov_map()
screen = Screen(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
camera = Camera(CAMERA_WIDTH, CAMERA_HEIGHT, dungeon_map)
renderer = Renderer(console, screen, camera)
messenger = Messenger(
    width=MESSENGER_WIDTH,
    height=MESSENGER_HEIGHT,
    screen=screen)

player = Player(dungeon_map.spawn[0], dungeon_map.spawn[1], '@', libtcod.white)
dungeon_map.objects.append(player)
amulet = Amulet(player, 3, 3)

while not libtcod.console_is_window_closed():
    renderer.render(player, dungeon_map, amulet)
    messenger.render()
    libtcod.console_flush()
    if handle_keys():
        break
