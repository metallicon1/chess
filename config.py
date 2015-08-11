#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2015-07-14, dyens
#
import os

PROJECT_PATH = os.path.relpath(os.path.dirname(__file__))
PICS_DIR = os.path.join(PROJECT_PATH, 'pics')
FIGURES_DIR = os.path.join(PICS_DIR, 'figures')
TMP_DIR = os.path.join(PICS_DIR, 'tmp')
ENGINE = '/usr/games/bin/gnuchess'
ENGINE_TIME_CALCULATION = 3
STEP_TIME = 3


try:
    from local_settings import *
except ImportError:
    pass



