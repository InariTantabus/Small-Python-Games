import pygame, sys, os, random, math

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Flappy Bird')

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 300))
#----------------Setup pygame/window----------------#

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def game():
    click = False
    scroll = 0
    pipes = []
    start = False
    pipe_timer = 0
    score_timer = 15
    score = 0
    font = pygame.font.SysFont(None, 20)

    class Bird:
        def __init__(self):
            self.x = 50
            self.y = 150
            self.vel = 0
        
        def draw(self):
            pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), 8)
        
        def update(self):
            self.vel += 0.2
            self.y += self.vel

        def rect(self):
            temp_di = math.sqrt(128)
            return pygame.Rect(self.x-temp_di/2, self.y-temp_di/2, temp_di, temp_di)

    class Pipe:
        def __init__(self, x):
            self.x = x
            self.y = 0
            self.hole = random.randint(1, 6)
        
        def draw(self, scroll):
            temp_rects = self.rect(scroll)
            for rect in temp_rects:
                pygame.draw.rect(display, (0, 255, 0), rect)

        def rect(self, scroll):
            temp_rects = []
            temp_rects.append(pygame.Rect(self.x-scroll, 0, 30, self.hole*30))
            temp_rects.append(pygame.Rect(self.x-scroll, self.hole*30+90, 30, 300))
            return temp_rects

    player = Bird()

    while True:
        display.fill((40, 120, 240))

        if start:
            scroll += 1
            player.update()

            if score_timer <= 0:
                if scroll > 150:
                    score += 1
                score_timer = 120
            else:
                score_timer -= 1


            if pipe_timer <= 0:
                pipes.append(Pipe(300+scroll))
                pipe_timer = 120
            else:
                pipe_timer -= 1

        if player.y-15 > 300:
            death_screen(score)

        for i, pipe in sorted(enumerate(pipes), reverse=True):
            pipe.draw(scroll)

            if pipe.x+30-scroll < 0:
                pipes.pop(i)

            temp_rects = pipe.rect(scroll)
            for rect in temp_rects:
                if rect.colliderect(player.rect()):
                    death_screen(score)

        player.draw()

        draw_text('{}'.format(score), font, (0, 0, 0), display, 15, 15)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if not start:
                        start = True
                    player.vel = -5

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

def death_screen(score):
    font = pygame.font.SysFont(None, 20)
    timer = 20

    running = True
    while running:
        display.fill((0, 0, 0))
        if timer > 0:
            timer -= 1 

        draw_text('You Died', font, (255, 255, 255), display, 120, 50)
        draw_text('You had {} points'.format(score), font, (255, 255, 255), display, 95, 70)
        draw_text('Press any key to try again', font, (255, 255, 255), display, 74, 100)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if timer == 0:
                    game()

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)
    game()

game()