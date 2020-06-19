#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-06-12 11:45:08
# Project: lib库

import json
import sqlite3,sys

from lib.mylog import mylogger

class CompNameToJsonUrl:
    URL="https://www.tianyancha.com/search?key="
    KEY = "baseUrl_list"
    KEY_ONSTART = "on_start"
    KEY_FINISHED = "on_finished"
    def __init__(self,from_path,to_path):
        self.from_path=from_path
        self.to_path=to_path
        self.json = {CompNameToJsonUrl.KEY:[]}
    def to_json(self):
        # 清空
        self.json.clear()
        self.json = {CompNameToJsonUrl.KEY: []}
        # 加载txt
        self._LoadText()
        # 生成json文件
        self._dumpjson()
    def chg_status(self,status):
        mylogger.info("call %s " % (sys._getframe().f_code.co_name))
        if status.strip()==CompNameToJsonUrl.KEY_FINISHED.strip():
            self.json[CompNameToJsonUrl.KEY_FINISHED] = True
            self.json[CompNameToJsonUrl.KEY_ONSTART] = False
            mylogger.info(self.json)
            with open(self.to_path, "w", encoding='utf-8') as f:
                json.dump(self.json, f, indent=1)
    def _dumpjson(self):
        mylogger.info("call %s " % (sys._getframe().f_code.co_name))
        self.json[CompNameToJsonUrl.KEY_FINISHED] = False
        self.json[CompNameToJsonUrl.KEY_ONSTART] = True
        mylogger.info(self.json)
        with open(self.to_path,"w", encoding='utf-8') as f:
            json.dump(self.json,f,indent=1)
    def _LoadText(self):
        with open(self.from_path,'r', encoding='utf-8') as f:
            while True:
                line = f.readline() # 整行读取数据
                if not line:
                    break
                line=line.strip()
                if not line:
                    continue
                url_dict = {}
                url_dict["url"] = "%s%s"%(CompNameToJsonUrl.URL,line)
                if url_dict in  self.json[CompNameToJsonUrl.KEY]:
                    continue
                self.json[CompNameToJsonUrl.KEY].append(url_dict)




