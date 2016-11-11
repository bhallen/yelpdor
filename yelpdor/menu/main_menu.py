from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu
from yelpdor.menu.help_menu import HelpMenu
from yelpdor.menu.nearby_restaurant_menu import NearbyRestaurantMenu
from yelpdor.menu.stats_menu import StatsMenu


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
