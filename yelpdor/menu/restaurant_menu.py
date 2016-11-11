from lib.libtcodpy import console_print
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu
from yelpdor.city import format_rating


class RestaurantMenu(AmuletMenu):

    def __init__(self, panel, business):
        super(self.__class__, self).__init__(panel)
        self.business = business

    @draw_menu
    def show(self):
        console_print(self.panel, 0, 0, self.business.name)
        console_print(self.panel, 0, 1, '')
        console_print(self.panel, 0, 2, 'Summary of reviews:')
        for i, facet in enumerate(self.business.ordered_facets):
            console_print(self.panel, 0, i+3, '> {}: {}'.format(
                facet, format_rating(self.business.rounded_aggregated_facet_ratings[facet])))
        console_print(self.panel, 0, 4, '')
        console_print(self.panel, 0, 5+len(self.business.ordered_facets), 'Press any digit key to go back.')

    def select_option(self, num):
        return
