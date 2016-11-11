from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu


class RestaurantMenu(AmuletMenu):

    def __init__(self, panel, business):
        super(self.__class__, self).__init__(panel)
        self.name = business.name
        self.rounded_aggregated_overall_rating = business.rounded_aggregated_overall_rating

    @draw_menu
    def show(self):
        console_print(self.panel, 0, 0, self.name)
        console_print(self.panel, 0, 1, 'a description')

    def select_option(self, num):
        return
