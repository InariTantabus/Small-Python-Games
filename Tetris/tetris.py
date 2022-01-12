import pygame, sys, os, random, math

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Tetris')

WINDOW_SIZE = (340, 400)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((340, 400))
#----------------Setup pygame/window----------------#

TILE_SIZE = 20

update_timer = 21
timer_max = 20
block_list = []
minos = []
direction = ''
bag = []
number_list = [0, 1, 2, 3, 4, 5, 6]
next_minos = []
score = 0
last_score = 0
font = pygame.font.SysFont(None, 20)
level = 1
fast_fall = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def get_bag(bag):
    temp_number_list = number_list.copy()
    for i in range(0, len(temp_number_list)):
        temp_number = random.randint(0, len(temp_number_list)-1)
        bag.append(temp_number_list[temp_number])
        temp_number_list.pop(temp_number)
    return bag

def draw_grid():
    for i in range(22):
        pygame.draw.line(display, (50, 50, 50), (1, i*TILE_SIZE), (198, i*TILE_SIZE))
    for i in range(11):
        pygame.draw.line(display, (50, 50, 50), (i*TILE_SIZE-1, 0), (i*TILE_SIZE-1, 400))

def get_mino(minos, bag):
    if len(bag) <= 3:
        bag = get_bag(bag)
    next_minos = [
        Tetramino(12, 2, ['i', 'o', 's', 'z', 'l', 'j', 't'][bag[1]]),
        Tetramino(12, 6, ['i', 'o', 's', 'z', 'l', 'j', 't'][bag[2]]),
        Tetramino(12, 10, ['i', 'o', 's', 'z', 'l', 'j', 't'][bag[3]])]
    temp_letter = ['i', 'o', 's', 'z', 'l', 'j', 't'][bag[0]]
    bag.pop(0)
    minos.append(Tetramino(4, -3, temp_letter, True))
    return minos, bag, next_minos

class Block:
    def __init__(self, x, y, color, active=False):
        self.x = x
        self.y = y
        self.color = color
        self.active = active
        self.blocked = False

    def draw(self):
        if self.active:
            pygame.draw.rect(display, self.color, self.rect())
        else:
            pygame.draw.rect(display, self.color, self.rect())

    def rect(self):
        return pygame.Rect(self.x*TILE_SIZE+1, self.y*TILE_SIZE+1, TILE_SIZE-2, TILE_SIZE-2)

    def update(self, block_list):
        if self.active and not self.blocked:
            self.y += 1
        if self.y+1 >= 20:
            self.blocked = True
        for block in block_list:
            if block.y == self.y+1 and block.x == self.x:
                self.blocked = True

