# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import pymysql
import requests
from lxml import etree


if __name__ == "__main__":

    conn = pymysql.connect(host='172.16.1.221', user='chuanghe', password='chuanghe', db='crawl_test', port=3306,
                           charset='utf8')
    cur = conn.cursor()
    sql = "SELECT id,title,content_url,account_name FROM wechat_OfficiaAaccount_ArticleList WHERE status=1"
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    for (id,title,content_url,account_name) in res:
        url = content_url
        res = requests.get(url)
        req = res.content
        selector = etree.HTML(req)
        if id == 10433:
            lines = selector.xpath('//div[@class="rich_media_content "]/descendant::p')
             # print len(lines)
            all_info1 = []
            for line in lines:
                if len(line) == 1:
                    print line[0]


                 # line1 = lines[1]
                 # xx1 = etree.tostring(line1)





        # content = []
        # proxy_lists = selector.xpath('//div[@class="rich_media_content "]/p/descendant::text()')
        # f = lambda x: x.strip()
        # contents_lists = [f(x) for x in proxy_lists]
        # content_list = ''.join(contents_lists)
        # print content_url,content_list

        # f = lambda x: x.strip()
        # contents_lists = [f(x) for x in proxy_lists]
        # content_list = ' '.join(contents_lists)
        # print url,content_list
        # if content_list == '':
        #     proxy_lists1 = selector.xpath('//div[@class="rich_media_content "]/descendant::p')
        #     content_list1 = []
        #     for proxy_list1 in proxy_lists1:
        #         all_texts = proxy_list1.xpath('*/text()')
        #         if all_texts:
        #             if len(all_texts) >= 1:
        #                 for all_text in all_texts:
        #                     content_list1.append(all_text.strip())
        #                     content_list = ''.join(content_list1)
        # print url,content_list




   # 全部string,然后拿下来，再用正则去掉各种符号什么的
   #  selector = etree.HTML(wb_data)
   #  lines = selector.xpath('//div[@class="entry"]/div[@id="entry"]/p')
   #  # print len(lines)
   #  if len(lines)>1:
   #      line1 = lines[1]
   #      xx1 = etree.tostring(line1)







    #########这个是抓取文章不全的
        # proxy_lists = selector.xpath('//div[@class="rich_media_content "]/descendant::p')
        # content_list1 = []
        # for proxy_list in proxy_lists:
        #     all_texts = proxy_list.xpath('*/text()')
        #     if all_texts:
        #         if len(all_texts) >= 1:
        #             for all_text in all_texts:
        #                 content_list1.append(all_text.strip())
        #                 content_list = ''.join(content_list1)
        # print content_url,content_list



















































