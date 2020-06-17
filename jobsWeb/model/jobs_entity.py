#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import db

class Resultdb51job(db.Model):
    __tablename__ = 'resultdb_51job'

    taskid = db.Column(nullable=False, primary_key=True)
    url = db.Column(nullable=False)
    result = db.Column(nullable=False)
    updatetime = db.Column(nullable=False)



class TblJobs51job(db.Model):
    __tablename__ = 'tbl_jobs_51job'

    ID = db.Column(db.Integer, primary_key=True)
    proj_name = db.Column(db.Text)
    job_url = db.Column(db.Text)
    job_title = db.Column(db.Text)
    job_salary_str = db.Column(db.Text)
    job_salary = db.Column(db.Integer)
    job_comp = db.Column(db.Text)
    job_addr = db.Column(db.Text)
    job_time = db.Column(db.Text)

    def __init__(self,proj_name,job_url,job_title,job_salary_str,job_salary,job_comp,job_addr,job_time):
        self.proj_name = proj_name
        self.job_url = job_url
        self.job_title = job_title
        self.job_salary_str = job_salary_str
        self.job_salary = job_salary
        self.job_comp = job_comp
        self.job_addr = job_addr
        self.job_time = job_time


