#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2015-07-14, programming
#

from desk import Desk
from engine import Engine
import time 
from config import STEP_TIME
import subprocess
from utils import plot

class Player(object):
    side = None
    position = set()
    engine = None
    desk_coords = None
    steps = []

    def __init__(self):
        d = Desk()
        self.position = d.get_position()
        self.side = d.side
        self.desk_coords = d.desk_coords
        self.desk = d

    def refresh_desk(self):
        time.sleep(2)
        d = Desk(self.side, self.desk_coords)
        self.position = d.get_position()
        print 'refreshed'

    def change_step_side(self):
        if self.step_side == 'w':
            self.step_side = 'b'
        else:
            self.step_side = 'w'


    def change_position(self, move):
        print u'изменение позиции %s' %move
        from_move = move[:2]
        to_move = move[2:4]
        figure = move[4:]
        position_dict = {i[0]: i[1] for i in self.position}
        # white short castle
        if from_move == 'e1' and to_move == 'g1':
            del position_dict[from_move]
            del position_dict['h1']
            position_dict[to_move] = 'kw'
            position_dict['f1'] = 'rw'
        # white long castle
        elif from_move == 'e1' and to_move == 'c1':
            del position_dict[from_move]
            del position_dict['a1']
            position_dict[to_move] = 'kw'
            position_dict['d1'] = 'rw'
        # black short castle
        elif from_move == 'e8' and to_move == 'g8':
            del position_dict[from_move]
            del position_dict['h8']
            position_dict[to_move] = 'kb'
            position_dict['f8'] = 'rb'
        # black long castle
        elif from_move == 'e8' and to_move == 'c8':
            del position_dict[from_move]
            del position_dict['a8']
            position_dict[to_move] = 'kb'
            position_dict['d8'] = 'rb'
        # p to q
        elif figure:
            del position_dict[from_move]
            position_dict[to_move] = figure + self.step_side
        # atack or step
        else:
            move_fig = position_dict[from_move]
            position_dict[to_move] = move_fig
            del position_dict[from_move]
        position_set = set()
        for field, figure in position_dict.iteritems():
            position_set.add((field, figure))
        self.position = position_set


    def start(self):
        self.engine = Engine()
        self.engine.new_game()
        self.engine.set_start_position()
        if self.side == 'WHITE':
            self.step_side = 'w'
            move = self.engine.calulate()
            print 'game start'
            print move
            print 'game go'
            self.steps.append(move)
            self.go(move)
            self.change_step_side()
            self.change_position(move)
        else:
            self.step_side = 'b'

    def go(self, move=None):
        _from = move[:2]
        _to = move[2:4]
        delta = self.desk_coords
        from_position = self.desk.get_field_coord(_from)
        to_position = self.desk.get_field_coord(_to)
        # Двигает мышку
        subprocess.call('xdotool mousemove %d %d' %(from_position[0] + delta[0], from_position[1] + delta[1]), shell=True)
        subprocess.call('xdotool mousedown 1', shell=True)
        subprocess.call('xdotool mousemove %d %d' %(to_position[0] + delta[0], to_position[1] + delta[1]), shell=True)
        subprocess.call('xdotool mouseup 1', shell=True)
        subprocess.call('xdotool mousemove %d %d' %(0, 0), shell=True)

    def play(self):
        while True:
            time.sleep(STEP_TIME)
            move = self.get_move()
            print u'ход %s' %move
            if move == self.steps[-1]:
                continue
            if move is not None:
                self.change_position(move)
                self.change_step_side()
                self.steps.append(move)
                moves = ' '.join(self.steps)
                self.engine.move(moves)
                our_move = self.engine.calulate()
                self.steps.append(our_move)
                print u'мы ходим %s' %our_move
                self.go(our_move)
                self.change_step_side()
                self.change_position(our_move)

    def get_move(self):
        old_position = self.position
        d = Desk(self.side, self.desk_coords)
        position = d.get_position()
        diff = position.symmetric_difference(old_position)

        print '#'*10
        print 'old'
        print old_position
        print '#'*10
        print 'new'
        print position
        print '#'*10
        print 'diff'
        print diff
        print '#'*10



        from_move = None
        to_move = None
        figure = ''
        if len(diff) == 2:
            # Просто ход фигуры и пешка дошла до края
            from_figure = None
            to_figure = None
            for i in diff:
                if {i}.issubset(old_position):
                    from_move = i[0]
                    from_figure = i[1]
                else:
                    to_move = i[0]
                    to_figure = i[1]
            if to_figure != from_figure:
                figure = to_figure[0]

        elif len(diff) == 3:
            # Срубили фигуру и взятие на проходе
            fig = None
            for i in diff:
                if {i}.issubset(position):
                    to_move = i[0]
                    fig = i[1]

            for i in diff:
                if i[1] == fig and i[0] != to_move:
                    from_move = i[0]

        elif len(diff) == 4:
            # Рокировка
            for i in diff:
                if i[1][0] == 'k':
                    if {i}.issubset(old_position):
                        from_move = i[0]
                    else:
                        to_move = i[0]
#        elif len(diff) == 0:
#            return None
#        else: 
#            print diff
#            plot(d.desk)

        if from_move is None:
            return None
        else:
            step = '%s%s%s' %(from_move, to_move, figure)
            return step

    def __del__(self):
        self.engine.quit()




if __name__ == '__main__':
    p = Player() 
    p.start()
    p.play()
