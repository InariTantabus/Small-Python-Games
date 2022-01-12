import pygame, sys, os, random, math, itertools

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Asteroids Game')

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
    font = pygame.font.SysFont(None, 20)
    player_pos = (150, 150)
    player_rot = 0
    player_points = []
    move = False
    turn = [False, False]
    bullets = []
    shoot_timer = 0
    asteroids = []
    asteroid_spawn_timer = 20
    add_asteroid = []
    score = 0

    colors = itertools.cycle(['black', 'green', 'blue', 'purple', 'pink', 'red', 'orange']) ##

    base_color = next(colors)
    next_color = next(colors)
    current_color = 'black'

    step = 1

    def find_player_points(pos, rot):
        points = []

        dist = 5
        points.append((pos[0]+dist*math.cos(rot), pos[1]-dist*math.sin(rot)))
        
        dist = math.hypot(155-150, 155-150) ## sqrt(50)
        angle = (rot+math.atan2(155-150, 155-150))%(2*math.pi)
        points.append((pos[0]-dist*math.cos(angle), pos[1]+dist*math.sin(angle)))

        dist = -2.5
        points.append((pos[0]+dist*math.cos((rot)%(2*math.pi)), pos[1]-dist*math.sin(rot)))

        dist = math.hypot(155-150, 155-150)
        angle = (rot+math.atan2(155-150, 145-150))%(2*math.pi)
        points.append((pos[0]+dist*math.cos(angle), pos[1]-dist*math.sin(angle)))

        return points

    class Bullet:
        def __init__(self, pos, angle):
            self.x = pos[0]
            self.y = pos[1]
            self.angle = angle
            self.timer = 2*60
        
        def draw(self):
            pygame.draw.line(display, (255, 0, 0), (self.x, self.y), (self.x+10*math.cos(self.angle), self.y+10*math.sin(self.angle)))
        
        def update(self):
            self.x += 8*math.cos(self.angle)
            self.y += 8*math.sin(self.angle)

    class Asteroid:
        def __init__(self, pos=(0, 0), size=0, edge=True):
            if edge:
                side = random.randint(0, 3)
                if side == 0:   
                    self.x = random.randint(0, 300)
                    self.y = -12
                elif side == 1:
                    self.x = 312
                    self.y = random.randint(0, 300)
                    self.angle = random.randint(90, 270)*math.pi/180
                elif side == 2:
                    self.x = random.randint(0, 300)
                    self.y = 312
                    self.angle = random.randint(0, 180)*math.pi/180
                else:
                    self.x = -12
                    self.y = random.randint(0, 300)
                    self.angle = (random.randint(270, 449)%360)*math.pi/180
                temp = (random.randint(50, 250), random.randint(50, 250))
                self.angle = math.atan2(temp[1]-self.y, temp[0]-self.x)
                self.size = random.randint(1, 3)
                self.speed_var = 1
            else:
                self.x = pos[0]
                self.y = pos[1]
                self.size = size-1
                temp = (random.randint(50, 250), random.randint(50, 250))
                self.angle = math.atan2(temp[1]-self.y, temp[0]-self.x)
                self.speed_var = 3
            self.spawn_cooldown = 20*self.size
        
        def draw(self):
            pygame.draw.circle(display, (255, 255, 255), (self.x, self.y), self.size*3+2)
            pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), self.size*3)
        
        def update(self):
            self.x += abs((self.size-4)/2/self.speed_var)*math.cos(self.angle)
            self.y += abs((self.size-4)/2/self.speed_var)*math.sin(self.angle)
            if self.spawn_cooldown > 0:
                self.spawn_cooldown -= 1
            if self.spawn_cooldown == 0:
                self.x %= 300
                self.y %= 300

    running = True
    while running:
        if score > 1500:
            display.fill(current_color)
            step += 1
            if step < 120:
                current_color = [x + (((y-x)/120)*step) for x, y in zip(pygame.color.Color(base_color), pygame.color.Color(next_color))] ##
            else:
                step = 1
                base_color = next_color
                next_color = next(colors)
        else:
            display.fill((0, 0, 0))

        if asteroid_spawn_timer > 0:
            asteroid_spawn_timer -= 1
        else:
            asteroids.append(Asteroid())
            asteroid_spawn_timer = random.randint(30, 120)
            
        if shoot_timer > 0:
            shoot_timer -= 1

        if turn[0]:
            player_rot -= (6*math.pi/180)
        if turn[1]:
            player_rot += (6*math.pi/180)
        if move:
            player_pos = ((player_pos[0]+2*math.cos(player_rot))%300, (player_pos[1]-2*math.sin(player_rot))%300)

        player_points = find_player_points(player_pos, player_rot)
        pygame.draw.polygon(display, (255, 255, 255), player_points, 3)
        pygame.draw.polygon(display, (0, 0, 0), player_points)

        for i, bullet in sorted(enumerate(bullets), reverse=True):
            bullet.update()
        
            for v, asteroid in sorted(enumerate(asteroids), reverse=True):
                temp_point = (asteroid.size*3+2)**2 - ((asteroid.x-bullet.x)**2 + (asteroid.y-bullet.y)**2)
                temp_point_2 = (asteroid.size*3+2)**2 - ((asteroid.x-bullet.x+10*math.cos(bullet.angle))**2 + (asteroid.y-bullet.y+10*math.cos(bullet.angle))**2)
                if temp_point >= 0 or temp_point_2 >= 0:
                    score += 25*asteroid.size
                    if asteroid.size > 1:
                        temp_random = random.randint(2, 3)
                        while temp_random > 0:
                            temp_random -= 1
                            add_asteroid.append([(asteroid.x, asteroid.y), asteroid.size])
                    asteroids.pop(v)
                    bullets.pop(i)
                    break

            if bullet.timer > 0:
                bullet.timer -= 1
            else:
                bullets.pop(i)
            if bullet.x < -30 or bullet.x > 330 or bullet.y < -30 or bullet.y > 330:
                bullets.pop(i)

            bullet.draw()
        
        while len(add_asteroid) > 0:
            asteroids.append(Asteroid(add_asteroid[0][0], add_asteroid[0][1], False))
            add_asteroid.pop(0)

        for asteroid in asteroids:
            asteroid.update()
            asteroid.draw()
            for point in player_points:
                temp_point = (asteroid.size*3+2)**2 - ((asteroid.x-point[0])**2 + (asteroid.y-point[1])**2)
                if temp_point >= 0:
                    running = False

        draw_text('{}'.format(score), font, (200, 200, 200), display, 5, 5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_w:
                    move = True
                if event.key == K_a:
                    turn[1] = True
                if event.key == K_d:
                    turn[0] = True
                if event.key == K_SPACE:
                    if shoot_timer == 0:
                        shoot_timer = 10
                        bullets.append(Bullet(player_pos, -player_rot))
            if event.type == KEYUP:
                if event.key == K_w:
                    move = False
                if event.key == K_a:
                    turn[1] = False
                if event.key == K_d:
                    turn[0] = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)
    death_menu(score)

def death_menu(score):
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