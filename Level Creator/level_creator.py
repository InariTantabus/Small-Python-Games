import pygame, sys, os, random

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Level Creator')

WINDOW_SIZE = (1200, 800)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((600, 400))

top_left = pygame.image.load('data/images/ground_tl.png')
top = pygame.image.load('data/images/ground_t.png')
top_right = pygame.image.load('data/images/ground_tr.png')
right = pygame.image.load('data/images/ground_r.png')
bot_right = pygame.image.load('data/images/ground_br.png')
bot = pygame.image.load('data/images/ground_b.png')
bot_left = pygame.image.load('data/images/ground_bl.png')
left = pygame.image.load('data/images/ground_l.png')
center = pygame.image.load('data/images/ground_c.png')
top_left.set_colorkey((0, 0, 0))
top.set_colorkey((0, 0, 0))
top_right.set_colorkey((0, 0, 0))
right.set_colorkey((0, 0, 0))
bot_right.set_colorkey((0, 0, 0))
bot.set_colorkey((0, 0, 0))
bot_left.set_colorkey((0, 0, 0))
left.set_colorkey((0, 0, 0))

grass_img = pygame.image.load('data/images/grass.png')
dirt_img = pygame.image.load('data/images/dirt.png')
plant_img = pygame.image.load('data/images/plant.png')
air_img = pygame.image.load('data/images/air.png')
air_img.set_colorkey((255, 255, 255))

font = pygame.font.SysFont(None, 20)

scroll = [0, 0]
scroll_amt = 2

scroll_right = False
scroll_left = False
scroll_up = False
scroll_down = False

click = False
drag = False

active_tile = 0
active_tile_img = air_img
temp_tile = 'air'
temp_tile_img = air_img
btns = {}
tiles = {}
lines = {}

def load_map(path):
  f = open(path + '.txt', 'r')
  data = f.read()
  f.close()
  data = data.split('\n')
  game_map = []
  for row in data:
    game_map.append(list(row))
  y = 0
  current_tile = grass_img
  for line in game_map:
    x = 0
    for tile in line:
      if tile == '2':
        current_tile = grass_img
      elif tile == '1':
        current_tile = dirt_img
      if tile != '0':
        tiles[((x * 16), (y * 16))] = [current_tile, ((x * 16), (y * 16))]
      x += 1
    y +=  1

def find_fl_tiles():
  if tiles:
    first_tile = ((tiles[list(tiles.keys())[0]][1][0] / 16), (tiles[list(tiles.keys())[0]][1][1] / 16))
    last_tile = ((tiles[list(tiles.keys())[0]][1][0] / 16), (tiles[list(tiles.keys())[0]][1][1] / 16))
    for tile in tiles:
      if (tiles[tile][1][0] / 16) < first_tile[0]:
        first_tile = ((tiles[tile][1][0] / 16), first_tile[1])
      if (tiles[tile][1][1] / 16) < first_tile[1]:
        first_tile = (first_tile[0], (tiles[tile][1][1] / 16))
      if (tiles[tile][1][0] / 16) > last_tile[0]:
        last_tile = ((tiles[tile][1][0] / 16), last_tile[1])
      if (tiles[tile][1][1] / 16) > last_tile[1]:
        last_tile = (last_tile[0], (tiles[tile][1][1] / 16))
  return first_tile, last_tile

def save_map(path):
  if tiles:
    first_tile, last_tile = find_fl_tiles()
    save_file = ''
    for i in range(int(last_tile[1] - first_tile[1]) + 1):
      for v in range(int(last_tile[0] - first_tile[0]) + 1):
        if (((v + first_tile[0]) * 16), ((i + first_tile[1]) * 16)) not in tiles:
          save_file += '0'
        else:
          if tiles[(((v + first_tile[0]) * 16), ((i + first_tile[1]) * 16))][0] == grass_img:
            save_file += '2'
          if tiles[(((v + first_tile[0]) * 16), ((i + first_tile[1]) * 16))][0] == dirt_img:
            save_file += '1'
      save_file += '\n'
    f = open(path + '.txt', 'w')
    data = f.write(save_file)
    f.close()

def draw_text(text, font, color, surface, x, y):
  textobj = font.render(text, 1, color)
  textrect = textobj.get_rect()
  textrect.topleft = (x, y)
  surface.blit(textobj, textrect)

