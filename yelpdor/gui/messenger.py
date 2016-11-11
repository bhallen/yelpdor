import textwrap

from lib import libtcodpy as libtcod

    
innermessenger = None

class InnerMessenger:
    MSG_X_OFFSET = 2
    BACKGROUND_COLOR = libtcod.black
    queue = []

    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.panel = libtcod.console_new(width, height)
        self.y = screen.height - height


    def render(self):
        libtcod.console_set_default_background(self.panel, self.BACKGROUND_COLOR)
        libtcod.console_clear(self.panel)
        msg_y_offset = 1
        for (line, color) in self.queue:
            libtcod.console_set_default_foreground(self.panel, color)
            libtcod.console_print_ex(self.panel,
                self.MSG_X_OFFSET,
                msg_y_offset,
                libtcod.BKGND_NONE,
                libtcod.LEFT,
                line)
            msg_y_offset += 1
        libtcod.console_blit(self.panel, 0, 0, self.width, self.height, 0, 0, self.y)  

    def message(self, msg, color):
        msg_lines = textwrap.wrap(msg, self.width)
     
        for line in msg_lines:
            if len(self.queue) == self.height:
                del self.queue[0]
            self.queue.append( (line, color) )


class Messenger:
    def __init__(self, width=None, height=None, screen=None):
        global innermessenger 
        if innermessenger is None:
            innermessenger = InnerMessenger(width, height, screen)


    def render(self):
        global innermessenger 
        innermessenger.render()


    def message(self, msg, color=libtcod.white):
        global innermessenger 
        innermessenger.message(msg, color)
