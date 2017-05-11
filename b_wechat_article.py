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


if __name__ == "__main__":

    conn = pymysql.connect(host='172.16.1.221', user='chuanghe', password='chuanghe', db='crawl_test', port=3306,
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,title,content_time,content_url,account_name FROM wechat_OfficiaAaccount_ArticleList WHERE status_article=1"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    for (id, title, content_time,content_url, account_name) in res:
        url = content_url
        # print url
        if url == '':
            sql5 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_article`= "0" where content_url = ""'
            mysql_dao.execute(sql5)
        else:
            if url != u'此篇确实是没有其他信息':
                headers = {
                    'Accept': 'image/webp,image/*,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                }
                # time.sleep(0.5)
                res = requests.get(url,headers=headers)
                req = res.content
                if u'此内容因违规无法查看' not in req:
                    if u'此内容被多人投诉，相关的内容无法进行查看' not in req:
                        if 'id="video"' not in req:
                            match1 = re.search(r'<div class="rich_media_content "', req)
                            start_position = match1.start()
                            match2 = re.search(r'var first_sceen__time', req)
                            end_position = match2.end()
                            json_chuan = req[start_position : end_position - 21]

                            re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
                            re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
                            re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
                            re_br = re.compile('<br\s*?/?>')  # 处理换行
                            re_h = re.compile('</?\w+[^>]*>')  # HTML标签
                            re_comment = re.compile('<!--[^>]*-->')  # HTML注释
                            re_http = re.compile('http:[^>]*html')  # HTML注释
                            s = re_cdata.sub('', json_chuan)  # 去掉CDATA
                            s = re_script.sub('', s)  # 去掉SCRIPT
                            s = re_style.sub('', s)  # 去掉style
                            # s = re_br.sub('\n', s)  # 将br转换为换行
                            s = re_br.sub('', s)  # 将br转换为空
                            s = re_h.sub('', s)  # 去掉HTML 标签
                            s = re_comment.sub('', s)  # 去掉HTML注释
                            contents = re_http.sub('', s)
                            content = contents.replace('var first_sceen__time','').replace('🐇','').replace('❤','').replace('●','').replace('▼','').replace('👀','').replace("'",'').replace('var fir','').replace('&amp;','').replace('  ','').replace('&gt;','').replace('&nbsp;','').replace('🔘','').replace('👇','').replace(u'“','').replace(u'”','').replace(u'"','').strip()
                            sql1 = ('INSERT IGNORE INTO `wechat_article_content`'
                                    '(`title`,`url`,`content`,`content_time`,`account_name`)'
                                    'VALUES ("%s","%s","%s","%s","%s")'
                                    ) % (
                                title, url, content, content_time, account_name)
                            print sql1
                            try:
                                mysql_dao.execute(sql1)
                            except:
                                print 'error'
                            else :
                                sql5 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_article`= "0" where (`id`="%s")' % id
                                mysql_dao.execute(sql5)
                        else:
                            print u'为视频'
                            sql6 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_article`= "0" where (`id`="%s")' % id
                            mysql_dao.execute(sql6)

                    else:
                        print u'被投诉'
                        sql2 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_article`= "0" where (`id`="%s")' %  id
                        mysql_dao.execute(sql2)
                else:
                    print u'违规微信'
                    sql3 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_article`= "0" where (`id`="%s")' % id
                    mysql_dao.execute(sql3)

            else:
                print u'此篇确实是没有其他信息'
                sql4 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_article`= "0" where (`id`="%s")' % id
                mysql_dao.execute(sql4)





































































