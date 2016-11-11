from abc import ABCMeta
from abc import abstractmethod

from lib import libtcodpy as libtcod


def draw_menu(func):
    '''Decorator for menu drawing.

    Wraps the drawing of menus to clear and initialize the canvas.
    '''

    def decorator(self, *args, **kwargs):
        libtcod.console_set_default_background(self.panel, libtcod.light_red)
        libtcod.console_clear(self.panel)

        func(self, *args, **kwargs)
    return decorator


class AmuletMenu(object):

    __metaclass_ = ABCMeta

    def __init__(self, panel):
        self.name = 'Name'
        self.panel = panel

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def select_option(self, num):
        pass
