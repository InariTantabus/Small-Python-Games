import pygame, sys, os, random, math

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Minesweeper')

WINDOW_SIZE = (1200, 800)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((600, 400))
#----------------Setup pygame/window----------------#

click = False
rclick = False
font = pygame.font.SysFont(None, 20)
bomb_count = 0
total_bombs = 75
new_game = False
win = False

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def check_cells(c, mouse_pos, new_game):
    for cell in c:
        if c[cell].rect().collidepoint(mouse_pos) and not c[cell].clicked:
            c[cell].toggle()

            if c[cell].bomb:
                new_game = True
                for tile in c:
                    if c[tile].bomb and not c[tile].clicked:
                        c[tile].toggle()
            else:
                if c[cell].value == 0:
                    check_list = [cell]
                    checked_list = []
                    to_add = []
                    running = True
                    while running:
                        if to_add:
                            for i, add in sorted(enumerate(to_add), reverse=True):
                                check_list.append(add)
                                to_add.pop(i)
                        
                        if not check_list:
                            running = False

                        for t, check in sorted(enumerate(check_list), reverse=True):
                            for i in range(3):
                                for v in range(3):
                                    test = '{}:{}'.format(c[check].x-1+i, c[check].y-1+v)
                                    if test in c and test not in checked_list and not c[test].bomb:
                                        if c[test].value == 0:
                                            to_add.append(test)
                                            checked_list.append(test)
                                        c[test].toggle()
                            checked_list.append(check)
                            check_list.pop(t)
    return new_game

def reset_game(c):
    c = {}
    new_game = False
    bomb_count = 0
    win = False

    for i in range(32): # generating grid
        for v in range(16):
            c["{}:{}".format(i, v)] = Cell((i, v))

    temp_c = list(c)
    for i in range(total_bombs): # adding bombs
        temp_rand = random.randint(0, len(temp_c)-1)
        c[temp_c[temp_rand]].bomb = True
        temp_c.pop(temp_rand)

    for cell in c: # determining values
        for i in range(3):
            for v in range(3):
                if not c[cell].bomb:
                    test = '{}:{}'.format(c[cell].x-1+i, c[cell].y-1+v)
                    if test in c:
                        if c[test].bomb:
                            c[cell].value += 1
    
    return c, new_game, bomb_count, win

def check_win(c):
    win = True
    for cell in c:
        if not c[cell].bomb:
            if not c[cell].clicked:
                win = False
                break
    return win

class Cell:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.locx = pos[0]*18 + 12
        self.locy = pos[1]*18 + 100
        self.bomb = False
        self.clicked = False
        self.value = 0
        self.hover = False
        self.flagged = False
    
    def rect(self):
        return pygame.Rect(self.locx+1, self.locy+1, 16, 16)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(self.locx, self.locy, 18, 18)) 
        if self.clicked:
            pygame.draw.rect(surface, (100, 100, 100), self.rect())
            if self.value != 0:
                draw_text('{}'.format(self.value), font, (255, 255, 255), surface, self.locx+6, self.locy+2)
            if self.bomb:
                if not self.flagged:
                    pygame.draw.rect(surface, (100, 0, 0), self.rect())
                else:
                    pygame.draw.rect(surface, (0, 100, 0), self.rect())
                draw_text('B', font, (255, 255, 255), surface, self.locx+6, self.locy+2)
        else:
            if self.hover:
                pygame.draw.rect(surface, (150, 150, 150), self.rect())
            else:
                pygame.draw.rect(surface, (200, 200, 200), self.rect())
            if self.flagged:
                draw_text('F', font, (200, 0, 0), surface, self.locx+6, self.locy+2)
    
    def toggle(self):
        self.clicked = True
    
    def update(self):
        self.hover = False

c = {}
c, new_game, bomb_count, win = reset_game(c)

while True: # game loop
    display.fill((50, 50, 50))
    mx, my = pygame.mouse.get_pos()
    mx /= 2
    my /= 2

    if not win:
        win = check_win(c)

    draw_text('Bombs: {}/{}'.format(bomb_count, total_bombs), font, (200, 200, 200), display, 30, 30)
    if new_game:
        draw_text('You Lose!'.format(bomb_count), font, (200, 0, 0), display, 280, 30)
        draw_text('Click to try again'.format(bomb_count), font, (200, 200, 200), display, 260, 45)
    if win:
        draw_text('You Win!'.format(bomb_count), font, (0, 200, 0), display, 282, 30)
        draw_text('Click to try again'.format(bomb_count), font, (200, 200, 200), display, 260, 45)

    temp_count = 0
    for cell in c:
        c[cell].draw(display)
        c[cell].update()
        if c[cell].rect().collidepoint(mx, my) and not c[cell].clicked:
            c[cell].hover = True

            if rclick:
                if not c[cell].flagged:
                    bomb_count += 1
                else:
                    bomb_count -= 1
                c[cell].flagged = not c[cell].flagged

        if c[cell].bomb and c[cell].flagged:
            temp_count += 1
    
    if temp_count == total_bombs:
        win = True

    if click:
        new_game = check_cells(c, (mx, my), new_game)

    rclick = False
    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_r:
                c, new_game, bomb_count, win = reset_game(c)

        if not new_game and not win:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if event.button == 3:
                    rclick = True
        else:
            if event.type == MOUSEBUTTONDOWN:
                c, new_game, bomb_count, win = reset_game(c)

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    mainClock.tick(60)