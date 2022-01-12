import pygame, sys, os, random, math

#-----------------------------------#
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Grid Cannon')

WINDOW_SIZE = (800, 800)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

display = pygame.Surface((400, 400))
#-----------------------------------#

click = False
right_click = False
mouse = [0, 0]
score = 0
tiles = []
tile_size = 80
royals = []
current_card = 0
ordered_deck = []
board = [[[], [], []], [[], [], [], [], []], [[], [], [], [], []], [[], [], [], [], []], [[], [], []]]
font = pygame.font.SysFont(None, 20)
item_color = (100, 20, 20)
armor_phase = [False, False]
royals_left = 12
check = [0, '']
check_list = []

def generate_cards():
    suits = ['C', 'S', 'H', 'D']
    current_suit = suits[0]
    cards = []
    for v in range(0, 4):
        for i in range(0, 13):
            cards.append([current_suit, (i + 1)])
        if (v + 1) < 4:
            current_suit = suits[v + 1]
    cards.append(['J', 0])
    cards.append(['J', 0])
    return cards

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def generate_board(active_deck, board):
    temp = 0
    temp_list = []
    checking = True
    deck = active_deck.copy()

    for row in range(0, len(board)):
        for column in range(0, len(board[row])):
            if row == 1 or row == 3:
                if column == 1 or column == 2 or column == 3:
                    checking = True
                    while checking:
                        temp = random.randint(0, (len(deck) - 1))
                        if deck[temp][1] > 10:
                            temp_list.append(deck[temp])
                            deck.pop(temp)
                        else:
                            checking = False
                    board[row][column] = deck[temp]
                    deck.pop(temp)
            elif row == 2:
                if column == 1 or column == 3:
                    checking = True
                    while checking:
                        temp = random.randint(0, (len(deck) - 1))
                        if deck[temp][1] > 10:
                            temp_list.append(deck[temp])
                            deck.pop(temp)
                        else:
                            checking = False
                    board[row][column] = deck[temp]
                    deck.pop(temp)
    if len(temp_list) < 1:
        test = 0
        while test < 11:
            temp = random.randint(0, (len(deck) - 1))
            test = deck[temp][1]
        temp_list.append(deck[temp])
    return deck, board, temp_list

def generate_tiles():
    tiles = []

    for row in range(0, len(board)):
        if len(board[row]) < 5:
            board[row].append([])
            board[row].insert(0, [])
        for column in range(0, len(board[row])):
            tiles.append(Tile((column, row), board[row][column]))
    return tiles

