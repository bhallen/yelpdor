from lib.libtcodpy import *
from collections import namedtuple
from yelpdor.amulet_menu import MainMenu

PANEL_WIDTH = 30
PANEL_HEIGHT = 15

MenuOption = namedtuple('MenuOption', ['name', 'function'])


class Amulet:
    '''Mobile app used to navigate and see stats'''
    
    AMULET_MODE, STATS_MODE = range(2)

    def __init__(self, player, x=0, y=0):
        self.player = player
        self.x = x
        self.y = y

        self.panel = console_new(PANEL_WIDTH, PANEL_HEIGHT)
        self.mode = Amulet.STATS_MODE
        self.main_menu = MainMenu(self.panel)



    def draw(self, con):
        if self.mode == Amulet.AMULET_MODE:
            console_blit(self.panel, 0, 0, 0, 0, con, self.x, self.y)
        elif self.mode == Amulet.STATS_MODE:
            self.draw_stats(con)

    def toggle_mode(self):
        if self.mode == Amulet.STATS_MODE:
            self.mode = Amulet.AMULET_MODE

            self.main_menu.show()
        elif self.mode == Amulet.AMULET_MODE:
            self.mode = Amulet.STATS_MODE
            console_set_default_background(self.panel,black)
            console_clear(self.panel)
        else:
            raise Exception('Unsupported mode')


    def draw_stats(self, con):
        console_print(con, self.x, self.y, 'Review count: {}'.format(self.player.review_count))
        console_print(con, self.x, self.y + 1, 'Reputation:   {}'.format(self.player.reputation))


    def keyboard_input(self, key):
        # TODO - This should really be two separate classes: amulet and stats
        assert self.mode == Amulet.AMULET_MODE

        if key >= KEY_0 and key <= KEY_9:
            num = key - KEY_0
        elif key >= KEY_KP0 and key <= KEY_KP9:
            num = key - KEY_KP0
        else:
            raise Exception('Amulet does not support this input value: {}'.format(key))


        self.main_menu.select_option(num)
