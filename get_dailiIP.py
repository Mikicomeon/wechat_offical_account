import urllib2
from bs4 import BeautifulSoup
import csv
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymysql
import requests
from lxml import etree
import re
import time
import json
from public.mysqlpooldao import MysqlDao
mysql_dao = MysqlDao()

def IPspider(numpage):
    csvfile = file('ips.csv', 'wb')
    writer = csv.writer(csvfile)
    url = 'http://www.xicidaili.com/nn/'
    user_agent = 'IP'
    headers = {'User-agent': user_agent}
    for num in xrange(1, numpage + 1):
        ipurl = url + str(num)
        print 'Now downloading the ' + str(num * 100) + ' ips'
        request = urllib2.Request(ipurl, headers=headers)
        content = urllib2.urlopen(request).read()
        bs = BeautifulSoup(content, 'html.parser')
        res = bs.find_all('tr')
        for item in res:
            try:
                temp = []
                tds = item.find_all('td')
                temp.append(tds[1].text.encode('utf-8'))
                temp.append(tds[2].text.encode('utf-8'))
                writer.writerow(temp)
            except IndexError:
                pass




IPspider(10)