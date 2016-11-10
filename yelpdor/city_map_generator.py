import random

from tile import TileType
from tile import create_tile
from tile import Rect
from dungeon_map import DungeonMap

MIN_BLOCK_SIZE = 13
MAX_BLOCK_SIZE = 21

def generate_city_map(width, height):
    # generates a grid-based city map

    dmap = DungeonMap(width, height)

    def draw_street(start, end, street_size=1, sidewalk_size=1):
        # draws a street from start to end, inclusive
        # there are street_size street tiles both left and right of center
        # and sidewalks are sidewalk_size wide
        # does not overwrite existing street tiles with sidewalk tiles
        start_x, start_y = start
        end_x, end_y = end

        if start_x == end_x:
            for y in range(start_y, end_y + 1):
                for x in range(
                    start_x - street_size - sidewalk_size,
                    start_x + street_size + sidewalk_size + 1
                ):
                    if not dmap.within_map(x, y):
                        continue
                    if abs(x - start_x) <= street_size:
                        dmap[x][y] = create_tile(TileType.street)
                    elif not dmap[x][y].tile_type == TileType.street:
                        dmap[x][y] = create_tile(TileType.sidewalk)
        elif start_y == end_y:
            # (I'm sure there's a nice way to deduplicate this code, but s/x/y is easier)
            for x in range(start_x, end_x + 1):
                for y in range(
                    start_y - street_size - sidewalk_size,
                    start_y + street_size + sidewalk_size + 1
                ):
                    if not dmap.within_map(x, y):
                        continue
                    if abs(y - start_y) <= street_size:
                        dmap[x][y] = create_tile(TileType.street)
                    elif not dmap[x][y].tile_type == TileType.street:
                        dmap[x][y] = create_tile(TileType.sidewalk)

    blocks = []

    dmap.spawn = None

    def streetify_rect(rect):
        if rect.w < 2 * MIN_BLOCK_SIZE and rect.h < 2 * MIN_BLOCK_SIZE:
            # find the edges of the sidewalk
            x1, y1 = rect.center()
            x2, y2 = x1, y1
            while dmap.within_map(x1, y1) and dmap[x1][y1].tile_type != TileType.sidewalk:
                x1 -= 1
            x1 += 1
            while dmap.within_map(x1, y1) and dmap[x1][y1].tile_type != TileType.sidewalk:
                y1 -= 1
            y1 += 1
            while dmap.within_map(x2, y2) and dmap[x2][y2].tile_type != TileType.sidewalk:
                x2 += 1
            x2 -= 1
            while dmap.within_map(x2, y2) and dmap[x2][y2].tile_type != TileType.sidewalk:
                y2 += 1
            y2 -= 1
            blocks.append(Rect(x1, y1, x2 - x1, y2 - y1))
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

    streetify_rect(Rect(0, 0, width, height))

    def wall_block(rect):
        for y in range(rect.y1, rect.y2 + 1):
            for x in range(rect.x1, rect.x2 + 1):
                if y == rect.y1 or y == rect.y2 or x == rect.x1 or x == rect.x2:
                    dmap[x][y] = create_tile(TileType.wall)

    for block in blocks:
        wall_block(block)

    # for y in range(height):
    #     row = ''
    #     for x in range(width):
    #         t = dmap[x][y].tile_type
    #         if t == TileType.street:
    #             row += ' '
    #         elif t == TileType.sidewalk:
    #             row += '.'
    #         elif t == TileType.floor:
    #             row += '+'
    #         else:
    #             row += '#'
    #     print(row)

    return dmap
