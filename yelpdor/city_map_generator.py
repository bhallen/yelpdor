import random

from tile import TileType
from tile import create_tile
from tile import Rect
from dungeon_map import DungeonMap

MIN_BLOCK_SIZE = 25
MAX_BLOCK_SIZE = 50

MIN_BIZ_SIZE = 5
MAX_BIZ_SIZE = 12

def divide_line(length, min_size, max_size):
    # generates dividers in the range 0 <= i < length
    # such that the remaining intervals are between min_size and max_size
    if length <= 2 * min_size:
        return []
    else:
        divide_point = random.randint(max(min_size, length - max_size - 1), length - min_size - 1)
        return divide_line(divide_point, min_size, max_size) + [divide_point]

def generate_city_map(width, height):
    # generates a grid-based city map

    dmap = DungeonMap(width, height)

    def draw_street(start, end, size=2):
        # draws a street from start to end, inclusive
        # there are size street tiles both left and right of center
        start_x, start_y = start
        end_x, end_y = end

        if start_x == end_x:
            for y in range(start_y, end_y + 1):
                for x in range(
                    start_x - size,
                    start_x + size + 1
                ):
                    if not dmap.within_map(x, y):
                        continue
                    dmap[x][y] = create_tile(TileType.street)
        elif start_y == end_y:
            # (I'm sure there's a nice way to deduplicate this code, but s/x/y is easier)
            for x in range(start_x, end_x + 1):
                for y in range(
                    start_y - size,
                    start_y + size + 1
                ):
                    if not dmap.within_map(x, y):
                        continue
                    dmap[x][y] = create_tile(TileType.street)

    blocks = []

    dmap.spawn = None

    def streetify_rect(rect):
        if rect.w < 2 * MIN_BLOCK_SIZE and rect.h < 2 * MIN_BLOCK_SIZE:
            # find the adjacent streets
            x1, y1 = rect.center()
            x2, y2 = x1, y1
            while dmap.within_map(x1, y1) and dmap[x1][y1].tile_type != TileType.street:
                x1 -= 1
            x1 += 1
            while dmap.within_map(x1, y1) and dmap[x1][y1].tile_type != TileType.street:
                y1 -= 1
            y1 += 1
            while dmap.within_map(x2, y2) and dmap[x2][y2].tile_type != TileType.street:
                x2 += 1
            x2 -= 1
            while dmap.within_map(x2, y2) and dmap[x2][y2].tile_type != TileType.street:
                y2 += 1
            y2 -= 1
            blocks.append(Rect(x1, y1, x2 - x1 + 1, y2 - y1 + 1))
            return
        vertical = random.randint(0, 1) == 1
        if rect.w < 2 * MIN_BLOCK_SIZE:
            vertical = False
        elif rect.h < 2 * MIN_BLOCK_SIZE:
            vertical = True

        if vertical:
            street_x = random.randint(rect.x1 + MIN_BLOCK_SIZE, rect.x2 - MIN_BLOCK_SIZE)
            if not dmap.spawn:
                dmap.spawn = (street_x, (rect.y1 + rect.y2) / 2)
            draw_street((street_x, rect.y1), (street_x, rect.y2))
            streetify_rect(Rect(rect.x1, rect.y1, street_x - rect.x1, rect.h))
            streetify_rect(Rect(street_x, rect.y1, rect.x2 - street_x, rect.h))
        else:
            street_y = random.randint(rect.y1 + MIN_BLOCK_SIZE, rect.y2 - MIN_BLOCK_SIZE)
            if not dmap.spawn:
                dmap.spawn = ((rect.x1 + rect.x2) / 2, street_y)
            draw_street((rect.x1, street_y), (rect.x2, street_y))
            streetify_rect(Rect(rect.x1, rect.y1, rect.w, street_y - rect.y1))
            streetify_rect(Rect(rect.x1, street_y, rect.w, rect.y2 - street_y))

    for x in range(0, width):
        for y in range(0, height):
            if x <3 or y <3 or width - x <= 3 or height - y <= 3:
                dmap[x][y] = create_tile(TileType.street)
    streetify_rect(Rect(3, 3, width - 6, height - 6))

    dmap.rooms = []

    def create_room(rect):
        for y in range(rect.y1, rect.y2):
            for x in range(rect.x1, rect.x2):
                if x == rect.x1 or x == rect.x2 - 1 or y == rect.y1 or y == rect.y2 - 1:
                    dmap[x][y] = create_tile(TileType.wall)
                else:
                    dmap[x][y] = create_tile(TileType.floor)
        dmap.rooms.append(Rect(rect.x1 + 1, rect.y1 + 1, rect.w - 2, rect.h - 2))

    def fill_block(block):
        # used to make sure rooms don't intersect each other
        room_hitboxes = []
        block_rooms = []

        top_divs = divide_line(block.w - 1, MIN_BIZ_SIZE, MAX_BIZ_SIZE)
        bottom_divs = divide_line(block.w - 1, MIN_BIZ_SIZE, MAX_BIZ_SIZE)
        left_divs = divide_line(block.h - 1, MIN_BIZ_SIZE, MAX_BIZ_SIZE)
        right_divs = divide_line(block.h - 1, MIN_BIZ_SIZE, MAX_BIZ_SIZE)

        # place corner rooms first
        room = Rect(block.x1, block.y1, top_divs[0] + 1, left_divs[0] + 1)
        room_hitboxes.append(Rect(room.x1, room.y1, room.w - 1, room.h - 1))
        create_room(room)
        room = Rect(block.x1 + top_divs[-1], block.y1, block.w - top_divs[-1], right_divs[0] + 1)
        room_hitboxes.append(Rect(room.x1, room.y1, room.w - 1, room.h - 1))
        create_room(room)
        room = Rect(block.x1, block.y1 + left_divs[-1], bottom_divs[0] + 1, block.h - left_divs[-1])
        room_hitboxes.append(Rect(room.x1, room.y1, room.w - 1, room.h - 1))
        create_room(room)
        room = Rect(block.x1 + bottom_divs[-1], block.y1 + right_divs[-1], block.w - bottom_divs[-1], block.h - right_divs[-1])
        room_hitboxes.append(Rect(room.x1, room.y1, room.w - 1, room.h - 1))
        create_room(room)

        for left, right in zip(top_divs, top_divs[1:]):
            collide = True
            while collide:
                height = random.randint(MIN_BIZ_SIZE, MAX_BIZ_SIZE)
                hitbox = Rect(block.x1 + left, block.y1, right - left, height)
                collide = False
                for other_hitbox in room_hitboxes:
                    if hitbox.intersect(other_hitbox):
                        collide = True
                        break
            room_hitboxes.append(hitbox)
            room = Rect(hitbox.x1, hitbox.y1, hitbox.w + 1, hitbox.h + 1)
            create_room(room)
        for left, right in zip(bottom_divs, bottom_divs[1:]):
            collide = True
            while collide:
                height = random.randint(MIN_BIZ_SIZE, MAX_BIZ_SIZE)
                hitbox = Rect(block.x1 + left, block.y2 - height - 1, right - left, height)
                collide = False
                for other_hitbox in room_hitboxes:
                    if hitbox.intersect(other_hitbox):
                        collide = True
                        break
            room_hitboxes.append(hitbox)
            height = random.randint(MIN_BIZ_SIZE, MAX_BIZ_SIZE)
            room = Rect(hitbox.x1, hitbox.y1, hitbox.w + 1, hitbox.h + 1)
            create_room(room)
        for top, bottom in zip(left_divs, left_divs[1:]):
            collide = True
            while collide:
                width = random.randint(MIN_BIZ_SIZE, MAX_BIZ_SIZE)
                hitbox = Rect(block.x1, block.y1 + top, width, bottom - top)
                collide = False
                for other_hitbox in room_hitboxes:
                    if hitbox.intersect(other_hitbox):
                        collide = True
                        break
            room_hitboxes.append(hitbox)
            room = Rect(hitbox.x1, hitbox.y1, hitbox.w + 1, hitbox.h + 1)
            create_room(room)
        for top, bottom in zip(right_divs, right_divs[1:]):
            collide = True
            while collide:
                width = random.randint(MIN_BIZ_SIZE, MAX_BIZ_SIZE)
                hitbox = Rect(block.x2 - width - 1, block.y1 + top, width, bottom - top)
                collide = False
                for other_hitbox in room_hitboxes:
                    if hitbox.intersect(other_hitbox):
                        collide = True
                        break
            room_hitboxes.append(hitbox)
            height = random.randint(MIN_BIZ_SIZE, MAX_BIZ_SIZE)
            room = Rect(hitbox.x1, hitbox.y1, hitbox.w + 1, hitbox.h + 1)
            create_room(room)

    for block in blocks:
        fill_block(block)

    # create doors for all the rooms
    for room in dmap.rooms:
        good_spots = []
        cx, cy = room.center()
        if dmap[room.x1 - 2][cy].tile_type == TileType.street:
            good_spots += [(room.x1 - 1, y) for y in range(room.y1 + 1, room.y2)]
        if dmap[room.x2 + 1][cy].tile_type == TileType.street:
            good_spots += [(room.x2, y) for y in range(room.y1 + 1, room.y2)]
        if dmap[cx][room.y1 - 2].tile_type == TileType.street:
            good_spots += [(x, room.y1 - 1) for x in range(room.x1 + 1, room.x2)]
        if dmap[cx][room.y2 + 1].tile_type == TileType.street:
            good_spots += [(x, room.y2) for x in range(room.x1 + 1, room.x2)]
        if len(good_spots) > 0:
            door_x, door_y = random.choice(good_spots)
            dmap[door_x][door_y] = create_tile(TileType.door)

    return dmap
