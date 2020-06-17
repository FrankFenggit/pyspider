#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import re
import json

from model import db
from model.jobs_entity import *
from lib import mylogger


class JobsParseServer:
    def __init__(self):
        self.results_spider = Resultdb51job.query.all()
        self.results_parse = []

    def save2db(self):
        TblJobs51job.query.delete();
        for each in self.results_parse:
            db.session.add(each)
            db.session.commit()
    def parse(self):
        self.results_parse.clear()
        for every in self.results_spider:
            each = json.loads(every.result) # str 转 json
            proj_name = self._parse_proj_name(each)
            job_url = self._parse_job_url(each)
            job_title = self._parse_job_title(each)
            job_salary_str = self._parse_job_salary_str(each)
            job_salary = self._parse_job_salary(each)
            job_comp = self._parse_job_comp(each)
            job_addr = self._parse_job_addr(each)
            job_time = self._parse_job_time(each)
            tbl_model  = TblJobs51job(proj_name,job_url,job_title,job_salary_str,job_salary,job_comp,job_addr,job_time)
            self.results_parse.append(tbl_model)
        return self.results_parse

    def _parse_proj_name(selt, each):
        return each["proj_name"]

    def _parse_job_url(selt, each):
        return each["url"]

    def _parse_job_title(selt, each):
        return each["job_title"]

    def _parse_job_salary_str(selt, each):
        return each["job_salary"]

    def _parse_job_salary(selt, each):
        salary =  each["job_salary"]
        salary_list = [float(s) for s in re.findall(r'\d+\.?\d*', salary)]
        length = len(salary_list)
        # 单位转换
        units = ['\u5343', '\u4e07']  # 千 万
        units_trans = [1000, 10000]
        len_units = len(units)
        for index in range(len_units):
            pattern = units[index]
            matchobj = re.search(pattern,salary)
            if not matchobj:
                continue
            for i in range(length):
                salary_list[i] = salary_list[i]*units_trans[index]
            break
        #年薪 换成月薪资
        pattern='\u5e74'
        matchobj=re.search(pattern,salary)
        if not matchobj:
            mylogger.warning("[salary_list:%s][salary:%s]"%(salary_list,salary))
        else:
            for i in range(length):
                salary_list[i] = salary_list[i]/12

        if not length:
            return 0
        if length==1:
            mylogger.error("[salary_list:%s][salary:%s]"%(salary_list,salary))
            return salary_list[0]
        if length==2:
            mylogger.debug("[salary_list:%s][salary:%s]" % (salary_list, salary))
            return int((salary_list[0]+salary_list[1])/2)
        if length>2:
            mylogger.error("[salary_list:%s][salary:%s]" % (salary_list, salary))
            return int((salary_list[0] + salary_list[1]) / 2)
    def _parse_job_comp(selt, each):
        return each["job_comp"]

    def _parse_job_addr(selt, each):
        ret = ""
        patten='\uff1a' # 上班地址：光谷APP广场2号楼17层
        addr_split = re.split(patten,each["job_addr"])
        len_addr_split = len(addr_split)
        if len_addr_split==1:
            ret = addr_split[0].strip()
            mylogger.warning("[addr_split[0]:%s]"%(addr_split[0]))
        elif len_addr_split==2:
            ret = addr_split[1].strip()
        elif len_addr_split>2:
            ret = addr_split[1].strip()
            mylogger.error("[addr_split[0]:%s]" % (addr_split[0]))

        return ret



    def _parse_job_time(selt, each):
        ret = ""
        job_src =  each["job_scr1"]
        job_src_split = re.split(r'\u00a0',job_src)
        pattern = '\u53d1\u5e03' # 发布
        for every in job_src_split :
            matchobj = re.search(pattern,every)
            if not matchobj:
                continue
            ret = every
            break
        return ret




