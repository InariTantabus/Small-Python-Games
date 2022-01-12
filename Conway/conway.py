import pygame, sys, os, random, math

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Game')

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((100, 100))
#----------------Setup pygame/window----------------#

click = False

class Cell(object):
    def __init__(self, pos):
        self.pos = pos
        self.alive = False
        self.color = (0, 0, 0)
        self.changed = [False, False]

    def draw(self):
        pygame.draw.circle(display, self.color, self.pos, 1)
    
    def update(self, cells, change=False):
        test = 0
        for i in range(3):
            for v in range(3):
                name = '{}:{}'.format(i+self.pos[0]-1, v+self.pos[1]-1)
                if name in cells and name != '{}:{}'.format(self.pos[0], self.pos[1]):
                    if cells[name].alive:
                        test += 1
        
        if test == 2 and self.alive:
            pass
        elif test == 3:
            self.changed = [True, True]
        else:
            self.changed = [True, False]
    
    def activate(self):
        if self.alive != self.changed[1]:
            self.change(True)

    def change(self, change=False):
        if change:
            self.alive = not self.alive
        if self.alive:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)

cells = {}
for i in range(100):
    for v in range(100):
        cells['{}:{}'.format(i, v)] = Cell((i, v))

active = False
while True:
    display.fill((20, 20, 20))
    mx, my = pygame.mouse.get_pos()
    mx = min(99, (int(mx/8) + 1))
    my = min(99, (int(my/8) + 1))

    for cell in cells:
        cells[cell].draw()

        if active:
            cells[cell].update(cells)
    
    if active:
        for cell in cells:
            if cells[cell].changed[0]:
                cells[cell].activate()
    
    if click and not active:
        cells['{}:{}'.format(mx, my)].change(True)

    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == KEYDOWN:
            active = not active

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    mainClock.tick(60)