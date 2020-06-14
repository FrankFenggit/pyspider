#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2020-06-12 11:45:08
# Project: 51job

from pyspider.libs.base_handler import *
import json

import logging
import logging.config

logging.config.fileConfig('logging.conf')

# create logger
mylogger = logging.getLogger(name="fileLogger")


class Handler(BaseHandler):
    crawl_config = {
    }

    def load_conf(self): #加载配置 url
        f = open('./51job_conf.json', encoding='utf-8')  # 打开json文件
        res = f.read()  # 读文件
        dict = json.loads(res)
        f.close()
        for each_one in dict["baseUrl_list"]:
            url=each_one["url"]
            if not url or (url in self.baseUrl):
                continue
            self.baseUrl.append(url)

    def __init__(self):
        # 搜索URL基线
        self.baseUrl = []

    @every(minutes=1 * 60)
    def on_start(self):
        mylogger.info("call on_start")
        self.load_conf();
        for url in self.baseUrl:
            mylogger.info(url)
            self.crawl(url, callback=self.index_page, validate_cert=False, fetch_type='js')

    @config(age=0.5 * 60 * 60)
    def index_page(self, response):
        mylogger.info("call index_page")
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
        mylogger.info("call detail_page")
        return {
            "url": response.url,
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

