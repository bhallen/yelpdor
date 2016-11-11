import os
import random

import lib.libtcodpy as libtcod

HUMAN_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/namegen/jice_mesopotamian.cfg'
DWARF_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/namegen/mingos_dwarf.cfg'

class NPC:

    types = ['Mesopotamian female',
             'Mesopotamian male',
             'dwarf female',
             'dwarf male']

    def __init__(self):
        libtcod.namegen_parse(HUMAN_NAME_CFG_PATH)
        libtcod.namegen_parse(DWARF_NAME_CFG_PATH)

        self.type = random.choice(self.types)
        self.name = libtcod.namegen_generate(self.type)

        if self.type in ['dwarf female', 'dwarf male']: # types with distinct surnames
            self.surname = libtcod.namegen_generate('dwarf surname')
        else:
            self.surname = libtcod.namegen_generate(self.type)

    def __repr__(self):
        return '{}, {}'.format(self.name, self.type)