def tile_btn(tile, tile_name, x, y, size_x, size_y):
  btns["{0}".format(tile_name)] = pygame.Rect(x, y, size_x, size_y)
  display.blit(pygame.transform.scale(tile, (size_x, size_y)), (x, y))

def draw_grid():
  for i in range(27):
    pygame.draw.line(display, (150, 150, 150), (0, (i * 16 - 16 - (scroll[1] % 16))), (400, (i * 16 - 16 - (scroll[1] % 16))), 1)
    pygame.draw.line(display, (150, 150, 150), ((i * 16 - 16 - (scroll[0] % 16)), 0), ((i * 16 - 16 - (scroll[0] % 16)), 400), 1)

#-----------------------------------------------------------------------------------------------------#

while True:
  display.fill((146,244,255))

  if scroll_amt < 2:
    scroll_amt = 2

  if scroll_right:
    scroll[0] += scroll_amt
  if scroll_left:
    scroll[0] -= scroll_amt
  if scroll_up:
    scroll[1] -= scroll_amt
  if scroll_down:
    scroll[1] += scroll_amt

  mx, my = pygame.mouse.get_pos()
  mx = (mx / 2)
  my = (my / 2)
  scroll_mx = (mx + scroll[0])
  scroll_my = (my + scroll[1])
  tile_mxy = (scroll_mx - (scroll_mx % 16), scroll_my - (scroll_my % 16)) # mouse (x, y) in tile grid
  tile_loc_mxy = ((tile_mxy[0] / 16 - 12), (tile_mxy[1] / 16 - 12))

  right_panel = pygame.Rect(400, 0, 200, 400)
  r_panel_seperator = pygame.Rect(400, 82, 200, 6)
  active_tile_panel = pygame.Rect(480, 30, 40, 40)
  canvas = pygame.Rect(0, 0, 400, 400)
  clear_map_btn = pygame.Rect(560, 10, 30, 10)
  load_map_btn = pygame.Rect(560, 25, 30, 10)
  save_map_btn = pygame.Rect(560, 40, 30, 10)

  draw_grid()

  tile_btn(grass_img, 'grass', 412, 100, 32, 32)
  tile_btn(dirt_img, 'dirt', 455, 100, 32, 32)
  tile_btn(air_img, 'air', 498, 100, 32, 32)

  tile_btn(top_left, 'tl', 412, 143, 32, 32)
  tile_btn(top, 't', 455, 143, 32, 32)
  tile_btn(top_right, 'tr', 498, 143, 32, 32)
  tile_btn(right, 'r', 498, 186, 32, 32)
  tile_btn(bot_right, 'br', 498, 229, 32, 32)
  tile_btn(bot, 'b', 455, 229, 32, 32)
  tile_btn(bot_left, 'bl', 412, 229, 32, 32)
  tile_btn(left, 'l', 412, 186, 32, 32)
  tile_btn(center, 'c', 455, 186, 32, 32)

  if click:
    if btns['grass'].collidepoint((mx, my)):
      active_tile = 'grass'
      active_tile_img = grass_img
    if btns['dirt'].collidepoint((mx, my)):
      active_tile = 'dirt'
      active_tile_img = dirt_img
    if btns['air'].collidepoint((mx, my)):
      active_tile = 'air'
      active_tile_img = air_img
    if btns['tl'].collidepoint((mx, my)):
      active_tile = 'tl'
      active_tile_img = top_left
    if btns['t'].collidepoint((mx, my)):
      active_tile = 't'
      active_tile_img = top
    if btns['tr'].collidepoint((mx, my)):
      active_tile = 'tr'
      active_tile_img = top_right
    if btns['r'].collidepoint((mx, my)):
      active_tile = 'r'
      active_tile_img = right
    if btns['br'].collidepoint((mx, my)):
      active_tile = 'br'
      active_tile_img = bot_right
    if btns['b'].collidepoint((mx, my)):
      active_tile = 'b'
      active_tile_img = bot
    if btns['bl'].collidepoint((mx, my)):
      active_tile = 'bl'
      active_tile_img = bot_left
    if btns['l'].collidepoint((mx, my)):
      active_tile = 'l'
      active_tile_img = left
    if btns['c'].collidepoint((mx, my)):
      active_tile = 'c'
      active_tile_img = center
    if clear_map_btn.collidepoint((mx, my)):
      tiles.clear()
    if load_map_btn.collidepoint((mx, my)):
      tiles.clear()
      load_map('tiles')
    if save_map_btn.collidepoint((mx, my)):
      save_map('tiles')

  if canvas.collidepoint((mx, my)) and drag:
    if active_tile != 'air':
      tiles[tile_mxy] = [active_tile_img, tile_mxy]
    elif tile_mxy in tiles:
      del tiles[tile_mxy]

  for tile in tiles:
    tiles[tile][1] = ((tiles[tile][1][0] - scroll[0]), (tiles[tile][1][1] - scroll[1]))
    if tiles[tile][1][0] > -32 and tiles[tile][1][0] < (display.get_width() + 32) and tiles[tile][1][1] > -32 and tiles[tile][1][1] < (display.get_height() + 32):
      display.blit(tiles[tile][0], tiles[tile][1])
    tiles[tile][1] = ((tiles[tile][1][0] + scroll[0]), (tiles[tile][1][1] + scroll[1]))

  pygame.draw.rect(display, (100, 100, 100), right_panel)
  pygame.draw.rect(display, (255, 255, 255), active_tile_panel)
  pygame.draw.rect(display, (50, 50, 50), r_panel_seperator)

  draw_text('{}'.format(tile_loc_mxy), font, (255, 255, 255), display, 410, 10)
  pygame.draw.rect(display, (245, 10, 10), clear_map_btn)
  pygame.draw.rect(display, (10, 245, 10), load_map_btn)
  pygame.draw.rect(display, (10, 10, 245), save_map_btn)
  draw_text('clear', font, (0, 0, 0), display, 525, 7)
  draw_text('load', font, (0, 0, 0), display, 525, 22)
  draw_text('save', font, (0, 0, 0), display, 525, 37)

  tile_btn(grass_img, 'grass', 412, 100, 32, 32)
  tile_btn(dirt_img, 'dirt', 455, 100, 32, 32)
  tile_btn(air_img, 'air', 497, 100, 32, 32)

  tile_btn(top_left, 'tl', 412, 143, 32, 32)
  tile_btn(top, 't', 455, 143, 32, 32)
  tile_btn(top_right, 'tr', 498, 143, 32, 32)
  tile_btn(right, 'r', 498, 186, 32, 32)
  tile_btn(bot_right, 'br', 498, 229, 32, 32)
  tile_btn(bot, 'b', 455, 229, 32, 32)
  tile_btn(bot_left, 'bl', 412, 229, 32, 32)
  tile_btn(left, 'l', 412, 186, 32, 32)
  tile_btn(center, 'c', 455, 186, 32, 32)

  if active_tile_img:
    display.blit(pygame.transform.scale(active_tile_img, (32, 32)), (484, 34))

  click = False
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if event.type == KEYDOWN:
      if event.key == K_d:
        scroll_right = True
      if event.key == K_a:
        scroll_left = True
      if event.key == K_w:
        scroll_up = True
      if event.key == K_s:
        scroll_down = True
    if event.type == KEYUP:
      if event.key == K_d:
        scroll_right = False
      if event.key == K_a:
        scroll_left = False
      if event.key == K_w:
        scroll_up = False
      if event.key == K_s:
        scroll_down = False
    if event.type == MOUSEBUTTONDOWN:
      if event.button == 1:
        click = True
        drag = True
      if event.button == 3:
        drag = True
        r_drag = True
        temp_tile = active_tile
        active_tile = 'air'
        temp_tile_img = active_tile_img
        active_tile_img = air_img
      if event.button == 4:
        scroll_amt += 1
      if event.button == 5:
        scroll_amt -= 1
    if event.type == MOUSEBUTTONUP:
      if event.button == 1:
        drag = False
      if event.button == 3:
        drag = False
        r_drag = False
        active_tile_img = temp_tile_img
        active_tile = temp_tile
      
  screen.blit(pygame.transform.scale(display, WINDOW_SIZE),(0, 0))
  pygame.display.update()
  mainClock.tick(60)
