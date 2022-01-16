# -*- coding: utf8 -*-
import pygame
import json
import random
import os
import sys

FPS = 60
WIDTH, HEIGHT = 1024, 1024
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = f'data/images/{name}'
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(pygame.Color(colorkey))
    else:
        image = image.convert_alpha()

    return image


class MainWindow:
    def __init__(self):
        self.health = 3

        self.cell_size = 50
        self.x = 10
        self.y = 10

        self.num_lvl = 1

        self.pos_ = pos_evil

        self.table = {
            'brick': 0,
            'kill': 0,
            'points': 0
        }

        self.dop = {'it_points': 0,
                    'num_lvl': []
                    }

        self.points = 0

        self.stop_lose = 1
        self.stop = 1

        self.bomb_positions = []
        self.ch_position = CHARACTER_PARAMETR_NONE['position']

        self.board_coord = []

    def pause_game(self):
        if self.stop == 0:
            screen.fill(pygame.Color('black'))

            self.stop = 1
        else:
            intro_text = "Pause"

            font = pygame.font.Font(None, 30)
            text_coord = [155, 25]
            string_rendered = font.render(intro_text, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord[1]
            intro_rect.right = text_coord[0]
            intro_rect.x = text_coord[0]
            text_coord[1] += intro_rect.height
            screen.blit(string_rendered, intro_rect)

            self.stop = 0

    def draw_lose(self):
        screen.fill((0, 0, 255))
        if self.health > 0:
            intro_text = ["Вы проиграли! ((", "",
                          f'В этой игре вы набрали: {self.points} очков', "",
                          f'У вас осталось: {self.health} жизней',
                          'Кликните по экрану, чтобы начать уровень заново', '']
        else:
            intro_text = ["Игра окончена! ((", "",
                          f'В этой игре вы набрали: {self.points} очков', "",
                          f'У вас осталось: {self.health} жизней',
                          'Кликните по экрану, чтобы выйти', '']

        font = pygame.font.Font(None, 45)
        text_coord = 150
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

    def draw_start(self):
        if self.stop_lose:
            if self.stop:

                intro_text = f'Score: {self.points}'

                screen.fill((0, 0, 0))
                pygame.draw.rect(screen, pygame.Color('white'), (100, 25, 50, 50))
                pygame.draw.rect(screen, pygame.Color('black'), (106, 35, 13, 33))
                pygame.draw.rect(screen, pygame.Color('black'), (130, 35, 13, 33))

                font = pygame.font.Font(None, 40)
                text_coord = [450, 30]
                string_rendered = font.render(intro_text, True, pygame.Color('white'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = text_coord[1]
                intro_rect.right = text_coord[1]
                intro_rect.x = text_coord[0]
                text_coord[1] += intro_rect.height
                screen.blit(string_rendered, intro_rect)

                x0, y0 = 800, 25

                im = load_image('heart.png')
                for i in range(self.health):
                    screen.blit(im, (x0 + i * 50, y0))

                for y in range(ROW):
                    dop = []
                    for x in range(COLUMN):
                        datas = SIGNS[FIELD[y][x]][1]

                        cell_size = datas['cell_size']
                        x1, y1 = datas['size']

                        im_surf = pygame.image.load(datas['im']).convert_alpha()

                        im_surf.set_colorkey((0, 255, 255))

                        im_rect = (75 + x1 + x * cell_size, 75 + y1 + y * cell_size,
                                   cell_size,
                                   cell_size)

                        screen.blit(im_surf, im_rect)

                        dop.append({
                            (y, x): [75 + x1 + x * cell_size,
                                     75 + y1 + y * cell_size,
                                     cell_size,
                                     cell_size]})
                    self.board_coord.append(dop)

    def lose(self):
        lose_game.play()
        self.stop_lose = 0

        self.health -= 1
        t = 0
        for i in self.dop['num_lvl']:
            for k in i:
                if self.num_lvl == k:
                    t = 1
                    i[k] = self.table
        if t == 0:
            self.dop['num_lvl'].append({self.num_lvl: self.table})
        for i in self.dop['num_lvl']:
            for k in i:
                self.dop['it_points'] += i[k]['points']

        with open('data/scoring.json', 'w') as file_w:
            json.dump(self.dop, file_w)

    def generate_lvl(self):
        if self.num_lvl <= 3:
            f = 'map_{}.txt'.format(self.num_lvl)

            return f
        else:
            return 'break'

    def win(self):
        self.pos_ = []
        self.ch_position = (0, 0)
        self.points = self.table['points']
        self.dop['num_lvl'].append(
            {self.num_lvl: self.table}
        )
        with open('data/scoring.json', 'w') as file_w:
            json.dump(self.dop, file_w)
        self.table = {
            'brick': 0,
            'kill': 0,
            'points': 0
        }
        self.num_lvl += 1

    def move_w(self):
        if self.stop_lose:
            if self.stop:
                if 0 <= self.ch_position[0] - 1 <= ROW:
                    if FIELD[self.ch_position[0] - 1][self.ch_position[1]] == '0':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0] - 1, self.ch_position[1])
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                    elif FIELD[self.ch_position[0] - 1][self.ch_position[1]] == 'E':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0] - 1, self.ch_position[1])
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                        self.win()
                        return 'win'
        else:
            return 'lose'

    def move_a(self):
        if self.stop_lose:
            if self.stop:
                if 0 <= self.ch_position[1] - 1 <= COLUMN:
                    if FIELD[self.ch_position[0]][self.ch_position[1] - 1] == '0':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0], self.ch_position[1] - 1)
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                    elif FIELD[self.ch_position[0]][self.ch_position[1] - 1] == 'E':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0], self.ch_position[1] - 1)
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                        self.win()
                        return 'win'
        else:
            return 'lose'

    def move_s(self):
        if self.stop_lose:
            if self.stop:
                if self.ch_position[0] + 1 < ROW:
                    if FIELD[self.ch_position[0] + 1][self.ch_position[1]] == '0':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0] + 1, self.ch_position[1])
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                    elif FIELD[self.ch_position[0] + 1][self.ch_position[1]] == 'E':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0] + 1, self.ch_position[1])
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                        self.win()
                        return 'win'
        else:
            return 'lose'

    def move_d(self):
        if self.stop_lose:
            if self.stop:
                if self.ch_position[1] + 1 < COLUMN:
                    if FIELD[self.ch_position[0]][self.ch_position[1] + 1] == '0':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0], self.ch_position[1] + 1)
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                    elif FIELD[self.ch_position[0]][self.ch_position[1] + 1] == 'E':
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '0'
                        self.ch_position = (self.ch_position[0], self.ch_position[1] + 1)
                        FIELD[self.ch_position[0]][self.ch_position[1]] = '1'

                        self.win()
                        return 'win'
        else:
            return 'lose'

    def add_bomb(self):
        y, x = self.ch_position
        if self.stop_lose:
            if self.stop:
                if 0 <= x - 1 and FIELD[y][x - 1] == '0':
                    FIELD[y][x] = 'v'
                    self.ch_position = (y, x - 1)
                    FIELD[y][x - 1] = '1'
                elif 0 <= y - 1 and FIELD[y - 1][x] == '0':
                    FIELD[y][x] = 'v'
                    self.ch_position = (y - 1, x)
                    FIELD[y - 1][x] = '1'
                elif x + 1 < COLUMN and FIELD[y][x + 1] == '0':
                    FIELD[y][x] = 'v'
                    self.ch_position = (y, x + 1)
                    FIELD[y][x + 1] = '1'
                elif y + 1 < ROW and FIELD[y + 1][x] == '0':
                    FIELD[y][x] = 'v'
                    self.ch_position = (y + 1, x)
                    FIELD[y + 1][x] = '1'
                self.bomb_positions.append([y, x])
        else:
            return 'lose'

    def mouse_pos(self, pos):
        global FIELD, pos_evil, COLUMN, ROW, map_

        if self.stop_lose == 0:
            if self.health > 0:
                self.pos_ = []
                pos_evil = []

                map_ = open(f'map_{self.num_lvl}.txt', 'r').read().rstrip().split()
                COLUMN, ROW = len(map_[0]), len(map_)
                FIELD = [[j for j in col] for col in map_]

                for y in range(ROW):
                    for x in range(COLUMN):
                        if FIELD[y][x] == 'B':
                            pos_evil.append(
                                {
                                    'xy': [y, x],
                                    'pos': move(y, x)
                                }
                            )

                self.pos_ = pos_evil

                self.table = {
                    'brick': 0,
                    'kill': 0,
                    'points': 0
                }
                self.points = 0
                self.stop_lose = 1
                self.stop = 1

                self.bomb_positions = []
                self.ch_position = CHARACTER_PARAMETR_NONE['position']

                self.board_coord = []

                screen.fill((0, 0, 0))
            else:
                quit_game()
        else:
            mouse_pos = list(pos)

            k1 = ''

            for i in self.board_coord:
                for j in i:
                    for k in j:
                        if j[k][0] <= mouse_pos[0] <= j[k][2] + j[k][0] and j[k][1] <= mouse_pos[1] <= j[k][3] + j[k][1]:
                            k1 = list(k)
                            break
            if k1 != '':
                self.blast(k1)
                return self.blast(k1)
            else:
                if button_pause[0] <= mouse_pos[0] <= button_pause[0] + button_pause[2] and button_pause[1] <= \
                        mouse_pos[1] <= button_pause[1] + button_pause[3]:
                    self.pause_game()

    def blast(self, k):
        if self.stop_lose:
            k1 = k
            if self.stop:
                if k1 in self.bomb_positions:
                    bomb_blast.play()

                    brick, kill = 0, 0

                    y, x = k1
                    if x + 1 < COLUMN and FIELD[y][x + 1] == 'X':
                        FIELD[y][x + 1] = '0'
                        self.table['brick'] += 1
                        brick += 1
                    elif x + 1 < COLUMN and FIELD[y][x + 1] == '1':
                        self.lose()
                    elif x + 1 < COLUMN and FIELD[y][x + 1] == 'B':
                        FIELD[y][x + 1] = '0'
                        self.table['kill'] += 1
                        kill += 1
                        die_evil.play()

                        for i in range(len(pos_evil)):
                            if pos_evil[i]['xy'] == [y, x + 1]:
                                pos_evil.remove(pos_evil[i])
                                break

                    if 0 <= x - 1 and FIELD[y][x - 1] == 'X':
                        FIELD[y][x - 1] = '0'
                        self.table['brick'] += 1
                        brick += 1
                    elif 0 <= x - 1 and FIELD[y][x - 1] == '1':
                        self.lose()
                    elif 0 <= x - 1 and FIELD[y][x - 1] == 'B':
                        FIELD[y][x - 1] = '0'
                        self.table['kill'] += 1
                        kill += 1
                        die_evil.play()

                        for i in range(len(pos_evil)):
                            if pos_evil[i]['xy'] == [y, x - 1]:
                                pos_evil.remove(pos_evil[i])
                                break

                    if 0 <= y - 1 and FIELD[y - 1][x] == 'X':
                        FIELD[y - 1][x] = '0'
                        self.table['brick'] += 1
                        brick += 1
                    elif 0 <= y - 1 and FIELD[y - 1][x] == '1':
                        self.lose()
                    elif 0 <= y - 1 and FIELD[y - 1][x] == 'B':
                        FIELD[y - 1][x] = '0'
                        self.table["kill"] += 1
                        kill += 1
                        die_evil.play()

                        for i in range(len(pos_evil)):
                            if pos_evil[i]['xy'] == [y - 1, x]:
                                pos_evil.remove(pos_evil[i])
                                break

                    if y + 1 < ROW and FIELD[y + 1][x] == 'X':
                        FIELD[y + 1][x] = '0'
                        self.table['brick'] += 1
                        brick += 1
                    elif y + 1 < ROW and FIELD[y + 1][x] == '1':
                        self.lose()
                    elif y + 1 < ROW and FIELD[y + 1][x] == 'B':
                        FIELD[y + 1][x] = '0'
                        self.table['kill'] += 1
                        kill += 1
                        die_evil.play()

                        for i in range(len(pos_evil)):
                            if pos_evil[i]['xy'] == [y + 1, x]:
                                pos_evil.remove(pos_evil[i])
                                break

                    FIELD[y][x] = '0'
                    self.table['points'] = (self.table['kill'] * 5) + (self.table['brick'] * 2)
                    if self.num_lvl == 1:
                        self.points = self.table['points']
                    else:
                        self.points += (brick * 2) + (kill * 5)
                    self.bomb_positions.remove(k1)
        else:
            return 'lose'

    def move_evil(self):
        if self.stop_lose == 1:
            if self.stop:
                if len(self.pos_) == 0:
                    self.pos_ = pos_evil
                for k in range(len(self.pos_)):
                    y1, x1 = self.pos_[k]['xy']
                    nap = self.pos_[k]['pos']

                    if self.pos_[k]['pos'] == 'right':
                        if x1 + 1 < COLUMN:
                            if FIELD[y1][x1 + 1] == '0':
                                self.pos_[k]['xy'] = [y1, x1 + 1]
                                FIELD[y1][x1 + 1] = 'B'
                                FIELD[y1][x1] = '0'
                            elif FIELD[y1][x1 + 1] == '1':
                                self.lose()
                            else:
                                self.pos_[k]['pos'] = 'left'
                        elif x1 == COLUMN - 1:
                            self.pos_[k]['pos'] = 'left'
                    if self.pos_[k]['pos'] == 'left':
                        if 0 <= x1 - 1:
                            if FIELD[y1][x1 - 1] == '0':
                                self.pos_[k]['xy'] = [y1, x1 - 1]
                                FIELD[y1][x1 - 1] = 'B'
                                FIELD[y1][x1] = '0'
                            elif FIELD[y1][x1 - 1] == '1':
                                self.lose()
                            else:
                                self.pos_[k]['pos'] = 'right'
                        elif x1 == 0:
                            self.pos_[k]['pos'] = 'right'
                    if self.pos_[k]['pos'] == 'top':
                        if y1 + 1 < ROW:
                            if FIELD[y1 + 1][x1] == '0':
                                self.pos_[k]['xy'] = [y1 + 1, x1]
                                FIELD[y1 + 1][x1] = 'B'
                                FIELD[y1][x1] = '0'
                            elif FIELD[y1 + 1][x1] == '1':
                                self.lose()
                            else:
                                self.pos_[k]['pos'] = 'bottom'
                        elif y1 == ROW - 1:
                            self.pos_[k]['pos'] = 'bottom'
                    if self.pos_[k]['pos'] == 'bottom':
                        if 0 <= y1 - 1:
                            if FIELD[y1 - 1][x1] == '0':
                                self.pos_[k]['xy'] = [y1 - 1, x1]
                                FIELD[y1 - 1][x1] = 'B'
                                FIELD[y1][x1] = '0'
                            elif FIELD[y1 - 1][x1] == '1':
                                self.lose()
                            else:
                                self.pos_[k]['pos'] = 'top'
                        elif y1 == 0:
                            self.pos_[k]['pos'] = 'top'
        else:
            return 'lose'


