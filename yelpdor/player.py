import sys

from game_obj import GameObj

class Player(GameObj):

    def __init__(self, x, y, char, color):
        GameObj.__init__(self, x, y, char, color)
        self.total_ticks = 0
        self.review_count = 0
        self.reputation = 0
        self.hunger = 0  # death at 100 for now
        self.dollars = 20
        self.ticks_between_payments = 100
        self.ticks_between_hunger_ticks = 1

    def tick(self):
        self.total_ticks += 1
        if self.total_ticks % self.ticks_between_hunger_ticks == 0:
            self.tick_hunger()
        if self.total_ticks % self.ticks_between_payments == 0:
            self.receive_payment()

    def tick_hunger(self):
        self.hunger += 1
        if self.hunger >= 100:
            sys.exit("You are dead.")
        elif self.hunger > 40 and self.hunger < 80 and self.hunger % 10 == 0:
            print 'You are hungry.'
        elif self.hunger >= 80 and self.hunger % 3 == 0:
            print 'You are starving. Literally.'

    def update_reviewing_stats(self, facet_to_player_rating, business):
        self.review_count += 1
        self.reputation += business.get_review_similarity(facet_to_player_rating)

    def receive_payment(self):
        payment = round(self.review_count * self.reputation)
        print 'You received {} dollars from your fans.'.format(payment)
        self.dollars += payment


