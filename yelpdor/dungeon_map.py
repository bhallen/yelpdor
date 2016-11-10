from tile import Tile


def make_map(height, width):

    #fill map with "unblocked" tiles
    dmap = [[ Tile(False)
        for y in range(height) ]
            for x in range(width) ]

    #place two pillars to test the map
    dmap[30][22].blocked = True
    dmap[30][22].block_sight = True
    dmap[50][22].blocked = True
    dmap[50][22].block_sight = True

    return dmap
