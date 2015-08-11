#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2015-07-08, dyens
#
from config import PICS_DIR, FIGURES_DIR, TMP_DIR
import subprocess
import cv2
import numpy as np
import os
from utils import multi_process
import gtk.gdk as gd
from utils import plot


class Cell(object):
    x = y = None
    name = None
    figure = None

    def __init__(self, name, x=None, y=None, figure=None):
        self.x = x
        self.y = y
        self.name = name
        self.figure = figure

    def __str__(self):
        return self.name

class Desk(object):
    h = w = 53
    figur_pics = os.listdir(FIGURES_DIR)
    figures = [i[:-4] for i in figur_pics]
    desk_file = os.path.join(TMP_DIR,'desk.png')
    desk = None
    cells = {}
    pic = None
    desk_x = desk_y = None
    position = set()
    side = None
    desk_coords = None


    def __init__(self, side=None, desk_coords=None):
        self.side = side
        self.desk_coords = desk_coords
        self._get_desk()
        # ???? Если это не писать, то position не обновляется при создании
        # нового класса !!!
        self.position = set()

    def get_position(self):
        if not self.cells:
            self._get_cells()
        for i, j in self.cells.iteritems():
            if j.figure is None:
                continue
            self.position.add((i, j.figure))
        return self.position

    def get_field_coord(self, field):
        if not self.cells:
            self._get_cells()
        cell = self.cells.get(field)
        return cell.x, cell.y




    def _get_cells(self):
        if self.side is None:
            self._get_side()
        cells = {}
        x_c, y_c = 0, 0
        x = x_c
        w = ['a', 'b', 'c', 'd', 'e', 'f', 'g' ,'h']
        h = range(1, 9)
        if self.side == 'BLACK':
            w.reverse()
            h.reverse()
        figures = {}
        process = []
        for f in self.figures:
            f_name, coord = self._get_coord(f)
            for c in coord:
                figures.update({c: f_name})

        for i in w:
            y = y_c + self.h * 8
            for j in h:
                fig = None
                name = '%s%d' %(i, j)
                c_x = x+self.w/2
                c_y = y-self.h/2
                for c in figures:
                    f_x, f_y = c
                    f_x = f_x + self.w/2
                    f_y = f_y + self.h/2
                    if abs(f_x - c_x) < self.h/2 and abs(f_y - c_y) < self.h/2:
                        fig = figures[c]
                c = Cell(name, x=x+self.w/2, y=y-self.h/2, figure=fig)
                cells.update({name: c})
                y = y - self.h
            x = x + self.w
        self.cells = cells

    def _get_desk_coord(self):
        if not self.desk_coords:
            part_desk = os.path.join(PICS_DIR, 'part_desk.png')
            figure = cv2.imread(part_desk, 0)
            res = cv2.matchTemplate(self.desk,figure,cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where( res >= threshold)
            zipped_loc = zip(*loc[::-1])
            if not zipped_loc:
                print u'Шахматная доска не обнаружена'
                raise Exception
            x=y=0
            for l in zipped_loc:
                x+=l[0]
                y+=l[1]
            x = x/len(zipped_loc)
            y = y/len(zipped_loc) - 2 * self.h
            self.desk_coords = (x,y)
        return self.desk_coords



    def paint(self, pt, w, h):
        if self.pic is None:
            self.pic = self.desk
        cv2.rectangle(self.pic, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

    def write(self):
        cv2.imwrite(os.path.join(TMP_DIR,'res.png'), self.pic)


    def _get_desk(self):
        u'''
        Инициализирует переменную self.desk
        '''
        w = gd.get_default_root_window()
        sz = w.get_size()
        pb = gd.Pixbuf(gd.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        img_rgb = pb.get_pixels_array()

#        subprocess.call('scrot %s' %self.desk_file, shell=True)
#        img_rgb = cv2.imread(self.desk_file)
#        img_rgb = cv2.imread('1.png')

        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        self.desk = img_gray
        # Вырежим нашу доску
        self.desk_x, self.desk_y = self._get_desk_coord()
        img = img_gray[self.desk_y: self.desk_y + 8*self.h, 
                self.desk_x: self.desk_x + 8*self.w]
        self.desk = img

    def _get_side(self):
        bk = 'kb'
        wk = 'kw'
        _, bk_coord = self._get_coord(bk) 
        _, wk_coord = self._get_coord(wk)
        if bk_coord[0][1] < wk_coord[0][1]:
            self.side = 'WHITE'
        else:
            self.side = 'BLACK'

    def _get_coord(self, fig):
        figure = cv2.imread(os.path.join(FIGURES_DIR, '%s.png' %fig), 0)
        res = cv2.matchTemplate(self.desk,figure,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        return (fig, zip(*loc[::-1]))


if __name__ == '__main__':
    d = Desk()

    for i in d.get_position():
        print i
#    import time
#    while True:
#        print '###'
#        time.sleep(5)
#        d = Desk()
#        count = 0
#        for i in  d.get_position():
#            if i[1]=='nw':
#                print i
#                count += 1
#        if count == 4:
#            break
#            pass
#        coord = d.get_field_coord('f5')

    # try paint
#    d.paint(coord, 20, 20)
#    d.write()

    #for i in d.figures:
    #    print i
    #    print d.get_coord(i)

#    for i, j in d.cells.iteritems():
#        if j.figure is not None:
#            d.paint((j.x, j.y), 20,20)
#    d.write()
#for pt in zip(*loc[::-1]):

