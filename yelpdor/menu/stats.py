from lib.libtcodpy import console_print


class Stats(object):  # pylint: disable=too-few-public-methods

    def __init__(self, x, y, player):
        self.x_pos = x
        self.y_pos = y
        self.player = player

    def draw(self, con):
        print_msg = make_msg_print(con, self.x_pos, self.y_pos)

        print_msg(0, 'Health: {}%%'.format(self.player.health))
        print_msg(1, 'Hunger: {}%%'.format(self.player.hunger))

        print_msg(3, 'Money: ${}'.format(self.player.dollars))

        print_msg(5, 'Review count: {}'.format(self.player.review_count))
        print_msg(6, 'Fame level: {}'.format(self.player.fame_level))


def make_msg_print(screen, x_offset, y_offset):
    def func(line_num, msg):
        console_print(screen, x_offset, y_offset + line_num, msg)
    return func
