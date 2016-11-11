from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu


class RestaurantMenu(AmuletMenu):

    def __init__(self, panel, name, description):
        super(self.__class__, self).__init__(panel)
        self.name = name
        self.description = description

    @draw_menu
    def show(self):
        console_print(self.panel, 0, 0, self.name)
        console_print(self.panel, 0, 1, self.description)

    def select_option(self, num):
        return
