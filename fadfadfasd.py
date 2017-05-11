# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymysql
import requests
from lxml import etree
import time
import re
from public.mysqlpooldao import MysqlDao
mysql_dao = MysqlDao()

url = 'http://mp.weixin.qq.com/s?__biz=MzA3NzU2MzkwMg==&mid=200977651&idx=1&sn=eddcde5572fdde432c94a26e79ca6c2d&scene=27#wechat_redirect'
res = requests.get(url)
req = res.content
try:
    match1 = re.search('var msg_cdn_url = "', req)
    start_position = match1.start()
    match2 = re.search("var msg_link", req)
    end_position = match2.end()
    addpicture_img = req[start_position+19: end_position-16]
    add_img = str(addpicture_img).replace('";','').strip()
except:
    print u'页面第一张图'
else:


