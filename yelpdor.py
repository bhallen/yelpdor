import libtcodpy as libtcod
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
libtcod.console_set_default_foreground(0, libtcod.white)
libtcod.console_put_char(0, 1, 1, '@', libtcod.BKGND_NONE)
libtcod.console_flush()


while not libtcod.console_is_window_closed():
  key = libtcod.console_wait_for_keypress(True)

