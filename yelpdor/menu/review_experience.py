from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu
from yelpdor.menu.message import MessageMenu


class ReviewExperienceMenu(AmuletMenu):

    def __init__(self, panel, business_name):
        super(self.__class__, self).__init__(panel)
        self.name = 'Review Experience'
        self.business_name = business_name

        self.facets = [
            'Cleanliness',
            'Service',
            'Food',
        ]
        self.reviewed = []

    @draw_menu
    def show(self):
        print_msg = super(ReviewExperienceMenu, self).make_msg_print_func()

        msg = 'Please rate the {facet} at {business}:'.format(
            facet=self.facets[-1],
            business=self.business_name
        )
        print_msg(0, msg)

    def select_option(self, num):
        if num >= 1 and num <= 5:
            self.reviewed.append((self.facets.pop(), num))
        else:
            return MessageMenu(self.panel, 'Please give a rating of 1-5 stars')

        if self.facets:
            return 'Still review...'
        else:
            return None
