#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.jobs_entity import TblJobs51job

class JobsServer:
    NUMS_PER_PAGE=20
    def __init__(self):
        self.pages = 0
        self.jobs_total = 0
    def get_jobs_by_page(self,page=1):
        jobs =  TblJobs51job.query.filter(TblJobs51job.job_salary>0).order_by(TblJobs51job.job_comp,TblJobs51job.job_salary.desc()).paginate(int(page), int(JobsServer.NUMS_PER_PAGE),False)
        self.pages = jobs.pages
        self.jobs_total = jobs.total
        return  jobs.items