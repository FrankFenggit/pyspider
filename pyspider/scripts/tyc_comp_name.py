#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-06-12 11:45:08
# Project: 51job

from pyspider.libs.base_handler import *
import json, sqlite3, re

import logging, logging.config

from scripts.tyc_comp_name_lib import CompNameToJsonUrl
from lib.urlParse import url_parse

logging.config.fileConfig('logging.conf')

# create logger
mylogger = logging.getLogger(name="fileLogger")


class Handler(BaseHandler):
    headers = {
        # "Host": "book.qidian.com",
        # "Connection": "keep-alive",
        # "Accept-Encoding": "gzip, deflate, sdch",
        # "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        # "Referer":"https://www.baidu.com",      "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    }
    crawl_config = {
        "headers": headers,
        #"timeout": 1000
    }

    def load_conf(self):  # 加载配置 url
        conf_file = "./%s_conf.json" % (self.project_name)
        mylogger.info("[conf_file:%s]" % (conf_file))
        f = open(conf_file, encoding='utf-8')  # 打开json文件
        res = f.read()  # 读文件
        dict = json.loads(res)
        f.close()
        for each_one in dict["baseUrl_list"]:
            url = each_one["url"]
            if not url or (url in self.baseUrl):
                continue
            self.baseUrl.append(url)

    def cleardb(self, dbpath, dbtbl_name):  # delete table 有时候无效 ，采用drop table
        mylogger.info("call %s " % (sys._getframe().f_code.co_name))
        try:
            conn = sqlite3.connect(dbpath)
            c = conn.cursor()
            # 获取建表语句
            sql_create = "select sql from sqlite_master where type='table' and  tbl_name='%s'" % (dbtbl_name)
            cursor = c.execute(sql_create)
            sql_create = ""
            for row in cursor:
                sql_create = row[0]
                break
            # drop table
            if not sql_create.isspace():
                sql_drop = "drop table %s" % (dbtbl_name)
                cursor = c.execute(sql_drop)
                cursor = c.execute(sql_create)
                conn.commit()
                mylogger.info("cleardb [%s:%s] %s succeful" % (dbpath, dbtbl_name, sql_drop))
            else:
                mylogger.error("[sql_create:isspace]")
        except:
            mylogger.error("cleardb [%s:%s] failed" % (dbpath, dbtbl_name))
        finally:
            cursor.close()
            conn.close()

    def __init__(self):
        # 搜索URL基线
        self.baseUrl = []

    @every(minutes=1* 24 * 60)
    def on_start(self):
        mylogger.info("call %s " % (sys._getframe().f_code.co_name))
        # 清空数据库 重新启动爬虫任务
        # dbtbl_name = "resultdb_" + self.project_name
        # self.cleardb('./data/result.db', dbtbl_name);
        # dbtbl_name = "taskdb_" + self.project_name
        # self.cleardb('./data/task.db', dbtbl_name);
        # 加载配置
        comp_name_tojson = CompNameToJsonUrl("./data/comp_name.txt", "./%s_conf.json" % (self.project_name))
        comp_name_tojson.to_json()
        self.load_conf();
        for url in self.baseUrl:
            mylogger.info("[baseUrl:%s]" % (url))
            self.crawl(url, callback=self.index_page, validate_cert=False, fetch_type='js')

    @config(age=10 *24 * 60 * 60)
    def index_page(self, response):
        mylogger.info("call %s " % (sys._getframe().f_code.co_name))
        # 详情页跳转
        for each in response.doc('#web-content div.header> a').items():
            mylogger.info("公司链接url: " + each.attr.href)
            mylogger.debug("公司名称: " + each.text())
            result, query_dict = url_parse(response.url)
            comp_name = query_dict.get("key", [])
            print(type(comp_name))
            if not len(comp_name):
                break
            seachobj = re.search(''.join(comp_name), each.text())
            if seachobj:
                self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False, fetch_type='js')
                break

    @config(priority=2)
    def detail_page(self, response):
        mylogger.info("call %s " % (sys._getframe().f_code.co_name))
        return {
            "url": response.url,
            "proj_name": self.project_name,
            "comp_website": response.doc('.company-link').text(),
            "comp_regmoney": response.doc('#_container_baseInfo .-breakall tr:nth-child(1) > td:nth-child(2) > div').text(),
            "comp_realmoney": response.doc('#_container_baseInfo .-breakall tr:nth-child(1) > td:nth-child(4)').text(),
            "comp_unisocialcode": response.doc('#_container_baseInfo .-breakall tr:nth-child(3) > td:nth-child(2)').text(),
            "comp_guimo": response.doc('#_container_baseInfo .-breakall tr:nth-child(8) > td:nth-child(2)').text(),
            "comp_nums": response.doc('#_container_baseInfo .-breakall tr:nth-child(8) > td:nth-child(4)').text(),
            "comp_name": response.doc('#company_web_top h1').text()
        }

    def on_result(self, result):
        if not result:
            mylogger.info("call on_result if not result")
            return
        mylogger.info("call on_result")
        mylogger.debug(result)
        return super(Handler, self).on_result(result)

