from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu


class MessageMenu(AmuletMenu):

    def __init__(self, panel, message):
        super(self.__class__, self).__init__(panel)
        self.message = message

    @draw_menu
    def show(self):
        print_msg = super(self.__class__, self).make_msg_print_func()
        print_msg(0, self.message)

    def select_option(self, num):
        # Any keypress will exit the menu
        return None
