from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu


class HelpMenu(AmuletMenu):

    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Show Help'

    @draw_menu
    def show(self):
        console_print(self.panel, 0, 0, 'This is the help menu')

    def select_option(self, num):
        pass
