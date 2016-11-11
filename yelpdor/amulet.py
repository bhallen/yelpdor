from lib.libtcodpy import *

PANEL_WIDTH = 30
PANEL_HEIGHT = 15

AMULET_MODE, STATS_MODE = range(2)

class Amulet:
    '''Mobile app used to navigate and see stats'''
    
    def __init__(self, player, x=0, y=0):
        self.player = player
        self.x = x
        self.y = y

        self.panel = console_new(PANEL_WIDTH, PANEL_HEIGHT)
        self.mode = AMULET_MODE


    def draw(self, con):
        if self.mode == AMULET_MODE:
            # Start with red canvas, similar mobile app
            console_set_default_background(self.panel,light_red)
            console_clear(self.panel)

            # Print menu
            self.draw_menu()
            console_blit(self.panel, 0, 0, 0, 0, con, self.x, self.y)
        elif self.mode == STATS_MODE:
            console_set_default_background(self.panel,black)
            console_clear(self.panel)

            self.draw_stats(con)
        else:
            raise Exception('Unsupported mode')

        # Draw the panel onto main game screen


    def draw_menu(self):
        console_print(self.panel, 0, 0, 'Amulet of Yelpdor')
        console_print(self.panel, 0, 1, '1. Nearby restaurants')
        console_print(self.panel, 0, 2, '2. Stats')
        console_print(self.panel, 0, 3, '3. Show Help')
        console_print(self.panel, 0, 4, '4. Quit Game')


    def draw_stats(self, con):
        console_print(con, self.x, self.y, 'Review count: {}'.format(self.player.review_count))
        console_print(con, self.x, self.y + 1, 'Reputation:   {}'.format(self.player.reputation))


    def toggle_mode(self):
        if self.mode == AMULET_MODE:
            self.mode = STATS_MODE
        else:
            self.mode = AMULET_MODE
