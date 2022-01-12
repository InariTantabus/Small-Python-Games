import pygame, sys, os

def shape_tiles(tile, tile_map, tileset):
    pos = [0, 0]
    if tile_map[tile][2] == 'ground':
        if str(tile_map[tile][0]) + ';' + str(tile_map[tile][1] - 1) not in tile_map:
            pos[0] = 1
        elif str(tile_map[tile][0]) + ';' + str(tile_map[tile][1] + 1) not in tile_map:
            pos[0] = 3
        else:
            pos[0] = 2
        if str(tile_map[tile][0] - 1) + ';' + str(tile_map[tile][1]) not in tile_map:
            pos[1] = 1
        elif str(tile_map[tile][0] + 1) + ';' + str(tile_map[tile][1]) not in tile_map:
            pos[1] = 3
        else:
            pos[1] = 2

        temp = [1, 2, 3, 8, 9, 4, 7, 6, 5][[[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]].index(pos)]

    return tileset[temp]





