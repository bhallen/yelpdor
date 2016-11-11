from collections import namedtuple

from lib import libtcodpy as libtcod
from yelpdor.menu.main_menu import NearbyRestaurantMenu

PANEL_WIDTH = 31
PANEL_HEIGHT = 24

MenuOption = namedtuple('MenuOption', ['name', 'function'])


class Amulet(object):
    '''Mobile app used to navigate and see stats'''

    def __init__(self, player, x=0, y=0, district=None):
        self.x_pos = x
        self.y_pos = y

        self.panel = libtcod.console_new(PANEL_WIDTH, PANEL_HEIGHT)
        self.visible = True
        self.menu_stack = []
        self.menu_stack.append(NearbyRestaurantMenu(self.panel, player, district))

    def current_menu(self):
        return self.menu_stack[-1]

    def draw(self, con):
        self.current_menu().show()
        libtcod.console_blit(self.panel, 0, 0, 0, 0, con, self.x_pos, self.y_pos)

    def toggle(self):
        self.visible = not self.visible

    def keyboard_input(self, key):
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
