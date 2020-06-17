#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 这个文件目的就是保证app  和 templates是同级目录，否则route找不模板
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app(db_path):
    app = Flask(__name__)
    app.jinja_env.auto_reload = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % (db_path)
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app