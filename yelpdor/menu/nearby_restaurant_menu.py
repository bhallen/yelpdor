from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu
from yelpdor.menu.restaurant_menu import RestaurantMenu


class NearbyRestaurantMenu(AmuletMenu):

    def __init__(self, panel):
        super(self.__class__, self).__init__(panel)
        self.name = 'Nearby restaurants'
        self.restaurants = [
            RestaurantMenu(
                panel,
                'Working Girls\'',
                'Please go to workinggirlscafe.com for more details.'
            ),
            RestaurantMenu(
                panel,
                'Gary Danko',
                'Please go to garydanko.com for more details.'
            ),
        ]

    @draw_menu
    def show(self):
        line_num = 0
        console_print(self.panel, 0, line_num,
                      'The following restaurants are nearby:')

        for num, restaurant in enumerate(self.restaurants, start=0):
            line_num += 1
            msg = '{}. {}'.format(num, restaurant.name)
            console_print(self.panel, 0, line_num, msg)

        line_num += 1
        exit_msg = '{}. {}'.format(len(self.restaurants), 'Exit')
        console_print(self.panel, 0, line_num, exit_msg)

    def select_option(self, num):
        if num >= len(self.restaurants):
            # Ignore invalid menu options
            return
        return self.restaurants[num]
