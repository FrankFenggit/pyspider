from flask import Flask,redirect,url_for
from flask import render_template
from datetime import timedelta
import re,json,sys

from lib import mylogger
from lib.copy_spider_dbfile import MyDBFile
from ext import create_app
from server.parse.jobsParseServer import JobsParseServer
from server.jobsSever import JobsServer

mydbfile=MyDBFile("../pyspider/data/result.db", "./data/")
app = create_app(mydbfile.mydbfile)

#解析爬虫数据，入库，只调用一次
g_init_flag = False
def my_init():
    mylogger.info("call %s " % (sys._getframe().f_code.co_name))
    global g_init_flag
    mylogger.info("[g_init_flag:%s]" % (g_init_flag))
    if g_init_flag:
        return
    job_server = JobsParseServer()
    job_server.parse()
    job_server.save2db()
    g_init_flag = True
    mylogger.info("call %s succefful" % (sys._getframe().f_code.co_name))

@app.route('/jobs/<int:page>')
def get_jobs(page):
    job_ser = JobsServer()
    jobs = job_ser.get_jobs_by_page(page)
    pages = [i+1 for i in range(job_ser.pages)]
    return render_template("index.htm",pages=pages,pages_num=job_ser.pages,jobs=jobs,jobs_total=job_ser.jobs_total)


@app.route("/")
def index():
    my_init()
    return redirect("/jobs/1")


if __name__ == '__main__':
    app.run()
