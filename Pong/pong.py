import pygame, sys, os, random, math

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Pong')

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
    top_block = pygame.Rect(0, 0, 300, 60)
    bot_block = pygame.Rect(0, 240, 300, 60)
    pi = math.pi
    score = 0
    font = pygame.font.SysFont(None, 20)

    class Ball:
        def __init__(self):
            self.x = 150
            self.y = 150
            temp_target = (random.randint(200, 280), random.randint(0, 300))
            self.angle = math.atan2(temp_target[1]-self.y, temp_target[0]-self.x)
            if (self.angle+0.4)%(2*pi) < 0.8:
                temp_angle = random.randint(0, 1)
                self.angle = (temp_angle*2-1)*0.4 + (temp_angle*2-1)*(random.randint(0, 5)/10)
            self.radius = 4
            self.speed = 2

        def draw(self):
            pygame.draw.circle(display, (255, 255, 255), (self.x, self.y), self.radius)
        
        def rect(self):
            return pygame.Rect(self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2)
        
        def get_new_angle(self, floof=True): # floof = floor/roof
            if floof:
                self.angle = (2*pi-self.angle)%(2*pi)
            else:
                self.angle = (pi-self.angle)%(2*pi)

        def update(self, score):
            if self.y+self.speed*math.sin(self.angle) < 60+self.radius or self.y+self.speed*math.sin(self.angle) > 240-self.radius:
                self.get_new_angle()
                self.y += self.speed*math.sin(self.angle)
            self.x += self.speed*math.cos(self.angle)
            if self.rect().colliderect(cpu.rect()) or self.rect().colliderect(player.rect()):
                self.get_new_angle(False)
                self.speed *= 1.1
                self.x += self.speed*math.cos(self.angle)
            self.y += self.speed*math.sin(self.angle)
            if self.rect().colliderect(cpu.rect()) or self.rect().colliderect(player.rect()):
                self.get_new_angle()
                self.y += self.speed*math.sin(self.angle)
            return score

    class Paddle:
        def __init__(self, x):
            self.x = x
            self.y = 120
            self.moving = {'up': False, 'down': False}
        
        def draw(self):
            pygame.draw.rect(display, (255, 255, 255), self.rect())
        
        def rect(self):
            return pygame.Rect(self.x, self.y, 7, 60)
        
        def move(self):
            if self.moving['up']:
                if self.y > 60:
                    self.y -= 2
            if self.moving['down']:
                if self.y < 180:
                    self.y += 2
        
        def auto(self):
            if self.y+30 > ball.y:
                self.moving['up'] = True
            else:
                self.moving['up'] = False
            if self.y+30 < ball.y:
                self.moving['down'] = True
            else:
                self.moving['down'] = False
            self.move()

    balls = [Ball()]
    player = Paddle(20)
    cpu = Paddle(273)

    running = True
    while running:
        display.fill((0, 0, 0))

        pygame.draw.rect(display, (50, 50, 50), top_block)
        pygame.draw.rect(display, (50, 50, 50), bot_block)
        draw_text('{}'.format(score), font, (255, 255, 255), display, 15, 15)

        for i, ball in enumerate(balls):
            score = ball.update(score)
            ball.draw()
            if ball.x <= 0:
                death_screen(score)
            if ball.x >= 300:
                score += 1
                balls.pop(i)
                balls.append(Ball())

        cpu.draw()
        cpu.auto()

        player.move()
        player.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
            if event.type == KEYDOWN:
                if event.key in [K_w, K_UP]:
                    player.moving['up'] = True
                if event.key in [K_s, K_DOWN]:
                    player.moving['down'] = True
            if event.type == KEYUP:
                if event.key in [K_w, K_UP]:
                    player.moving['up'] = False
                if event.key in [K_s, K_DOWN]:
                    player.moving['down'] = False
                    
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

def death_screen(score):
    top_block = pygame.Rect(0, 0, 300, 60)
    bot_block = pygame.Rect(0, 240, 300, 60)
    font = pygame.font.SysFont(None, 20)
    timer = 20

    running = True
    while running:
        display.fill((0, 0, 0))
        if timer > 0:
            timer -= 1 
        
        pygame.draw.rect(display, (50, 50, 50), top_block)
        pygame.draw.rect(display, (50, 50, 50), bot_block)

        draw_text('You Died', font, (255, 255, 255), display, 120, 100)
        if score == 1:
            draw_text('You had {} point'.format(score), font, (255, 255, 255), display, 98, 120)
        else:
            draw_text('You had {} points'.format(score), font, (255, 255, 255), display, 95, 120)
        draw_text('Press any key to try again', font, (255, 255, 255), display, 74, 150)
        
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