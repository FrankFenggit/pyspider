#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-06-12 11:45:08
# Project: lib库

import json
import sqlite3

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
mylogger = logging.getLogger(name="fileLogger")

class CompNameToJsonUrl:
    URL="https://www.tianyancha.com/search?key="
    KEY = "baseUrl_list"
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
    def _dumpjson(self):
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




