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
import pymysql

if __name__ == "__main__":

    conn = pymysql.connect(host='172.16.1.221', user='chuanghe', password='chuanghe', db='crawl_test', port=3306,charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,title,content_time,content_url,account_name FROM wechat_OfficiaAaccount_ArticleList WHERE status_redirect=1"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()

    for (id, title, content_time,content_url, account_name) in res:
        url = content_url
        if url == '':
            sql5 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_redirect`= 0 where (`id`="%s")' % id
            mysql_dao.execute(sql5)
        else:
            if url != u'此篇确实是没有其他信息':
                res = requests.get(url)
                req = res.content
                if (u'此内容因违规无法查看' not in req) and (u'此内容被多人投诉，相关的内容无法进行查看' not in req):
                    # url = 'http://mp.weixin.qq.com/s?__biz=MzAxNzAzMTExOA==&mid=209955884&idx=1&sn=151ceaa8b3bc77eb2c41356988fc780d&scene=27#wechat_redirect'
                    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                               'Accept-Encoding': 'gzip, deflate, sdch',
                               'Accept-Language': 'zh-CN,zh;q=0.8',
                               'Connection': 'keep-alive',
                               'cookie' : 'pgv_pvi=8374003712; dm_login_weixin_scan=',
                               # 'Host': 'pan.baidu.com',
                               'Upgrade-Insecure-Requests': '1',
                               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                    selector = etree.HTML(req)
                    judges = selector.xpath('//div[@class="rich_media_tool"]/a[@class="media_tool_meta meta_primary"]/text()')
                    if judges:
                        judge = judges[0]
                        if judge == u'阅读原文':
                            # print req
                            match1 = re.search(r"var msg_source_url = '", req)
                            start_position = match1.start()
                            match2 = re.search(r"var img_format", req)
                            end_position = match2.end()
                            redirect_urls = req[start_position+22: end_position-14]
                            redirect_url = redirect_urls.replace("';","").strip()
                            # print redirect_url
                            sql3 = ('INSERT IGNORE INTO `wechat_article_redirectUrl`'
                                    '(`title`,`account_name`,`content_url`,`redirect_url`,`content_time`)'
                                    'VALUES ("%s","%s","%s","%s","%s")'
                                    ) % (
                                        title, account_name, content_url, redirect_url, content_time)
                            print sql3
                            try:
                                mysql_dao.execute(sql3)
                            except:
                                print 'error'
                            else:
                                sql4 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_redirect`= 0 where (`id`="%s")' % id
                                mysql_dao.execute(sql4)

                    else:
                        print u'没有阅读原文，既没有可跳转的页面'
                        sql6 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_redirect`= 0 where (`id`="%s")' % id
                        mysql_dao.execute(sql6)


                else:
                    sql1 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_redirect`= 0 where (`id`="%s")' % id
                    mysql_dao.execute(sql1)
            else:
                sql2 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_redirect`= 0 where (`id`="%s")' % id
                mysql_dao.execute(sql2)