class Tetramino:
    def __init__(self, x, y, mino_type, active=False):
        self.x = x
        self.y = y
        self.type = mino_type
        self.active = active
        self.des = False
        self.rotation = 0
        self.color = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0), (255, 165, 0), (0, 0, 255), (255, 0, 255)][['i', 'o', 's', 'z', 'l', 'j', 't'].index(self.type)]
        self.blocks = [
            [self.block_place(0, 2), self.block_place(1, 2), self.block_place(2, 2), self.block_place(3, 2)], # i
            [self.block_place(0, 0), self.block_place(0, 1), self.block_place(1, 1), self.block_place(1, 0)], # o
            [self.block_place(1, 1), self.block_place(2, 1), self.block_place(0, 2), self.block_place(1, 2)], # s
            [self.block_place(0, 1), self.block_place(1, 1), self.block_place(1, 2), self.block_place(2, 2)], # z
            [self.block_place(0, 1), self.block_place(1, 1), self.block_place(2, 1), self.block_place(0, 2)], # l
            [self.block_place(0, 1), self.block_place(1, 1), self.block_place(2, 1), self.block_place(2, 2)], # j
            [self.block_place(0, 1), self.block_place(1, 1), self.block_place(2, 1), self.block_place(1, 2)] # t
            ][['i', 'o', 's', 'z', 'l', 'j', 't'].index(self.type)]
        if self.active:
            self.toggle_active_blocks()

    def block_place(self, xoset=0, yoset=0):
        return Block(self.x+xoset, self.y+yoset, self.color)

    def toggle_active_blocks(self):
        for block in self.blocks:
            block.active = not block.active

    def update(self, direction, block_list):
        if self.active:
            self.move(direction, block_list)
        for block in self.blocks:
            if block.blocked:
                for block in self.blocks:
                    block_list.append(block)
                self.des = True
                break
        return block_list

    def move(self, direction, block_list):
        if direction == 'right':
            right = True
        if direction == 'left':
            left = True
            
        for block in self.blocks:
            if len(block_list) > 0:
                for tile in block_list:
                    if direction == 'right':
                        if block.x+1 >= 10 or (block.x+1 == tile.x and block.y == tile.y):
                            right = False
                    if direction == 'left':
                        if block.x-1 < 0 or (block.x-1 == tile.x and block.y == tile.y):
                            left = False
            else:
                if direction == 'right':
                    if block.x+1 >= 10:
                        right = False
                if direction == 'left':
                    if block.x-1 < 0:
                        left = False

        for block in self.blocks:
            if direction == 'right':  
                if right:
                    block.x += 1
            if direction == 'left':
                if left:
                    block.x -= 1

    def rotate(self, block_list):
        if self.type != 'o':
            if self.type == 'i':
                if self.rotation == 0:
                    self.blocks[0].x += 2
                    self.blocks[0].y -= 2
                    self.blocks[1].x += 1
                    self.blocks[1].y -= 1
                    self.blocks[3].x -= 1
                    self.blocks[3].y += 1
                    self.rotation = 1
                else:
                    self.blocks[0].x -= 2
                    self.blocks[0].y += 2
                    self.blocks[1].x -= 1
                    self.blocks[1].y += 1
                    self.blocks[3].x += 1
                    self.blocks[3].y -= 1
                    self.rotation = 0
            elif self.type == 's':
                if self.rotation == 0:
                    self.blocks[1].x -= 1
                    self.blocks[1].y -= 1
                    self.blocks[2].x += 2
                    self.blocks[3].x += 1
                    self.blocks[3].y -= 1
                    self.rotation = 1
                else:
                    self.blocks[1].x += 1
                    self.blocks[1].y += 1
                    self.blocks[2].x -= 2
                    self.blocks[3].x -= 1
                    self.blocks[3].y += 1
                    self.rotation = 0
            elif self.type == 'z':
                if self.rotation == 0:
                    self.blocks[0].x += 1
                    self.blocks[0].y += 1
                    self.blocks[2].x += 1
                    self.blocks[2].y -= 1
                    self.blocks[3].y -= 2
                    self.rotation = 1
                else:
                    self.blocks[0].x -= 1
                    self.blocks[0].y -= 1
                    self.blocks[2].x -= 1
                    self.blocks[2].y += 1
                    self.blocks[3].y += 2
                    self.rotation = 0
            elif self.type == 'l':
                if self.rotation == 0:
                    self.blocks[0].x += 1
                    self.blocks[0].y -= 1
                    self.blocks[2].x -= 1
                    self.blocks[2].y += 1
                    self.blocks[3].y -= 2
                    self.rotation = 1
                elif self.rotation == 1:
                    self.blocks[0].x += 1
                    self.blocks[0].y += 1
                    self.blocks[2].x -= 1
                    self.blocks[2].y -= 1
                    self.blocks[3].x += 2
                    self.rotation = 2
                elif self.rotation == 2:
                    self.blocks[0].x -= 1
                    self.blocks[0].y += 1
                    self.blocks[2].x += 1
                    self.blocks[2].y -= 1
                    self.blocks[3].y += 2
                    self.rotation = 3
                else:
                    self.blocks[0].x -= 1
                    self.blocks[0].y -= 1
                    self.blocks[2].x += 1
                    self.blocks[2].y += 1
                    self.blocks[3].x -= 2
                    self.rotation = 0
            elif self.type == 'j':
                if self.rotation == 0:
                    self.blocks[0].x += 1
                    self.blocks[0].y -= 1
                    self.blocks[2].x -= 1
                    self.blocks[2].y += 1
                    self.blocks[3].x -= 2
                    self.rotation = 1
                elif self.rotation == 1:
                    self.blocks[0].x += 1
                    self.blocks[0].y += 1
                    self.blocks[2].x -= 1
                    self.blocks[2].y -= 1
                    self.blocks[3].y -= 2
                    self.rotation = 2
                elif self.rotation == 2:
                    self.blocks[0].x -= 1
                    self.blocks[0].y += 1
                    self.blocks[2].x += 1
                    self.blocks[2].y -= 1
                    self.blocks[3].x += 2
                    self.rotation = 3
                else:
                    self.blocks[0].x -= 1
                    self.blocks[0].y -= 1
                    self.blocks[2].x += 1
                    self.blocks[2].y += 1
                    self.blocks[3].y += 2
                    self.rotation = 0
            elif self.type == 't':
                if self.rotation == 0:
                    self.blocks[0].x += 1
                    self.blocks[0].y -= 1
                    self.blocks[2].x -= 1
                    self.blocks[2].y += 1
                    self.blocks[3].x -= 1
                    self.blocks[3].y -= 1
                    self.rotation = 1
                elif self.rotation == 1:
                    self.blocks[0].x += 1
                    self.blocks[0].y += 1
                    self.blocks[2].x -= 1
                    self.blocks[2].y -= 1
                    self.blocks[3].x += 1
                    self.blocks[3].y -= 1
                    self.rotation = 2
                elif self.rotation == 2:
                    self.blocks[0].x -= 1
                    self.blocks[0].y += 1
                    self.blocks[2].x += 1
                    self.blocks[2].y -= 1
                    self.blocks[3].x += 1
                    self.blocks[3].y += 1
                    self.rotation = 3
                else:
                    self.blocks[0].x -= 1
                    self.blocks[0].y -= 1
                    self.blocks[2].x += 1
                    self.blocks[2].y += 1
                    self.blocks[3].x -= 1
                    self.blocks[3].y += 1
                    self.rotation = 0

