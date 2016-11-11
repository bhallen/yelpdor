import os
import random

import lib.libtcodpy as libtcod
from game_obj import GameObj

HUMAN_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/textgen/jice_mesopotamian.cfg'
DWARF_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/textgen/mingos_dwarf.cfg'
ELF_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/textgen/lbeer_elven.cfg'

class NPC(GameObj):

    types = ['Mesopotamian female',
             'Mesopotamian male',
             'elf male',
             'dwarf female',
             'dwarf male']

    def __init__(self):
        libtcod.namegen_parse(HUMAN_NAME_CFG_PATH)
        libtcod.namegen_parse(DWARF_NAME_CFG_PATH)
        libtcod.namegen_parse(ELF_NAME_CFG_PATH)

        self.type = random.choice(self.types)
        self.name = libtcod.namegen_generate(self.type)

        self.color = libtcod.Color(255, 255, 0)

        if self.type in ['dwarf female', 'dwarf male']: # types with distinct surnames
            self.surname = libtcod.namegen_generate('dwarf surname')
            self.char = 'd'
        elif self.type in ['Mesopotamian female', 'Mesopotamian male']:
            self.surname = libtcod.namegen_generate(self.type)
            self.char = 'h'
        elif self.type in ['elf female', 'elf male']:
            self.surname = libtcod.namegen_generate(self.type)
            self.char = 'e'

    def __repr__(self):
        return '{}, {}'.format(self.name, self.type)
