import pygame, sys, os, random, math

#----------------Setup pygame/window----------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)
pygame.display.set_caption('Double click to close')
#----------------Setup pygame/window----------------#

explosion_sound = pygame.mixer.Sound('explosion.wav')
explosion_sound.set_volume(0.1)

pygame.mixer.music.load('8-bit.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.025)

running = True
close = 0
score = 0
font = pygame.font.SysFont(None, 20)
size = 1

def update_display_size(size, frame=NOFRAME):
    WINDOW_SIZE = (64 * size, 64 * size)
    screen = pygame.display.set_mode(WINDOW_SIZE, frame, 32)
    display = pygame.Surface((64, 64))

    return screen, display, WINDOW_SIZE

screen, display, WINDOW_SIZE = update_display_size(size)

def handle_close_check(close):
    if close >= 11:
        pygame.quit()
        sys.exit()
    if close > 0:
        close -= 1
    return close

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def game(close, size):
    score = 0
    running = True
    next_spawner_num = 0
    spawners = []
    particles = []
    enemies = []
    enemy_timer = 40
    moving = {'up': False, 'left': False, 'down': False, 'right': False}

    def handle_enemy_timer(enemy_timer, enemies, spawners, next_spawner_num):
        temp = next_spawner_num
        if enemy_timer > 0:
            enemy_timer -= 1
        if enemy_timer == 0:
            enemies.append(Enemy(spawners[next_spawner_num]))
            temp = next_spawner(spawners)
            enemy_timer = 40
        
        return enemy_timer, enemies, temp

    def next_spawner(spawners):
        temp = random.randint(0, len(spawners) - 1)
        return temp

    def create_spawners(spawners):
        for i in range(8):
            spawners.append((i*8, -1))
        for i in range(8):
            spawners.append((-1, i*8))
        for i in range(8):
            spawners.append((i*8, 65))
        for i in range(8):
            spawners.append((65, i*8))

        return spawners

    def enemy_functions(enemies, player, score, particles):
        remove = []
        for i, enemy in sorted(enumerate(enemies), reverse=True):
            enemy.draw(display)
            enemy.move((player.x, player.y))
            for v, enemy2 in sorted(enumerate(enemies), reverse=True):
                if enemy2.pos != enemy.pos:
                    if enemy.rect().colliderect(enemy2.rect()):
                        if enemy.size > enemy2.size:
                            enemy2.size -= 1
                            remove.append(i)
                            particles.append(Particle(enemy.pos))
                            if enemy2.size < 2:
                                remove.append(v)
                        elif enemy.size < enemy2.size:
                            enemy.size -= 1
                            remove.append(v)
                            particles.append(Particle(enemy.pos))
                            if enemy.size < 2:
                                remove.append(i)
                        else:
                            particles.append(Particle(enemy.pos))
                            remove.append(i)
                            remove.append(v)
        if remove:
            for i in range(0, len(remove) - 1):
                enemies.pop(max(remove))
                remove.pop(remove.index(max(remove)))
                score += 1
                explosion_sound.play()
        return enemies, score, particles

    def calculat_new_xy(old_xy,speed,angle_in_radians): ##
        new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
        new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
        return (new_x, new_y)

    def circle_surf(radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    class Enemy:
        def __init__(self, start):
            self.size = random.randint(2, 4)
            self.pos = start
            self.speed = (abs(self.size / 4 * -1) + 1.25) / (self.size * 1.2)

        def rect(self):
            return pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        
        def draw(self, surf):
            pygame.draw.rect(surf, (0, 255, 0), self.rect())

        def move(self, target):
            self.pos = calculat_new_xy(self.pos, self.speed, math.atan2(target[1] - self.pos[1], target[0] - self.pos[0]))

    class Player:
        def __init__(self):
            self.x = 30
            self.y = 30
            self.size = 4
        
        def rect(self, size=2):
            return pygame.Rect(self.x + 1, self.y + 1, size, size)

        def draw(self, surf):
            pygame.draw.rect(surf, (255, 0, 255), self.rect(4))
        
        def move(self, direction):
            if direction['up'] and self.y > -1:
                self.y -= 1
            if direction['left'] and self.x > -1:
                self.x -= 1
            if direction['down'] and self.y < 59:
                self.y += 1
            if direction['right'] and self.x < 59:
                self.x += 1
        
        def collide_check(self, enemies, score):
            running = True
            for i, enemy in sorted(enumerate(enemies), reverse=True):
                if self.rect().colliderect(enemy.rect()):
                    running = False
            return running

    class Particle:
        def __init__(self, loc):
            self.x = loc[0]
            self.y = loc[1]
            self.timer = 6
        
        def update(self, score):
            temp = 255 - (score)
            if temp < 10:
                temp = 10
            pygame.draw.circle(display, (temp, temp, temp), (int(self.x), int(self.y)), (int(self.timer)))
            self.timer -= 1

    player = Player()
    spawners = create_spawners(spawners)
    screen, display, WINDOW_SIZE = update_display_size(size)

    while running:
        temp_color = score
        if temp_color > 200:
            temp_color = 200
        display.fill((temp_color, temp_color, temp_color))
        running = player.collide_check(enemies, score)
        close = handle_close_check(close)

        for particle in particles:
            particle.update(score)
        enemy_timer, enemies, next_spawner_num = handle_enemy_timer(enemy_timer, enemies, spawners, next_spawner_num)
        enemies, score, particles = enemy_functions(enemies, player, score, particles)
        player.draw(display)
        player.move(moving)
        for i in range(0, len(spawners) - 1):
            if next_spawner_num == i:
                display.blit(circle_surf(8, (100, 0, 0)), (int(spawners[i][0] - 8), int(spawners[i][1] - 8)), special_flags=BLEND_RGB_ADD)
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    close += 10
            if event.type == KEYDOWN:
                if event.key == K_w:
                    moving['up'] = True
                if event.key == K_a:
                    moving['left'] = True
                if event.key == K_s:
                    moving['down'] = True
                if event.key == K_d:
                    moving['right'] = True
            if event.type == KEYUP:
                if event.key == K_w:
                    moving['up'] = False
                if event.key == K_a:
                    moving['left'] = False
                if event.key == K_s:
                    moving['down'] = False
                if event.key == K_d:
                    moving['right'] = False

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)
    return score

def death_screen(close, score, size):
    change = False
    running = True
    screen, display, WINDOW_SIZE = update_display_size(size, 0)
    while running:
        if change:
            screen, display, WINDOW_SIZE = update_display_size(size, 0)
        temp_color = score
        if temp_color > 200:
            temp_color = 200
        display.fill((temp_color, temp_color, temp_color))
        close = handle_close_check(close)

        draw_text('{}'.format(score), font, (255, 0, 0), display, 24, 16)
        draw_text('Space', font, (255, 255, 255), display, 14, 30)
        draw_text('to restart', font, (255, 255, 255), display, 5, 44)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    close += 10
                if event.button ==  4:
                    if size < 5:
                        size += 1
                        change = True
                if event.button ==  5:
                    if size > 1:
                        size -= 1
                        change = True
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    score = game(close, size)

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)
    return size

score = game(close, size)
size = death_screen(close, score, size)