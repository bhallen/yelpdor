from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu
from yelpdor.menu.restaurant_menu import RestaurantMenu
from yelpdor.city import format_rating


class NearbyRestaurantMenu(AmuletMenu):

    def __init__(self, panel, player, district):
        super(self.__class__, self).__init__(panel)
        self.name = 'Nearby restaurants'
        self.panel = panel
        self.player = player
        self.district = district
        self.sorted_restaurants = []
        self.restaurant_menus = []

    @draw_menu
    def show(self):
        self.sorted_restaurants = self.district.sorted_by_distance(self.player)
        self.restaurant_menus = [RestaurantMenu(self.panel, r) for r in self.sorted_restaurants]
        line_num = 0
        console_print(self.panel, 0, line_num,
                      'The following restaurants are nearby:')

        for num, restaurant in enumerate(self.restaurant_menus, start=0):
            line_num += 1
            msg = '{}. {} {}'.format(num, restaurant.name, format_rating(restaurant.rounded_aggregated_overall_rating))
            console_print(self.panel, 0, line_num, msg)

        line_num += 1
        exit_msg = '{}. {}'.format(len(self.restaurant_menus), 'Exit')
        console_print(self.panel, 0, line_num, exit_msg)

    def select_option(self, num):
        if num >= len(self.restaurant_menus):
            # Ignore invalid menu options
            return
        return self.restaurant_menus[num]
