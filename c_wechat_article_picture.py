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
    sql = "SELECT id,title,content_time,content_url,account_name FROM wechat_OfficiaAaccount_ArticleList WHERE status_picture=1"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()

    for (id, title, content_time, content_url, account_name) in res:
        url = content_url
        print id,url
        if url != u'此篇确实是没有其他信息' and url != '':
            res = requests.get(url)
            req = res.content

            try:
                match1 = re.search('var msg_cdn_url = "', req)
                start_position = match1.start()
                match2 = re.search("var msg_link", req)
                end_position = match2.end()
                addpicture_img = req[start_position + 19: end_position - 16]
                add_img = str(addpicture_img).replace('";', '').strip()
            except:
                print u'页面第一张图'
            else:
                sql19 = ('INSERT IGNORE INTO `wechat_article_picture`'
                         '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                         'VALUES ("%s","%s","%s","%s","%s")'
                         ) % (
                            title, add_img, url, content_time, account_name)
                print sql19
                mysql_dao.execute(sql19)

            if (u'此内容因违规无法查看' not in req) and (u'此内容被多人投诉，相关的内容无法进行查看' not in req) :

                selector = etree.HTML(req)
                picture_sources = selector.xpath('//div[@class="rich_media_content "]/section[@data-role="outer"]/section[@data-role="outer"]')
                imag_sources = selector.xpath('//div[@class="rich_media_content "]/p')
                third_sources = selector.xpath('//div[@class="rich_media_content "]/section[@data-role="outer"]/section[@data-role="outer"]/section[@data-role="outer"]/section[@data-role="outer"]/p')
                fourth_sources = selector.xpath('//div[@class="rich_media_content "]/section/p')
                fifth_sources = selector.xpath('//div[@class="rich_media_content "]/section[@data-role="outer"]/section[@data-role="outer"]/section[@data-role="outer"]/section[@data-role="outer"]/section[@data-role="outer"]/section[@data-role="outer"]/p')
                try:
                    if picture_sources:
                        picture_source = picture_sources[0].xpath('section/p')
                        # print len(picture_source)
                        for picture in picture_source:
                            pictures1 = picture.xpath('img/@src')
                            pictures2 = picture.xpath('img/@data-src')
                            pictures3 = picture.xpath('span/img/@src')
                            pictures4 = picture.xpath('span/img/@data-src')
                            if pictures1:
                                picture1 = pictures1[0]
                                # print picture1
                                sql1 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, picture1, url, content_time, account_name)
                                print sql1
                                mysql_dao.execute(sql1)
                            if pictures2:
                                picture2 = pictures2[0]
                                # print picture2
                                sql2 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, picture2, url, content_time, account_name)
                                print sql2
                                mysql_dao.execute(sql2)
                            if pictures3:
                                picture3 = pictures3[0]
                                # print picture1
                                sql7 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, picture3, url, content_time, account_name)
                                print sql7
                                mysql_dao.execute(sql7)
                            if pictures4:
                                picture4 = pictures4[0]
                                # print picture1
                                sql8 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, picture4, url, content_time, account_name)
                                print sql8
                                mysql_dao.execute(sql8)


                    if imag_sources:
                        for imag_source in imag_sources:
                            images1 = imag_source.xpath('img/@src')
                            images2 = imag_source.xpath('img/@data-src')
                            images3 = imag_source.xpath('span/img/@src')
                            images4 = imag_source.xpath('span/img/@data-src')
                            if images1:
                                image1 = images1[0]
                                # print image1
                                sql3 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, image1, url, content_time, account_name)
                                print sql3
                                mysql_dao.execute(sql3)
                            if images2:
                                image2 = images2[0]
                                # print image2
                                sql4 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, image2, url, content_time, account_name)
                                print sql4
                                mysql_dao.execute(sql4)
                            if images3:
                                image3 = images3[0]
                                # print image1
                                sql9 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, image3, url, content_time, account_name)
                                print sql9
                                mysql_dao.execute(sql9)
                            if images4:
                                image4 = images4[0]
                                # print image2
                                sql10 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, image4, url, content_time, account_name)
                                print sql10
                                mysql_dao.execute(sql10)
                    if third_sources:
                        for third_source in third_sources:
                            thirds1 = third_source.xpath('img/@src')
                            thirds2 = third_source.xpath('img/@data-src')
                            thirds3 = third_source.xpath('span/img/@src')
                            thirds4 = third_source.xpath('span/img/@data-src')
                            if thirds1:
                                third1 = thirds1[0]
                                # print image1
                                sql11 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, third1, url, content_time, account_name)
                                print sql11
                                mysql_dao.execute(sql11)
                            if thirds2:
                                third2 = thirds2[0]
                                # print image2
                                sql12 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, third2, url, content_time, account_name)
                                print sql12
                                mysql_dao.execute(sql12)
                            if thirds3:
                                third3 = thirds3[0]
                                # print image1
                                sql13 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, third3, url, content_time, account_name)
                                print sql13
                                mysql_dao.execute(sql13)
                            if thirds4:
                                third4 = thirds4[0]
                                # print image2
                                sql14 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, third4, url, content_time, account_name)
                                print sql14
                                mysql_dao.execute(sql14)
                    if fourth_sources:
                        for fourth_source in fourth_sources:
                            fourths1 = fourth_source.xpath('img/@src')
                            fourths2 = fourth_source.xpath('img/@data-src')
                            fourths3 = fourth_source.xpath('span/img/@src')
                            fourths4 = fourth_source.xpath('span/img/@data-src')
                            if fourths1:
                                fourth1 = fourths1[0]
                                # print image1
                                sql15 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fourth1, url, content_time, account_name)
                                print sql15
                                mysql_dao.execute(sql15)
                            if fourths2:
                                fourth2 = fourths2[0]
                                # print image2
                                sql16 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fourth2, url, content_time, account_name)
                                print sql16
                                mysql_dao.execute(sql16)
                            if fourths3:
                                fourth3 = fourths3[0]
                                # print image1
                                sql17 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fourth3, url, content_time, account_name)
                                print sql17
                                mysql_dao.execute(sql17)
                            if fourths4:
                                fourth4 = fourths4[0]
                                # print image2
                                sql18 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fourth4, url, content_time, account_name)
                                print sql18
                                mysql_dao.execute(sql18)
                    if fifth_sources:
                        for fifth_source in fifth_sources:
                            fifths1 = fifth_source.xpath('img/@src')
                            fifths2 = fifth_source.xpath('img/@data-src')
                            fifths3 = fifth_source.xpath('span/img/@src')
                            fifths4 = fifth_source.xpath('span/img/@data-src')
                            if fifths1:
                                fifth1 = fifths1[0]
                                # print image1
                                sql22 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fifth1, url, content_time, account_name)
                                print sql22
                                mysql_dao.execute(sql22)
                            if fifths2:
                                fifth2 = fifths2[0]
                                # print image2
                                sql23 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fifth2, url, content_time, account_name)
                                print sql23
                                mysql_dao.execute(sql23)
                            if fifths3:
                                fifth3 = fifths3[0]
                                # print image1
                                sql24 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fifth3, url, content_time, account_name)
                                print sql24
                                mysql_dao.execute(sql24)
                            if fifths4:
                                fifth4 = fifths4[0]
                                # print image2
                                sql25 = ('INSERT IGNORE INTO `wechat_article_picture`'
                                        '(`title`,`imag_url`,`news_url`,`content_time`,`account_name`)'
                                        'VALUES ("%s","%s","%s","%s","%s")'
                                        ) % (
                                           title, fifth4, url, content_time, account_name)
                                print sql25
                                mysql_dao.execute(sql25)
                except:
                    print 'error'
                else:
                    sql = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_picture`= 0 where (`id`="%s")' % id
                    mysql_dao.execute(sql)
            else:
                sql6 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_picture`= 0 where (`id`="%s")' % id
                mysql_dao.execute(sql6)

        else:
            sql5 = 'UPDATE `wechat_OfficiaAaccount_ArticleList` set `status_picture`= 0 where (`id`="%s")' % id
            mysql_dao.execute(sql5)


