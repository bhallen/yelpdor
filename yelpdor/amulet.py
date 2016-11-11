from lib.libtcodpy import *
from collections import namedtuple

PANEL_WIDTH = 30
PANEL_HEIGHT = 15

MenuOption = namedtuple('MenuOption', ['name', 'function'])


def draw_menu(func):
    '''Decorator for menu drawing.

    Wraps the drawing of menus to clear and initialize the canvas.
    '''
    def decorator(self):
        console_set_default_background(self.panel,light_red)
        console_clear(self.panel)

        func(self)
    return decorator


class Amulet:
    '''Mobile app used to navigate and see stats'''
    
    AMULET_MODE, STATS_MODE = range(2)

    def __init__(self, player, x=0, y=0):
        self.player = player
        self.x = x
        self.y = y

        self.panel = console_new(PANEL_WIDTH, PANEL_HEIGHT)
        self.mode = Amulet.STATS_MODE
        self.menu = [
            MenuOption('Nearby restaurants', self.show_restaurant),
            MenuOption('Stats', self.show_stats),
            MenuOption('Show Help', self.show_help),
        ]



    def draw(self, con):
        if self.mode == Amulet.AMULET_MODE:
            console_blit(self.panel, 0, 0, 0, 0, con, self.x, self.y)
        elif self.mode == Amulet.STATS_MODE:
            self.draw_stats(con)

    def toggle_mode(self):
        if self.mode == Amulet.STATS_MODE:
            self.mode = Amulet.AMULET_MODE

            self.main_menu()
        elif self.mode == Amulet.AMULET_MODE:
            self.mode = Amulet.STATS_MODE
            console_set_default_background(self.panel,black)
            console_clear(self.panel)
        else:
            raise Exception('Unsupported mode')


    @draw_menu
    def main_menu(self):
        line_num = 0
        console_print(self.panel, 0, line_num, 'Amulet of Yelpdor')

        for num, menu_option in enumerate(self.menu):
            line_num += 1
            msg = '{}. {}'.format(num, menu_option.name)
            console_print(self.panel, 0, line_num, msg)

    @draw_menu
    def show_help(self):
        console_print(self.panel, 0, 0, 'This is the help menu')

    @draw_menu
    def show_restaurant(self):
        line_num = 0
        console_print(self.panel, 0, line_num, 'The following restaurants are nearby:')
        restaurants = ['Working Girls', 'Gary Danko']

        for num, name in enumerate(restaurants, start=1):
            line_num += 1
            console_print(self.panel, 0, line_num, '{}. {}'.format(num, name))

    @draw_menu
    def show_stats(self):
        console_print(self.panel, 0, 0, 'Detailed statistics')

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

        if num >= len(self.menu):
            # Ignore invalid menu options
            return

        self.menu[num].function()
