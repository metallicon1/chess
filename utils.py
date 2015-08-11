#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2015-07-15, dyens
#
from multiprocessing import Process
import time
from matplotlib import pyplot as plt

def plot(img, title='title'):
    plt.imshow(img, 'gray'), plt.title(title)
    plt.show()


def multi_process(fn):
    def wrap(*args):
        p = Process(target = fn, args=args)
        p.start()
        return p
    return wrap


