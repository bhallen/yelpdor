import os
import random

import lib.libtcodpy as libtcod
from game_obj import GameObj

HUMAN_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/textgen/jice_mesopotamian.cfg'
DWARF_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/textgen/mingos_dwarf.cfg'
ELF_NAME_CFG_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../res/textgen/lbeer_elven.cfg'

libtcod.namegen_parse(HUMAN_NAME_CFG_PATH)
libtcod.namegen_parse(DWARF_NAME_CFG_PATH)
libtcod.namegen_parse(ELF_NAME_CFG_PATH)

NAME_TYPES = ['Mesopotamian female',
         'Mesopotamian male',
         'elf male',
         'dwarf female',
         'dwarf male']


def generate_name(name_type=None):
    # returns a tuple of (name, surname)

    if not name_type:
        name_type = random.choice(NAME_TYPES)
    name = libtcod.namegen_generate(name_type)

    if name_type in ['dwarf female', 'dwarf male']: # types with distinct surnames
        surname = libtcod.namegen_generate('dwarf surname')
    elif name_type in ['Mesopotamian female', 'Mesopotamian male']:
        surname = libtcod.namegen_generate(name_type)
    elif name_type in ['elf female', 'elf male']:
        surname = libtcod.namegen_generate(name_type)
    
    return (name, surname)


class NPC(GameObj):

    def __init__(self):
        self.type = random.choice(NAME_TYPES)

        self.name, self.surname = generate_name(self.type)
        self.color = libtcod.Color(255, 255, 0)

        if self.type in ['dwarf female', 'dwarf male']:
            self.char = 'd'
        elif self.type in ['Mesopotamian female', 'Mesopotamian male']:
            self.char = 'h'
        elif self.type in ['elf female', 'elf male']:
            self.char = 'e'

    def __repr__(self):
        return '{}, {}'.format(self.name, self.type)
