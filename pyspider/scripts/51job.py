#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-06-12 11:45:08
# Project: 51job

from pyspider.libs.base_handler import *
import json
import sqlite3

from lib import mylogger

class Handler(BaseHandler):
    crawl_config = {
    }

    def load_conf(self): #加载配置 url
        conf_file="./%s_conf.json"%(self.project_name)
        mylogger.info("[conf_file:%s]"%(conf_file))
        f = open(conf_file, encoding='utf-8')  # 打开json文件
        res = f.read()  # 读文件
        dict = json.loads(res)
        f.close()
        for each_one in dict["baseUrl_list"]:
            url=each_one["url"]
            if not url or (url in self.baseUrl):
                continue
            self.baseUrl.append(url)
    def cleardb(self,dbpath,dbtbl_name):  # delete table 有时候无效 ，采用drop table
        mylogger.info("call %s "%(sys._getframe().f_code.co_name))
        try:
            conn = sqlite3.connect(dbpath)
            c = conn.cursor()
            # 获取建表语句
            sql_create = "select sql from sqlite_master where type='table' and  tbl_name='%s'"%(dbtbl_name)
            cursor = c.execute(sql_create)
            sql_create=""
            for row in cursor:
                sql_create=row[0]
                break
            # drop table
            if not sql_create.isspace():
                sql_drop="drop table %s"%(dbtbl_name)
                cursor=c.execute(sql_drop)
                cursor = c.execute(sql_create)
                conn.commit()
                mylogger.info("cleardb [%s:%s] %s succeful" % (dbpath, dbtbl_name,sql_drop))
            else:
                mylogger.error("[sql_create:isspace]")
        except:
            mylogger.error("cleardb [%s:%s] failed"%(dbpath,dbtbl_name))
        finally:
            cursor.close()
            conn.close()
    def __init__(self):
        # 搜索URL基线
        self.baseUrl = []

    @every(minutes=1 * 60)
    def on_start(self):
        mylogger.info("call %s "%(sys._getframe().f_code.co_name))
        # 清空数据库 重新启动爬虫任务
        dbtbl_name="resultdb_"+self.project_name
        self.cleardb('./data/result.db',dbtbl_name);
        dbtbl_name = "taskdb_" + self.project_name
        self.cleardb('./data/task.db',dbtbl_name);
        # 加载配置
        self.load_conf();
        for url in self.baseUrl:
            mylogger.info("[baseUrl:%s]"%(url))
            self.crawl(url, callback=self.index_page, validate_cert=False, fetch_type='js')

    @config(age=0.5 * 60 * 60)
    def index_page(self, response):
        mylogger.info("call %s "%(sys._getframe().f_code.co_name))
        # 职位列表跳转
        for each in response.doc('#resultList p > span > a').items():
            mylogger.info("职位列表url: " + each.attr.href)
            self.crawl(each.attr.href, callback=self.detail_page, validate_cert=False, fetch_type='js')
        # 翻页
        detail_url_list=[x.attr.href for x in response.doc('#resultList  .bk>a').items()]
        mylogger.info("翻页url: " + "分页".join(detail_url_list))
        self.crawl(detail_url_list, callback=self.index_page,
                   validate_cert=False, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        mylogger.info("call %s "%(sys._getframe().f_code.co_name))
        return {
            "url": response.url,
            "proj_name": self.project_name,
            "job_title": response.doc('h1').text(),
            "job_salary": response.doc('.cn > strong').text(),
            "job_comp": response.doc('.catn').text(),
            "job_scr1": response.doc('.ltype').text(),
            "job_scr2": response.doc('.jtag > div').text(),
            "job_addr": response.doc('.bmsg > .fp').text(),
            "job_comp_brief": response.doc('.tmsg').text(),
        }

    def on_result(self, result):
        if not result:
            mylogger.info("call on_result if not result")
            return
        mylogger.info("call on_result")
        mylogger.debug(result)
        return super(Handler, self).on_result(result)

    def on_finished(self, response, task):
        mylogger.info("call %s " % (sys._getframe().f_code.co_name))
        mylogger.info(self)
        mylogger.info(response)
        mylogger.info(task)

