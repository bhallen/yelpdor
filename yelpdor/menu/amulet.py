from collections import namedtuple

from lib import libtcodpy as libtcod
from lib.libtcodpy import console_print
from yelpdor.menu.main_menu import MainMenu

PANEL_WIDTH = 30
PANEL_HEIGHT = 15

MenuOption = namedtuple('MenuOption', ['name', 'function'])


class Amulet(object):
    '''Mobile app used to navigate and see stats'''

    AMULET_MODE, STATS_MODE = range(2)

    def __init__(self, player, x=0, y=0):
        self.player = player
        self.x_pos = x
        self.y_pos = y

        self.panel = libtcod.console_new(PANEL_WIDTH, PANEL_HEIGHT)
        self.mode = Amulet.STATS_MODE
        self.menu_stack = []
        self.menu_stack.append(MainMenu(self.panel))

    def current_menu(self):
        return self.menu_stack[-1]

    def draw(self, con):
        if self.mode == Amulet.AMULET_MODE:
            libtcod.console_blit(self.panel, 0, 0, 0, 0,
                                 con, self.x_pos, self.y_pos)
        elif self.mode == Amulet.STATS_MODE:
            self.draw_stats(con)

    def toggle_mode(self):
        if self.mode == Amulet.STATS_MODE:
            self.mode = Amulet.AMULET_MODE

            self.current_menu().show()
        elif self.mode == Amulet.AMULET_MODE:
            self.mode = Amulet.STATS_MODE
            libtcod.console_set_default_background(self.panel, libtcod.black)
            libtcod.console_clear(self.panel)
        else:
            raise Exception('Unsupported mode')

    def draw_stats(self, con):
        console_print(con, self.x_pos, self.y_pos, 'Health: {}%%'.format(
            self.player.health))
        console_print(con, self.x_pos, self.y_pos + 1, 'Hunger: {}%%'.format(
            self.player.hunger))

        console_print(con, self.x_pos, self.y_pos + 3, 'Money: ${}'.format(
            self.player.dollars))

        console_print(con, self.x_pos, self.y_pos + 5, 'Review count: {}'.format(
            self.player.review_count))
        console_print(con, self.x_pos, self.y_pos + 6, 'Fame level: {}'.format(
            self.player.fame_level))

    def keyboard_input(self, key):
        # TODO - This should really be two separate classes: amulet and stats
        assert self.mode == Amulet.AMULET_MODE

        if key >= libtcod.KEY_0 and key <= libtcod.KEY_9:
            num = key - libtcod.KEY_0
        elif key >= libtcod.KEY_KP0 and key <= libtcod.KEY_KP9:
            num = key - libtcod.KEY_KP0
        else:
            raise Exception(
                'Amulet does not support this input value: {}'.format(key))

        self.select_option(num)

    def select_option(self, num):
        menu = self.current_menu().select_option(num)
        if menu:
            self.menu_stack.append(menu)
        else:
            self.menu_stack.pop()

        self.current_menu().show()