def place_royals(input_list, board):
    blacklist = []
    royal_dict = {}
    for royal in range(0, len(input_list)):
        best = ['', 0, 'black']
        royal_color = 'black'
        if input_list[royal][0] in ['H', 'D']:
            royal_color = 'red'
        for item in tiles:
            if len(item.card) > 0 and item.slots > 0 and item.card not in blacklist:
                if best[0] in ['H', 'D']:
                    best[2] = 'red'
                if item.card[0] == input_list[royal][0]:
                    if best[0] != input_list[royal][0]:
                        best = [item.card[0], item.card[1], item.color]
                    elif item.card[1] > best[1]:
                        best = [item.card[0], item.card[1], item.color]
                elif item.color == royal_color:
                    if best[0] != input_list[royal][0]:
                        if best[2] != royal_color:
                            best = [item.card[0], item.card[1], item.color]
                        elif item.card[1] > best[1]:
                            best = [item.card[0], item.card[1], item.color]
                elif best[0] != input_list[royal][0]:
                    if best[2] != royal_color:
                        if item.card[1] > best[1]:
                            best = [item.card[0], item.card[1], item.color]
        for item in tiles:
            if item.card == [best[0], best[1]]:
                item.slots -= 1
                if item.slots < 1:
                    blacklist.append(item.card)
                royal_dict[royal] = [[best[0], best[1]], input_list[royal], royal_color]
    for card in royal_dict:
        for v, item in sorted(enumerate(tiles), reverse=True):
            item_loc = (item.x, item.y)
            if royal_dict[card][0] == item.card:
                if item_loc != (1, 1) and item_loc != (1, 3) and item_loc != (3, 1) and item_loc != (3, 3):
                    if item.y == 1:
                        for i in tiles:
                            if i.x == 2 and i.y == 0:
                                i.change(royal_dict[card][1])
                                break
                    elif item.y == 2:
                        if item.x == 1:
                            for i in tiles:
                                if i.x == 0 and i.y == 2:
                                    i.change(royal_dict[card][1])
                                    break
                        else:
                            for i in tiles:
                                if i.x == 4 and i.y == 2:
                                    i.change(royal_dict[card][1])
                                    break
                    elif item.y == 3:
                        for i in tiles:
                            if i.x == 2 and i.y == 4:
                                i.change(royal_dict[card][1])
                                break
                else:
                    temp_best = ['', 0, 'black']
                    if item_loc == (1, 1):
                        for i in tiles:
                            if i.x == 2 and i.y == 1:
                                temp_best = [i.card[0], i.card[1], i.color, (0, 1)]
                                break
                        for i in tiles:
                            if i.x == 1 and i.y == 2:
                                if i.card[0] == royal_dict[card][1][0]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        temp_best = [i.card[0], i.card[1], i.color, (1, 0)]
                                        break
                                    elif i.card[1] > temp_best[1]:
                                        temp_best = [i.card[0], i.card[1], i.color, (1, 0)]
                                        break
                                elif i.color == royal_dict[card][2]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        if temp_best[2] != royal_dict[card][2]:
                                            temp_best = [i.card[0], i.card[1], i.color, (1, 0)]
                                            break
                                        elif i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (1, 0)]
                                            break
                                elif temp_best[0] != royal_dict[card][1][0]:
                                    if temp_best[2] != royal_dict[card][2]:
                                        if i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (1, 0)]
                                            break
                        for i in tiles:
                            if i.x == 0 and i.y == 1:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (1, 0)]
                            elif i.x == 1 and i.y == 0:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (0, 1)]
                            if i.x == temp_best[3][0] and i.y == temp_best[3][1]:
                                i.change(royal_dict[card][1])
                                break
                    elif item_loc == (1, 3):
                        for i in tiles:
                            if i.x == 2 and i.y == 3:
                                temp_best = [i.card[0], i.card[1], i.color, (0, 3)]
                                break
                        for i in tiles:
                            if i.x == 1 and i.y == 2:
                                if i.card[0] == royal_dict[card][1][0]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        temp_best = [i.card[0], i.card[1], i.color, (1, 4)]
                                        break
                                    elif i.card[1] > temp_best[1]:
                                        temp_best = [i.card[0], i.card[1], i.color, (1, 4)]
                                        break
                                elif i.color == royal_dict[card][2]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        if temp_best[2] != royal_dict[card][2]:
                                            temp_best = [i.card[0], i.card[1], i.color, (1, 4)]
                                            break
                                        elif i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (1, 4)]
                                            break
                                elif temp_best[0] != royal_dict[card][1][0]:
                                    if temp_best[2] != royal_dict[card][2]:
                                        if i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (1, 4)]
                                            break
                        for i in tiles:
                            if i.x == 0 and i.y == 3:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (1, 4)]
                            elif i.x == 1 and i.y == 4:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (0, 3)]
                            if i.x == temp_best[3][0] and i.y == temp_best[3][1]:
                                i.change(royal_dict[card][1])
                                break
                    elif item_loc == (3, 1):
                        for i in tiles:
                            if i.x == 2 and i.y == 1:
                                temp_best = [i.card[0], i.card[1], i.color, (4, 1)]
                                break
                        for i in tiles:
                            if i.x == 3 and i.y == 2:
                                if i.card[0] == royal_dict[card][1][0]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        temp_best = [i.card[0], i.card[1], i.color, (3, 0)]
                                        break
                                    elif i.card[1] > temp_best[1]:
                                        temp_best = [i.card[0], i.card[1], i.color, (3, 0)]
                                        break
                                elif i.color == royal_dict[card][2]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        if temp_best[2] != royal_dict[card][2]:
                                            temp_best = [i.card[0], i.card[1], i.color, (3, 0)]
                                            break
                                        elif i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (3, 0)]
                                            break
                                elif temp_best[0] != royal_dict[card][1][0]:
                                    if temp_best[2] != royal_dict[card][2]:
                                        if i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (3, 0)]
                                            break
                        for i in tiles:
                            if i.x == 4 and i.y == 1:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (3, 0)]
                            elif i.x == 3 and i.y == 0:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (4, 1)]
                            if i.x == temp_best[3][0] and i.y == temp_best[3][1]:
                                i.change(royal_dict[card][1])
                                break
                    elif item_loc == (3, 3):
                        for i in tiles:
                            if i.x == 2 and i.y == 3:
                                temp_best = [i.card[0], i.card[1], i.color, (4, 3)]
                                break
                        for i in tiles:
                            if i.x == 3 and i.y == 2:
                                if i.card[0] == royal_dict[card][1][0]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        temp_best = [i.card[0], i.card[1], i.color, (3, 4)]
                                        break
                                    elif i.card[1] > temp_best[1]:
                                        temp_best = [i.card[0], i.card[1], i.color, (3, 4)]
                                        break
                                elif i.color == royal_dict[card][2]:
                                    if temp_best[0] != royal_dict[card][1][0]:
                                        if temp_best[2] != royal_dict[card][2]:
                                            temp_best = [i.card[0], i.card[1], i.color, (3, 4)]
                                            break
                                        elif i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (3, 4)]
                                            break
                                elif temp_best[0] != royal_dict[card][1][0]:
                                    if temp_best[2] != royal_dict[card][2]:
                                        if i.card[1] > temp_best[1]:
                                            temp_best = [i.card[0], i.card[1], i.color, (3, 4)]
                                            break
                        for i in tiles:
                            if i.x == 4 and i.y == 3:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (3, 4)]
                            elif i.x == 3 and i.y == 4:
                                if len(i.card) > 0:
                                    temp_best = [i.card[0], i.card[1], i.color, (4, 3)]
                            if i.x == temp_best[3][0] and i.y == temp_best[3][1]:
                                i.change(royal_dict[card][1])
                                break
    return tiles

