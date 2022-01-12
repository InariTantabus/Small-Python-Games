import pygame, sys, os

tileset = {}
tileset['tl'] = pygame.image.load('data/images/tiles/ground_tl.png')
tileset['t'] = pygame.image.load('data/images/tiles/ground_t.png')
tileset['tr'] = pygame.image.load('data/images/tiles/ground_tr.png')
tileset['r'] = pygame.image.load('data/images/tiles/ground_r.png')
tileset['br'] = pygame.image.load('data/images/tiles/ground_br.png')
tileset['b'] = pygame.image.load('data/images/tiles/ground_b.png')
tileset['bl'] = pygame.image.load('data/images/tiles/ground_bl.png')
tileset['l'] = pygame.image.load('data/images/tiles/ground_l.png')
tileset['c'] = pygame.image.load('data/images/tiles/ground_c.png')
for tile in tileset:
    tileset[tile].set_colorkey((0, 0, 0))

tile_index = {1:tileset['tl'],
              2:tileset['t'],
              3:tileset['tr'],
              4:tileset['r'],
              5:tileset['br'],
              6:tileset['b'],
              7:tileset['bl'],
              8:tileset['l'],
              9:tileset['c']
              }