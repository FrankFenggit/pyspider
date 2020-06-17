#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.config

# 日志模块拆分
logging.config.fileConfig('logging.conf')
mylogger = logging.getLogger(name="fileLogger") # create logger