class Menu:
    def __init__(self):
        self._options = []
        self._callbacks = []
        self._current_option_index = 0

    def append_option(self, option, callback):
        self._options.append(ARIAL_30.render(option, True, (255, 255, 255)))
        self._callbacks.append(callback)

    def switch(self, direction):
        self._current_option_index = max(0, min(self._current_option_index + direction, len(self._options) - 1))

    def select(self):
        self._callbacks[self._current_option_index]()

    def draw(self, surf, x, y, option_y_padding):
        for i, option in enumerate(self._options):
            option_rect: pygame.Rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if i == self._current_option_index:
                pygame.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)


def quit_game():
    global RUN
    RUN = False


def init_game():
    global RUN, COLUMN, ROW, FIELD, koef_step, win, pos_evil, map_

    win = MainWindow()
    while RUN:
        step = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    step = win.move_w()
                elif event.key == pygame.K_a:
                    step = win.move_a()
                elif event.key == pygame.K_s:
                    step = win.move_s()
                elif event.key == pygame.K_d:
                    step = win.move_d()
                elif event.key == pygame.K_SPACE:
                    win.add_bomb()
                elif event.key == pygame.K_ESCAPE:
                    win.pause_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                step = win.mouse_pos(event.pos)

        if koef_step % 10 == 0:
            step = win.move_evil()

            # движение
        if step == 'win':
            win_game.play()
            if win.generate_lvl() == 'break':
                RUN = False
            else:
                map_ = open(win.generate_lvl(), 'r').read().rstrip().split()
                COLUMN, ROW = len(map_[0]), len(map_)
                FIELD = [[j for j in col] for col in map_]
                koef_step = 0

                pos_evil = []

                for y in range(ROW):
                    for x in range(COLUMN):
                        if FIELD[y][x] == 'B':
                            pos_evil.append(
                                {
                                    'xy': [y, x],
                                    'pos': move(y, x)
                                }
                            )

        elif step == 'lose':
            win.draw_lose()
        elif step != 'lose:':
            win.draw_start()
        pygame.display.flip()

        koef_step += 1


