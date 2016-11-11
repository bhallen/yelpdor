from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu


class StatsMenu(AmuletMenu):

    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Stats'

    @draw_menu
    def show(self):
        console_print(self.panel, 0, 0, 'Detailed statistics')

    def select_option(self, num):
        pass