minos, bag, next_minos = get_mino(minos, bag)
while True:
    display.fill((0, 0, 0))

    draw_grid()

    level = int(score/10)+1
    timer_max = 20-level*2
    if fast_fall:
        timer_max /= 4
    if timer_max < 1:
        timer_max = 1

    draw_text('Lines {}'.format(score), font, (255, 255, 255), display, 210, 300)
    draw_text('Level {}'.format(level), font, (255, 255, 255), display, 210, 330)
    if last_score > 0:
        draw_text('Last score {}'.format(last_score), font, (255, 255, 255), display, 210, 360)

    for mino in next_minos:
        for block in mino.blocks:
            block.draw()

    if update_timer > 0:
        update_timer -= 1
    else:
        update_timer = timer_max
        for mino in minos:
            for block in mino.blocks:
                block.update(block_list)

    for i, mino in sorted(enumerate(minos), reverse=True):
        mino.update(direction, block_list)
        if mino.des:
            minos.pop(i)
            minos, bag, next_minos = get_mino(minos, bag)

        for block in mino.blocks:
            block.draw()

    temp_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for block in block_list:
        if block.active:
            block.active = False
        block.draw()
        if block.y < 0:
            last_score = score
            score = 0
            level = 1
            block_list = []
            break
        if block.y >= 0 and block.y <=19:
            temp_counter[block.y] += 1
    for inc, ind in enumerate(temp_counter):
        if ind >= 10:
            score += 1
            for i, block in sorted(enumerate(block_list), reverse=True):
                if block.y == inc:
                    block_list.pop(i)
    
    temp_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for block in block_list:
        if block.y >= 0 and block.y <=19:
            temp_counter[block.y] += 1
    for inc, ind in enumerate(temp_counter):
        if ind == 0:
            for i in sorted(range(0, inc), reverse=True):
                for block in block_list:
                    if block.y == i:
                        block.y += 1

    direction = ''
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for mino in minos:
                    mino.toggle_active_blocks()
        if event.type == KEYDOWN:
            if event.key == K_a:
                direction = 'left'
            if event.key == K_d:
                direction = 'right'
            if event.key == K_s:
                fast_fall = True
                update_timer = 0
            if event.key == K_w:
                for mino in minos:
                    mino.rotate(block_list)
        if event.type == KEYUP:
            if event.key == K_s:
                fast_fall = False
                timer_max = 20

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    mainClock.tick(60)