def move(y1, x1):
    if x1 + 1 < COLUMN:
        if FIELD[y1][x1 + 1] == '0':
            return 'right'
    if 0 <= x1 - 1:
        if FIELD[y1][x1 - 1] == '0':
            return 'left'
    if y1 + 1 < ROW:
        if FIELD[y1 + 1][x1] == '0':
            return 'top'
    if 0 <= y1 - 1:
        if FIELD[y1 - 1][x1] == '0':
            return 'bottom'


if __name__ == '__main__':
    # параметры по умолчанию
    cell_size = 50  # для всех блоков
    koef_step = 5  # коэффицент сдвига злодея

    pygame.init()
    pygame.display.init()
    pygame.mixer.init()

    ARIAL_30 = pygame.font.SysFont('arial', 40)

    bomb_blast = pygame.mixer.Sound('data/effects/bomb_blasted.ogg')
    bomb_blast.set_volume(0.2)
    lose_game = pygame.mixer.Sound('data/effects/lose_game.ogg')
    win_game = pygame.mixer.Sound('data/effects/win_game.ogg')
    die_evil = pygame.mixer.Sound('data/effects/die_evil.ogg')
    die_evil.set_volume(0.3)

    button_pause = [100, 25, 50, 50]  # кнопка паузы

    # параметры на персонажа по умолчанию
    CHARACTER_PARAMETR_NONE = {
        'size': (25, 25),
        'im': 'data/images/hero_copy.jpg',  # -> none
        'hp': 25,
        'color': (0, 0, 100),
        'bomb': 50,
        'speed': 5,
        'cell_size': cell_size,
        'position': (0, 0)
    }
    # параметры стенки
    BRICK_PARAMETR_NONE = {
        'size': (25, 25),
        'im': 'data/images/wood_copy.jpg',  # -> none
        'hp': 10,
        'color': (255, 255, 0),
        'cell_size': cell_size
    }
    BEDROCK_NONE = {
        'size': (25, 25),
        'im': 'data/images/stone_copy.jpg',
        'hp': 9999999,
        'color': (255, 0, 125),
        'cell_size': cell_size
    }
    # параметры злодеев
    EVIL_CHARACTER_NONE = {
        'size': (25, 25),
        'im': 'data/images/evil.jpg',  # -> none
        'hp': 50,
        'color': (0, 0, 255),
        'speed': 2,
        'cell_size': cell_size
    }
    # параметры дорожки
    TRACK_NONE = {
        'size': (25, 25),
        'color': (0, 255, 0),
        'im': 'data/images/grass_copy.jpg',  # -> none
        'cell_size': cell_size
    }
    # параметры выхода
    EXIT_NONE = {
        'size': (25, 25),
        'color': (0, 0, 255),
        'im': 'data/images/door.jpg',  # -> none
        'cell_size': cell_size
    }
    # параметры бомбы
    BOMB_NONE = {
        'size': (25, 25),
        'color': (0, 125, 0),
        'im': 'data/images/bomb.jpg',
        'cell_size': cell_size
    }

    map_ = open('map_1.txt').read().rstrip().split('\n')
    ''' парсинг данных с .txt файла '''
    COLUMN, ROW = len(map_[0]), len(map_)
    FIELD = [[j for j in col] for col in map_]

    pos_evil = []

    for y in range(ROW):
        for x in range(COLUMN):
            if FIELD[y][x] == 'B':
                pos_evil.append(
                    {
                        'xy': [y, x],
                        'pos': move(y, x)
                    }
                )

    SIGNS = {
        '1': ('c', CHARACTER_PARAMETR_NONE),
        '0': ('t', TRACK_NONE),
        'X': ('b', BRICK_PARAMETR_NONE),
        'B': ('e', EVIL_CHARACTER_NONE),
        'E': ('ex', EXIT_NONE),
        'H': ('h', BEDROCK_NONE),
        'v': ('v', BOMB_NONE)
    }

    menu = Menu()
    win = MainWindow()
    # stat = Statistics()
    # evil = Evil()

    menu.append_option('Начать игру', init_game)
    menu.append_option('Выход', quit_game)

    screen = pygame.display.set_mode((1024, 1024))
    pygame.display.set_caption('Маленькие Бомберы')

    RUN = True

    while RUN:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_w:
                    menu.switch(-1)
                elif e.key == pygame.K_s:
                    menu.switch(1)
                elif e.key == pygame.K_SPACE:
                    menu.select()

        screen.fill((0, 0, 0))

        menu.draw(screen, 100, 100, 75)

        pygame.display.flip()
