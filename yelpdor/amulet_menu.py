from lib.libtcodpy import *


def draw_menu(func):
    '''Decorator for menu drawing.

    Wraps the drawing of menus to clear and initialize the canvas.
    '''
    def decorator(self):
        console_set_default_background(self.panel,light_red)
        console_clear(self.panel)

        func(self)
    return decorator


class AmuletMenu(object):

    def __init__(self, panel):
        self.name = 'Name'
        self.panel = panel

    def show(self):
        '''Abstract method, subclass MUST implement'''
        assert False, 'This should not be called'

    def select_option(self, num):
        '''Abstract method, subclass MUST implement'''
        assert False, 'This should not be called'


class MainMenu(AmuletMenu):

    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Nearby restaurants'
        self.menu = [
            NearbyRestaurantMenu(self.panel),
            StatsMenu(self.panel),
            HelpMenu(self.panel),
        ]

    @draw_menu
    def show(self):
        line_num = 0
        console_print(self.panel, 0, line_num, 'Amulet of Yelpdor')

        for num, menu_option in enumerate(self.menu):
            line_num += 1
            msg = '{}. {}'.format(num, menu_option.name)
            console_print(self.panel, 0, line_num, msg)

    def select_option(self, num):
        if num >= len(self.menu):
            # Ignore invalid menu options
            return
        self.menu[num].show()


class NearbyRestaurantMenu(AmuletMenu):
    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Nearby restaurants'
        self.restaurants = ['Working Girls', 'Gary Danko']

    @draw_menu
    def show(self):
        line_num = 0
        console_print(self.panel, 0, line_num, 'The following restaurants are nearby:')

        for num, name in enumerate(self.restaurants, start=1):
            line_num += 1
            console_print(self.panel, 0, line_num, '{}. {}'.format(num, name))

    @draw_menu
    def show_restaurant(self, name):
        console_print(self.panel, 0, line_num, 'Info for the {}'.format(name))


    def select_option(self, num):
        if num >= len(self.restaurants):
            # Ignore invalid menu options
            return
        show_restaurant(self.restaurants[num])


class StatsMenu(AmuletMenu):
    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Stats'

    @draw_menu
    def show(self):
        console_print(self.panel, 0, 0, 'Detailed statistics')


class HelpMenu(AmuletMenu):
    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Show Help'

    @draw_menu
    def show(self):
        console_print(self.panel, 0, 0, 'This is the help menu')
