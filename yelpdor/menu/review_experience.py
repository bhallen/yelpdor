import yelpdor.city
from yelpdor.menu.amulet_menu import AmuletMenu
from yelpdor.menu.amulet_menu import draw_menu
from yelpdor.menu.message import MessageMenu


class ReviewExperienceMenu(AmuletMenu):

    def __init__(self, panel, business_name, review_callback):
        super(self.__class__, self).__init__(panel)
        self.name = 'Review Experience'
        self.business_name = business_name
        self.review_callback = review_callback
        self.blocking = True

        # This is copied from Restaurant.ordered_facets, should be cleaned up
        # Reverse ordered for display
        self.facets = [
            'Food/Drinks',
            'Service',
            'Cleanliness'
        ]
        self.reviewed = []

    @draw_menu
    def show(self):
        print_msg = super(ReviewExperienceMenu, self).make_msg_print_func()

        msg = '{facet} score? (1-5)'.format(
            facet=self.facets[-1],
        )
        print_msg(0, self.business_name)
        print_msg(1, msg)

    def select_option(self, num):
        if num >= 1 and num <= 5:
            self.reviewed.append((self.facets.pop(), num))
        else:
            return MessageMenu(self.panel, 'Please give a rating of 1-5 stars')

        if self.facets:
            return 'Still review...'
        else:
            review = yelpdor.city.Review([(facet, score) for facet, score in self.reviewed])
            self.review_callback(review)
            return None