def get_new_card(card_list, board):
    if len(card_list) != 0:
        new_card = card_list[0]
        card_list.pop(0)
        for i in board:
            if i.x == 4 and i.y == 4:
                i.change(new_card)
    else:
        print('You lose, you had {} points'.format(score))
        pygame.quit()
        sys.exit()
    return new_card, board

def get_random_deck(card_list):
    random_list = []
    copy_list = card_list.copy()
    for i, card in sorted(enumerate(copy_list), reverse=True):
        temp = random.randint(0, (len(copy_list) - 1))
        random_list.append(copy_list[temp])
        copy_list.pop(temp)
    return random_list

def check_hit(board, loc):
    for item in board:
        if item.x == loc[0] and item.y == loc[1]:
            if loc in [(2, 1), (1, 2), (3, 2), (2, 3)]:
                check_list = [[(2, 4), (2, 3), (2, 2)], [(4, 2), (3, 2), (2, 2)], [(0, 2), (1, 2), (2, 2)], [(2, 0), (2, 1), (2, 2)]][[(2, 1), (1, 2), (3, 2), (2, 3)].index(loc)]
                for i in board:
                    if i.x == check_list[0][0] and i.x == check_list[0][1] and len(i.card) > 0:
                        check = [[(11 + i.armor), 'any'], [(12 + i.armor), 'color'], [(13 + i.armor), 'suit']][['J', 'Q', 'K'].index(item.card[0])]
                if check[1] == 'suit':
                    pass
                elif check[1] == 'color':
                    pass
                else:
                    pass
            elif loc in [(1, 1), (3, 1), (1, 3), (3, 3)]:
                pass

            # if loc == (1, 1):
            #     pass
            # if loc == (1, 2):
            #     for i in board:
            #         if i.x == 3 and i.x == 2 and len(i.card) > 0:
            #             check = [[(11 + i.armor), 'suit'], [(12 + i.armor), 'color'], [(13 + i.armor), 'any']][['J', 'Q', 'K'].index(item.card[0])]
            # if loc == (1, 3):
            #     pass
            # if loc == (2, 1):
            #     pass
            # if loc == (2, 3):
            #     pass
            # if loc == (3, 1):
            #     pass
            # if loc == (3, 2):
            #     pass
            # if loc == (3, 3):
            #     pass

class Tile:
    def __init__(self, loc, card):
        self.x = loc[0]
        self.y = loc[1]
        self.true_x = (loc[0] * tile_size)
        self.true_y = (loc[1] * tile_size)
        self.card = card
        self.card_list = [card]
        self.shown = False
        self.armor = 0
        self.value = 0
        if len(self.card) > 0:
            self.value = card[1]
            if self.value in [11, 12, 13]:
                self.value = ['J', 'Q', 'K'][(self.value - 11)]
        self.slots = 1
        if self.x in [1, 3] and self.y in [1, 3]:
            self.slots = 2
        self.color = 'black'
        if len(card) > 0:
            if card[0] in ['H', 'D']:
                self.color = 'red'
            if card[0] == 'J':
                self.color = ''

    def rect(self, size):
        return pygame.Rect(self.true_x, self.true_y, size, size)

    def change(self, card):
        if self.x in [1, 2, 3] and self.y in [1, 2, 3]:
            if card[1] in [0, 1]:
                for i, item in sorted(enumerate(self.card_list), reverse=True):
                    ordered_deck.append(self.card_list[((len(self.card_list) - 1) - i)])
                    self.card_list.pop(((len(self.card_list) - 1) - i))
            else:
                pass
            self.card_list.append(card)
        self.card = card
        if len(self.card) > 0:
            self.value = card[1]
            if self.value in [11, 12, 13]:
                self.value = ['J', 'Q', 'K'][(self.value - 11)]
    
    def toggle(self):
        if self.shown:
            self.shown = False
        else:
            self.shown = True

