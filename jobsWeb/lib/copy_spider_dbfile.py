#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil,sys,os

from lib import mylogger

class MyDBFile:
    def __init__(self,from_path,to_path):
        self.from_path = ""
        self.to_path = ""
        self.mydbfile = ""
        self.copy_db_file(from_path, to_path)

    def copy_db_file(self, from_path, to_path):
        if not os.path.exists(os.path.dirname(to_path)):
            os.makedirs(os.path.dirname(to_path))
        shutil.copy(from_path, to_path)
        self.from_path = os.path.abspath(from_path)
        self.to_path = os.path.abspath(to_path)
        self.mydbfile = os.path.join(self.to_path, os.path.split(self.from_path)[1])
        mylogger.info("[self.from_path:%s][self.to_path:%s]" % (self.from_path, self.to_path))
        mylogger.info("[self.mydbfile:%s]" % (self.mydbfile))