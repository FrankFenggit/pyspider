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
        #目标路径检测
        if not os.path.exists(os.path.dirname(to_path)):
            os.makedirs(os.path.dirname(to_path))
        self.from_path = os.path.abspath(from_path)
        self.to_path = os.path.abspath(to_path)
        self.mydbfile = os.path.join(self.to_path, os.path.split(self.from_path)[1])
        #目标文件检测，不存在就拷贝
        if os.path.isfile(self.mydbfile):
            mylogger.info("数据库已存在,如果要使用新库，请删除当前数据库，系统会自动拷贝爬虫数据库[self.mydbfile:%s]" % (self.mydbfile))
            return
        shutil.copy(from_path, to_path)
        if os.path.isfile(self.mydbfile):
            mylogger.info("数据库拷贝成功")
        else:
            mylogger.error("数据库拷贝失败")
        mylogger.info("[self.from_path:%s][self.to_path:%s]" % (self.from_path, self.to_path))
        mylogger.info("[self.mydbfile:%s]" % (self.mydbfile))