active_deck = generate_cards()
active_deck, board, royals = generate_board(active_deck, board)
tiles = generate_tiles()
tiles = place_royals(royals, tiles)
current_card, tiles = get_new_card(active_deck, tiles)
ordered_deck = get_random_deck(active_deck)

#-----------------------------------------------------------------------------------------------#
while True:
    display.fill((0, 0, 0))

    mouse[0], mouse[1] = pygame.mouse.get_pos()
    mouse[0] = (mouse[0] / 2)
    mouse[1] = (mouse[1] / 2)

    if not armor_phase[0]:
        armor_phase = [False, False]
    for i in tiles:
        loc = (i.x, i.y)
        if len(i.card) > 0 and loc != (4, 4):
            if current_card[1] >= i.card[1] or current_card[1] in [0, 1]:
                armor_phase = [False, True]
    if not armor_phase[1]:
        armor_phase = [True, True]
        print('armor')

    royals_left = 12
    for item in tiles:
        if item.shown:
            royals_left -= 1
        if royals_left == 0:
            print('You win! You lost {} points'.format(score))
            pygame.quit()
            sys.exit()
        loc = (item.x, item.y)
        pygame.draw.rect(display, (80, 80, 80), item.rect(tile_size))
        if len(item.card) > 0:
            if not item.shown:
                item_color = [(100, 20, 20), (100, 50, 20), (20, 20, 100), (20, 60, 100), (100, 20, 100)][['H', 'D', 'S', 'C', 'J'].index(item.card[0])]
                pygame.draw.rect(display, item_color, item.rect(tile_size))
                draw_text('{}'.format(item.value), font, (255, 255, 255), display, (item.true_x + 35), (item.true_y + 20))
                if loc in [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (1, 4), (2, 4), (3, 4)]:
                    if item.armor > 0:
                        draw_text('+ {}'.format(item.armor), font, (255, 255, 255), display, (item.true_x + 48), (item.true_y + 20))
            else:
                pygame.draw.rect(display, (20, 20, 20), item.rect(tile_size))
        pygame.draw.rect(display, (100, 100, 100), item.rect(tile_size), 2)
        if click:
            if item.rect(80).collidepoint((mouse[0], mouse[1])):
                if loc not in [(0, 0), (0, 4), (4, 0), (4, 4)]:
                    if armor_phase[0]:
                        if loc in [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (1, 4), (2, 4), (3, 4)]:
                            if len(item.card) > 0:
                                item.card[1] += current_card[1]
                                item.armor += current_card[1]
                                current_card, tiles = get_new_card(ordered_deck, tiles)
                        else:
                            score -= 1
                            item.change(current_card)
                            current_card, tiles = get_new_card(ordered_deck, tiles)
                        armor_phase = [False, False]
                    else:
                        if loc in [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (1, 4), (2, 4), (3, 4)]:
                            if current_card[1] > 10:
                                if len(item.card) == 0:
                                    item.change(current_card)
                                    current_card, tiles = get_new_card(ordered_deck, tiles)
                        else:
                            if current_card[1] < 11:
                                if len(item.card) > 0:
                                    if item.card[1] <= current_card[1] and current_card[1] not in [0, 1]:
                                        item.change(current_card)
                                        current_card, tiles = get_new_card(ordered_deck, tiles)
                                    elif current_card[1] in [0, 1]:
                                        item.change(current_card)
                                        current_card, tiles = get_new_card(ordered_deck, tiles)
                                else:
                                    item.change(current_card)
                                    current_card, tiles = get_new_card(ordered_deck, tiles)
        if right_click:
            if loc in [(0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (1, 4), (2, 4), (3, 4)]:
                if item.rect(80).collidepoint((mouse[0], mouse[1])):
                    item.toggle()

    draw_text('Deck: {}'.format(len(ordered_deck)), font, (255, 255, 255), display, (15), ((4 * tile_size) + 20))
    draw_text('Score: {}'.format(score), font, (255, 255, 255), display, (15), ((4 * tile_size) + 35))

    click = False
    right_click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            print('You had {} points'.format(score))
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            active_deck = generate_cards()
            active_deck, board, royals = generate_board(active_deck, board)
            tiles = generate_tiles()
            tiles = place_royals(royals, tiles)
            current_card, tiles = get_new_card(active_deck, tiles)
            ordered_deck = get_random_deck(active_deck)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
            if event.button == 2:
                print(ordered_deck)
            if event.button == 3:
                right_click = True

    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    mainClock.tick(60)