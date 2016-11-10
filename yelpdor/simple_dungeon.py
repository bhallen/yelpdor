import libtcodpy as libtcod

from dungeon_map import DungeonMap
from tile import Tile
from tile import Rect


ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30


def create_room(dmap, room):
    #go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            dmap[x][y].blocked = False
            dmap[x][y].block_sight = False


def create_h_tunnel(dmap, x1, x2, y):
    #horizontal tunnel. min() and max() are used in case x1>x2
    for x in range(min(x1, x2), max(x1, x2) + 1):
        dmap[x][y].blocked = False
        dmap[x][y].block_sight = False


def create_v_tunnel(dmap, y1, y2, x):
    #vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        dmap[x][y].blocked = False
        dmap[x][y].block_sight = False


def make_map(player, height, width):
    #fill map with "blocked" tiles
    dmap = DungeonMap(width, height)

    num_rooms = 0

    for r in range(MAX_ROOMS):
        #random width and height
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        #random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, width - w - 1)
        y = libtcod.random_get_int(0, 0, height - h - 1)

        #"Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        #run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in dmap.rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            #this means there are no intersections, so this room is valid

            #"paint" it to the map's tiles
            create_room(dmap, new_room)

            #center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                #this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                #all rooms after the first:
                #connect it to the previous room with a tunnel

                #center coordinates of previous room
                (prev_x, prev_y) = dmap.rooms[num_rooms-1].center()

                #draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    create_h_tunnel(dmap, prev_x, new_x, prev_y)
                    create_v_tunnel(dmap, prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    create_v_tunnel(dmap, prev_y, new_y, prev_x)
                    create_h_tunnel(dmap, prev_x, new_x, new_y)

            #finally, append the new room to the list
            dmap.rooms.append(new_room)
            num_rooms += 1

    return dmap
