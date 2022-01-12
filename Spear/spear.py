import pygame, sys, os, random, math

import scripts.tileset_loader as t
import scripts.arc_engine_v1 as ae
import scripts.shape_tiles as shape_tiles
import scripts.rotate as rotate

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Spear Platformer')

WINDOW_SIZE = (1200, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((600, 400))
#----------------Setup pygame/window----------------#

true_scroll = [0, 0]
scroll = [0, 0]
player_momentum = [0, 0]
jumps = 1
font = pygame.font.SysFont(None, 20)
ramps = []
on_spear = False

moving_right = False
moving_left = False
click = False

TILE_SIZE = 16
tile_map = {}
tile_rects = []
for v in range(3):
    for i in range(12):
        tile_map[str(i - 2) + ';' + str(v + 3)] = (i - 2, v + 3, 'ground')
tile_map['8;2'] = (8, 2, 'ground')
tile_map['9;2'] = (9, 2, 'ground')
tile_map['-1;2'] = (-1, 2, 'ground')
tile_map['-2;2'] = (-2, 2, 'ground')
for i in range(4):
    tile_map['15;' + str(i + 0)] = (15, i + 0, 'ground')
for i in range(4):
    tile_map['16;' + str(i + 0)] = (16, i + 0, 'ground')
for v in range(2):
    for i in range(2):
        tile_map[str(i + 11) + ';' + str(v + 1)] = (i + 11, v + 1, 'ground')
for v in range(2):
    for i in range(2):
        tile_map[str(i + 8) + ';' + str(v)] = (i + 8, v, 'ground')

for tile in tile_map:
    tile_rects.append(pygame.Rect(tile_map[tile][0] * TILE_SIZE - scroll[0], tile_map[tile][1] * TILE_SIZE - scroll[1], TILE_SIZE, TILE_SIZE))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def find_angle(sX, sY, pos): ## https://www.youtube.com/watch?v=Y4xlUNfrvow&ab_channel=TechWithTim
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2
    
    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.po + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle

class Spear:
    def __init__(self, x, y, size_x, size_y, angle, stuck=False, in_wall=False):
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.size_x = size_x
        self.size_y = size_y
        self.angle = angle
        self.move_angle = 0
        self.spd = 0
        self.image = pygame.image.load('data/images/spear/spear.png')
        self.image.set_colorkey((0, 0, 0))
        self.rot_image = self.image
        self.power = 30
        self.shoot = False
        self.time = 0
        self.startx = self.x
        self.starty = self.y
        self.stuck = stuck
        self.in_wall = in_wall
        self.falling = False
    
    def draw(self, surf, scroll):
        self.rot_image = rotate.blit_rotate(surf, self.image, (self.x - scroll[0], self.y - scroll[1]), (self.size_x / 2, self.size_y / 2), self.angle);
    
    def move(self, tiles):
        self.stuck = False
        self.in_wall = False
        self.old_x = self.x
        self.old_y = self.y
        self.time += 0.2
        pos = self.throw_path(self.startx, self.starty, self.power, self.move_angle, self.time)
        self.x = pos[0]
        if self.time > 0.2:
            tile_hit_list = ae.collision_test(self.rect(), tiles)
            if len(tile_hit_list) > 0:
                self.time = 0
                self.shoot = False
                self.stuck = True
        self.y = pos[1]
        if self.time > 0.2:
            tile_hit_list = ae.collision_test(self.rect(), tiles)
            if len(tile_hit_list) > 0:
                self.time = 0
                self.shoot = False
                self.stuck = True
        self.get_rotation()
        if not (self.angle-90 >= 75 and self.angle-90 <= 105) and not (self.angle+90 >= 75 and self.angle+90 <= 105):
            self.in_wall = True

    def fall(self, tiles):
        self.stuck = False
        self.in_wall = False
        self.old_x = self.x
        self.old_y = self.y
        self.time += 0.2
        pos = self.throw_path(self.startx, self.starty, self.power, self.move_angle, self.time)
        self.x = pos[0]
        if self.time > 0.2:
            tile_hit_list = ae.collision_test(self.rect(), tiles)
            if len(tile_hit_list) > 0:
                self.time = 0
                self.falling = False
                self.stuck = True
        self.y = pos[1]
        if self.time > 0.2:
            tile_hit_list = ae.collision_test(self.rect(), tiles)
            if len(tile_hit_list) > 0:
                self.time = 0
                self.falling = False
                self.stuck = True
        self.get_rotation()

    def get_rotation(self):
        self.angle = rotate.angle_of_line(self.old_x, self.old_y, self.x, self.y) - 90 % 360

    def throw_path(self, startx, starty, power, angle, time):
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power

        distX = velx * time
        distY = (vely * time) + ((-4.9 * (time)**2) / 2)

        newx = round(distX + startx)
        newy = round(starty - distY)

        return (newx, newy)
    
    def rect(self):
        temp = rotate.point_pos(self.x - 2, self.y - 2, 7, self.angle + 180)
        return pygame.Rect(temp[0], temp[1], 3, 3)
    
    def hitbox(self, scroll=[0, 0]):
        return pygame.Rect(self.x-scroll[0]-self.rot_image.get_width()/2-1, self.y-scroll[1]-self.rot_image.get_height()/2-1, self.rot_image.get_width()+2, self.rot_image.get_height()+2)

ae.load_animations('data/images/entities/')
player = ae.entity(20, 20, 6, 15, 'player')
true_scroll = [(20 - (player.size_x / 2) - (display.get_width() / 2)), (20 - (player.size_y / 2) - (display.get_height() / 2))]

test_spear = Spear(50, 45, 3, 30, 200)

#------------------------------------Game Loop------------------------------------#
while True:
    display.fill((10, 10, 20))

    true_scroll[0] += (player.x - true_scroll[0] - (600 + player.size_x) / 2) / 20
    true_scroll[1] += (player.y - true_scroll[1] - (400 + player.size_y) / 2) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    player.change_frame(1)
    player.display(display, scroll)

    test_spear.draw(display, scroll)

    ramps = [] 
    ramps.append(test_spear) # for spear in spears

    if test_spear.shoot:
        test_spear.move(tile_rects)
    if test_spear.falling:
        test_spear.fall(tile_rects)

    for tile in tile_map:
        temp = shape_tiles.shape_tiles(tile, tile_map, t.tile_index)
        display.blit(temp, (tile_map[tile][0] * TILE_SIZE - scroll[0], tile_map[tile][1] * TILE_SIZE - scroll[1]))

    if moving_right:
        player_momentum[0] += 0.5
        if player_momentum[0] > 1.5:
            player_momentum[0] = 1.5
            player_momentum[0] -= 0.5
    if moving_left:
        player_momentum[0] -= 0.5
        if player_momentum[0] < -1.5:
            player_momentum[0] = -1.5

    if player_momentum[0] > 0:
        player.set_flip(False)
        if player.held_item:
            player.held_item.angle = 290
    if player_momentum[0] < 0:
        player.set_flip(True)
        if player.held_item:
            player.held_item.angle = 70

    player_momentum[1] += 0.15
    collision_types = player.move(player_momentum, tile_rects, ramps)

    on_spear = False
    if test_spear.stuck and test_spear.in_wall:
        if player.rect().colliderect(test_spear.hitbox()):
            temp_angle = test_spear.angle/180*math.pi+(math.pi/2)
            temp_x = test_spear.x+15*math.cos(-temp_angle+math.pi)
            temp_y = test_spear.y+15*math.sin(-temp_angle+math.pi)

            temp_width = temp_x-(player.x+player.size_x/2)
            temp_height = temp_y-(player.y+player.size_y)
            temp_dist = math.sqrt(temp_width**2+temp_height**2)
            temp_y2 = temp_y+temp_dist*math.sin(-temp_angle)

            if player.y+player.size_y/2 < temp_y2:
                if player_momentum[1] >= 0:
                    on_spear = True
                    
                    player.y = temp_y2-player.size_y-1
                    collision_types['bottom'] = True

    if player.y > 100: # respawn if you fall
        player = ae.entity(20, 20, 6, 15, 'player')
        test_spear = Spear(50, 45, 3, 30, 200)
    if test_spear.y > 100: # respawn spear
        test_spear = Spear(50, 45, 3, 30, 200)

    if collision_types['bottom']:
        player_momentum[1] = -.15
        if not moving_right and not moving_left:
            player_momentum[0] = 0
        jumps = 1
    if collision_types['top']:
        player_momentum[1] = 0.15
    if collision_types['right'] or collision_types['left']:
        player_momentum[0] = 0

    #-------------------------------------Testing-------------------------------------#    
    # draw_text('{}'.format(player_momentum[1]), font, (255, 255, 255), display, 20, 20)
    #-------------------------------------Testing-------------------------------------#

    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_SPACE:
                if jumps > 0:
                    if player.rect().colliderect(test_spear.hitbox()):
                        if test_spear.in_wall and on_spear:
                            test_spear.power = 5
                            test_spear.startx = test_spear.x
                            test_spear.starty = test_spear.y
                            test_spear.time = 0
                            if -test_spear.angle > 0 and -test_spear.angle < 180:
                                test_spear.move_angle = find_angle(test_spear.startx, test_spear.starty, (test_spear.x-3, test_spear.y-1))
                            else:
                                test_spear.move_angle = find_angle(test_spear.startx, test_spear.starty, (test_spear.x+3, test_spear.y-1))
                            test_spear.falling = True
                    player_momentum[1] = - 2.8 
                    jumps -= 1
        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if player.held_item:
                    player.held_item = 0
                    if test_spear.shoot != True:
                        test_spear.shoot = True
                        test_spear.power = 30
                        test_spear.startx = test_spear.x
                        test_spear.starty = test_spear.y
                        test_spear.time = 0
                        if player.flip:
                            test_spear.move_angle = find_angle(test_spear.startx, test_spear.starty, (test_spear.x - 100, test_spear.y - 50))
                        else:
                            test_spear.move_angle = find_angle(test_spear.startx, test_spear.starty, (test_spear.x + 100, test_spear.y - 50))
                elif player.rect().colliderect(test_spear.hitbox()):
                    if not test_spear.in_wall and not test_spear.falling:
                        player.held_item = test_spear
                        test_spear.stuck = False
                        test_spear.angle = 290
            if event.button == 2: # testing
                print(temp_y2, player.y)

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    mainClock.tick(60)