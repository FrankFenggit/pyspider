#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import parse

def url_parse(url):
    # url解码
    urldata = parse.unquote(url)
    # url结果
    result = parse.urlparse(urldata)
    # url里的查询参数
    query_dict = parse.parse_qs(result.query)
    # 获取我想要的信息
    #key = query_dict.get('key', [])
    return result,query_dict