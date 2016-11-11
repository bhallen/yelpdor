import math
import random

from yelpdor.game_obj import GameObj
from yelpdor.gui.messenger import Messenger
from yelpdor.npc import generate_name
from yelpdor.utils import load_eventset


FAN_COMMENT_PROBABILITY = 0.2


class Player(GameObj):  # pylint: disable=too-many-instance-attributes

    def __init__(self, x, y, char, color):
        GameObj.__init__(self, x, y, char, color)
        self.total_ticks = 0
        self.review_count = 0
        self.reputation = 0
        self.fame_level = 0
        self.health = 100  # percent
        self.hunger = 0  # percent; health starts decreasing at 100% hunger
        self.dollars = 20
        self.ticks_between_payments = 20
        self.ticks_between_hunger_ticks = 2
        self.current_business = ''

        self.dungeon_map = None
        self.district = None
        self.amulet = None

    def set_level(self, dungeon_map, district):
        self.dungeon_map = dungeon_map
        self.district = district

    def move(self, dmap, dx, dy):
        # move by the given amount, if the destination is not blocked
        if (dmap.within_map(self.x + dx, self.y + dy) and
                not dmap[self.x + dx][self.y + dy].blocked):
            self.x += dx
            self.y += dy
            self.tick()

    def tick(self):
        self.total_ticks += 1
        if self.total_ticks % self.ticks_between_hunger_ticks == 0:
            self.tick_hunger()
        if self.total_ticks % self.ticks_between_payments == 0 and self.fame_level > 0:
            self.receive_payment()

        if self.district:
            # check position for events
            player_business = self.district.find_business_containing_player(self)
            if player_business and self.current_business != player_business:
                self.current_business = player_business
                self.current_business.visit(self)
            elif not player_business and self.current_business:
                self.current_business.leave_review(self)
                self.current_business = None

    def tick_hunger(self):
        if self.health == 0:
            Messenger().message('You are dead.')
            self.char = 'X'
        elif self.hunger == 100:
            if self.health > 30:
                Messenger().message('You are starving to death.')
                Messenger().message('')
            else:
                Messenger().message('You are literally starving to death. Quite literally.')
                Messenger().message('')
            self.health -= 1
        else:
            self.hunger += 1
            if self.hunger < 50:
                if self.health != 100:
                    self.health = self.health + 1
            if self.hunger > 40 and self.hunger < 80 and self.hunger % 10 == 0:
                Messenger().message('You are hungry.')
                Messenger().message('')
            elif self.hunger >= 80 and self.hunger % 3 == 0:
                Messenger().message('You are very hungry.')
                Messenger().message('')

    def update_reviewing_stats(self, player_review, business):
        self.review_count += 1
        review_accuracy = business.get_review_similarity(player_review)
        self.reputation += review_accuracy
        previous_fame_level = self.fame_level
        self.fame_level = int(math.floor(self.reputation))
        if self.fame_level > previous_fame_level:
            Messenger().message('You become more famous for your accurate business reviews!')
            Messenger().message('')
        return review_accuracy

    def receive_payment(self):
        payment = int(round(math.log(self.review_count) * self.reputation))
        payment += random.randint(-1, 2)
        if payment > 0:
            events = load_eventset('fanstory')
            self.dollars += payment
            Messenger().message('You received {} dollar{} from your fans.'.format(
                payment,
                's' if payment > 1 else '',
            ))
            if random.random() < FAN_COMMENT_PROBABILITY:
                name, surname = generate_name()
                Messenger().message('{} writes "{}"'.format(
                    name + ' ' + surname[0] + '.',
                    random.choice(events)),
                )
            Messenger().message('')
