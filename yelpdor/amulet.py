from lib import libtcodpy as libtcod

PANEL_WIDTH = 30
PANEL_HEIGHT = 20

class Amulet:
    '''Mobile app used to navigate and see stats'''
    
    def __init__(self, x=0, y=0):
        '''
        Param:
        x - x position to draw amulet onto game screen
        y - y position to draw amulet onto game screen
        '''
        self.x = x
        self.y = y

        self.panel = libtcod.console_new(PANEL_WIDTH, PANEL_HEIGHT)
        self.visible = False

    def draw(self, con):
        if self.visible:
            # Start with clear canvas
            libtcod.console_set_default_background(self.panel,libtcod.light_red)
            libtcod.console_clear(self.panel)

            # Print menu
            self.draw_menu()

            # Draw the panel onto main game screen
            libtcod.console_blit(self.panel, 0, 0, 0, 0, con, self.x, self.y)


    def draw_menu(self):
            libtcod.console_print(self.panel, 0, 0,"Amulet of Yelpdor")
            libtcod.console_print(self.panel, 0, 1,"1. Nearby restaurant")
            libtcod.console_print(self.panel, 0, 2,"2. Stats")
            libtcod.console_print(self.panel, 0, 3,"3. Show Help")
            libtcod.console_print(self.panel, 0, 4,"4. Quit Game")


    def toggle_visibility(self):
        self.visible = not self.visible
