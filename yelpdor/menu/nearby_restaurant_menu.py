from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu


class NearbyRestaurantMenu(AmuletMenu):

    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Nearby restaurants'
        self.restaurants = ['Working Girls', 'Gary Danko']

    @draw_menu
    def show(self):
        line_num = 0
        console_print(self.panel, 0, line_num,
                      'The following restaurants are nearby:')

        for num, name in enumerate(self.restaurants, start=1):
            line_num += 1
            console_print(self.panel, 0, line_num, '{}. {}'.format(num, name))

    @draw_menu
    def show_restaurant(self, name):
        console_print(self.panel, 0, 0, 'Info for the {}'.format(name))

    def select_option(self, num):
        if num >= len(self.restaurants):
            # Ignore invalid menu options
            return
        self.show_restaurant(self.restaurants[num])
