#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2015-07-14, programming
#

import subprocess, time
import re
from config import ENGINE, ENGINE_TIME_CALCULATION

class Engine(object):
    engine = None

    def __init__(self):
        self.engine = subprocess.Popen(
            [ENGINE, '-u'],
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def new_game(self):
        self.put('ucinewgame')


    def set_start_position(self, position=None):
        if position is not None:
            self.put('position startpos moves %s' %position)
        else:
            self.put('position startpos')

    def move(self, moves):
        self.put('position startpos moves %s' %moves)


    def calulate(self):
        self.put('go infinite')
        time.sleep(ENGINE_TIME_CALCULATION)
        self.put('stop')
        for out in self.get():
            ret = out
        pattern = re.compile(r'bestmove (\w+)')
        return pattern.findall(ret)[0]

    def quit(self):
        self.put('quit')

    def put(self, command):
        self.engine.stdin.write(command+'\n')
#        print('\nyou:\n\t'+command)

    def get(self):
        # using the 'isready' command (engine has to answer 'readyok')
        # to indicate current last line of stdout
        self.engine.stdin.write('isready\n')
        while True:
            text = self.engine.stdout.readline().strip()
            if text == 'readyok':
                break
            if text !='':
                yield text

if __name__ == '__main__':
    e = Engine()
    e.new_game()
    e.set_start_position()
    print e.calulate()
    e.move('e2e4')
    print e.calulate()
