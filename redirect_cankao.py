# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import requests
import time
from lxml import etree
from public.mysqlpooldao import MysqlDao
mysql_dao = MysqlDao()
import urllib2
import httplib


url = 'http://mp.weixin.qq.com/s?__biz=MzAxNzAzMTExOA==&mid=209955884&idx=1&sn=151ceaa8b3bc77eb2c41356988fc780d&scene=27#wechat_redirect'


import http.client
conn = http.client.HTTPConnection(url)
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print(r1.status, r1.reason)
# res =requests.get(url)
# req =res.content
# if u'阅读原文' in req:
    # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #            'Accept-Encoding': 'gzip, deflate, sdch',
    #            'Accept-Language': 'zh-CN,zh;q=0.8',
    #            'Connection': 'keep-alive',
    #            'cookie' : 'pgv_pvi=8374003712; dm_login_weixin_scan=',
    #            # 'Host': 'pan.baidu.com',
    #            'Upgrade-Insecure-Requests': '1',
    #            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # html = requests.get(url,allow_redirects=False)
    # print html.headers['Location']
    # print urllib2.geturl()
# res = requests.get(url, allow_redirects=False, timeout=0.5)
# if 300 <= res.status_code < 400:
#     print res.headers['location']
# else:
#     print  '[no redirect]'
# import urllib2
#
# req = urllib2.Request(url)
# try:
#     urllib2.urlopen(req)
# except urllib2.URLError, e:
#     if hasattr(e, "code"):
#         print e.code
#     if hasattr(e, "reason"):
#         print e.reason
# else:
#     print "OK"
# import urllib2
#
#
# class RedirectHandler(urllib2.HTTPRedirectHandler):
#     def http_error_301(self, req, fp, code, msg, headers):
#         pass
#
#     def http_error_302(self, req, fp, code, msg, headers):
#         pass
#
#
# opener = urllib2.build_opener(RedirectHandler)
# opener.open(url)
# print opener




# 参考：
# 这个涉及到两个，仔细看：
# url = 'http://mp.weixin.qq.com/s?src=3&timestamp=1494410320&ver=1&signature=nAGLXGyESuuT7G69D7Hsq0V4j9SQ5LNxoNpLf2mr0JtntNznT4RrxzYxhvVbyJqlMbpSDPgD9M30SvMtgGIciia07QH76kjWOFqOs2B6ayaaMaHrpsxk*a-Yd*vU4O*E7PgcJrnfvO8bINOdMWuU7w=='