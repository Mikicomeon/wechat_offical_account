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
import json



def get_nextpageInfo(account_name,biz,pass_ticket,nextpage_id):
    print '============================================='
    url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=' + biz + '&f=json&frommsgid=' + nextpage_id + '&count=10&scene=124&is_ok=1&uin=777&key=777&pass_ticket=' + pass_ticket + '&wxtoken=&x5=1&f=json'
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'X-Requested-With' : 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/WIFI Language/zh_CN',
        'Accept': "*/*",
        # 'Referer' : 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA3NzU2MzkwMg==&scene=124&devicetype=android-22&version=26050733&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=foYQOvBQnETExafe41ehqBy4KJAuVfvChZlQQD2UBk7%2FMvgL0WEg8J4IPjfBefbS&wx_header=1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'cookie' : 'wxtokenkey=4ab5869c6253e4e2993cef6a2e2bb9d3f4a75c61037a8cbfa7bc58f18f75ab0a; wxticket=1584902625; wxticketkey=40e1e63343592f614fbf6a5305030d17f4a75c61037a8cbfa7bc58f18f75ab0a; rewardsn=aaf9608db19a1ddab19a; wap_sid=CKy6+dgCEkB4ZndjRHNxWDFLUzd0b3d4eTFQWlJ6ekdsQy16TVpuN3I2MjBUOGQyenZ6a3F5RXdGLXNwLTlkSXlxb3c1SWtBGAQgpBQon4SM9ggw4KHPyAU=; wap_sid2=CKy6+dgCElwybUhHWDNSY1c5Ml85YlEyWmNtVjVDOEJFdWIzTTBDMlZuQmR1aXlscTBHN0M5bGRfWkN0V2lwOXdqQlZESkdCYTl1MERmRmJHNzkwMTVrSjBXX2phWWdEQUFBfjDgoc/IBQ==; pass_ticket=3ctNc/GTSQstHj09GWDO0fLMkoyiW5m3SeBR+e1Qy4xLLDJMt77aFR8SO8Ru5CBK'
        # 'cookie': 'wxtokenkey=375f0f10a05c2270b63d380f5f674dee324b5d28744cfa94f032c6ddcf5b0b3b; wxticket=2890078309; wxticketkey=d91b424ae28371030e9d8ccfc68089ff324b5d28744cfa94f032c6ddcf5b0b3b; wap_sid=CKSZkvIBEkBMRTFrTUJNckVoYm1tczgzSllvNE9Ta21UTkJoemdhX1E2WjU1SVVtME4xTXNZc3p3V0pVWE5Pa3NkZldlMzBSGAQgpBQoteTi9wgw4e7EyAU=; wap_sid2=CKSZkvIBElx2eWFuVlFEODdVbTk2YVplR2VGVktyMnpMejQzQXJMTnZDWW5kWER2eFBZZGpqYXRYUHVRbTI0dzM2eEw4QUdFemlYQy10RnZrWXY3RTBzbmhOZlMtWWNEQUFBfjDh7sTIBQ==; pass_ticket=JQMpooOj50E19uV6QLmqdlIY/y4Lw66kdcNBPRtpCm1k9uBj875XYnrQgMyrpugR'
    }
    time.sleep(3)
    res = requests.get(url,headers=headers)
    print url
    req = res.content
    json_list = req.replace('\\','').replace('amp;','').replace('&quot;','').replace('&gt;','')
    print json_list
    if re.findall('"msg_count":0',json_list):
        print u'结束采集'

    else:
        match1 = re.search(r'{"list":', json_list)
        start_position = match1.start()
        match2 = re.search(r'}]}"}', json_list)
        end_position = match2.end()
        nextpage_json = json_list[start_position : end_position - 2]
        nextpage_json_chuanchuan1 = nextpage_json.replace('&quot;', '').replace('&nbsp;', '')
        print nextpage_json_chuanchuan1
        nextpage_json_chuanchuan = json.loads(nextpage_json_chuanchuan1)
        proxy_lists = nextpage_json_chuanchuan['list']

        nextpage_id_lists = []
        for nextpage_ids in proxy_lists:
            nextpage_id_single = nextpage_ids['comm_msg_info']['id']
            nextpage_id_lists.append(nextpage_id_single)
        nextpage_id = str(nextpage_id_lists[-1])

        for proxy_list in proxy_lists:
            if re.findall('app_msg_ext_info',str(proxy_list)):
                title = content_time = content_url = ''
                #####content_time两部分公用
                content_time1 = proxy_list['comm_msg_info']['datetime']
                time_local = time.localtime(int(content_time1))  ######time.struct_time(tm_year=2017, tm_mon=5, tm_mday=4, tm_hour=17, tm_min=34, tm_sec=38, tm_wday=3, tm_yday=124, tm_isdst=0)
                content_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 2017-05-04 17:34:38

                ###########第一部分
                title = proxy_list['app_msg_ext_info']['title']
                title = str(title).replace('&amp;','').replace('quot;','')
                content_url = proxy_list['app_msg_ext_info']['content_url']
                # print account_name, biz, title, content_time, content_url

                sql2 = ('INSERT IGNORE INTO `wechat_OfficiaAaccount_ArticleList`'
                               '(`account_name`,`account_biz`,`title`,`content_time`,`content_url`)'
                               'VALUES ("%s","%s","%s","%s","%s")'
                               ) % (
                                    account_name, biz, title, content_time, content_url)
                print sql2
                mysql_dao.execute(sql2)

                ############第二部分
                second_part_areas = proxy_list['app_msg_ext_info']['multi_app_msg_item_list']
                #####等下看看是否有空的
                for second_part_area in second_part_areas:
                    sub_title = sub_content_time = sub_content_url = ''
                    sub_title = second_part_area['title']
                    sub_content_time = content_time
                    sub_content_url = second_part_area['content_url']
                    sql3 = ('INSERT IGNORE INTO `wechat_OfficiaAaccount_ArticleList`'
                            '(`account_name`,`account_biz`,`title`,`content_time`,`content_url`)'
                            'VALUES ("%s","%s","%s","%s","%s")'
                            ) % (
                               account_name, biz, sub_title, sub_content_time, sub_content_url)
                    print sql3
                    mysql_dao.execute(sql3)
            else:
                content_time = title = url = ''
                content_time1 = proxy_list['comm_msg_info']['datetime']
                time_local = time.localtime(int(content_time1))  ######time.struct_time(tm_year=2017, tm_mon=5, tm_mday=4, tm_hour=17, tm_min=34, tm_sec=38, tm_wday=3, tm_yday=124, tm_isdst=0)
                content_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 2017-05-04 17:34:38
                title = proxy_list['comm_msg_info']['content']
                content_url = u'此篇确实是没有其他信息'
                sql4 = ('INSERT IGNORE INTO `wechat_OfficiaAaccount_ArticleList`'
                        '(`account_name`,`account_biz`,`title`,`content_time`,`content_url`)'
                        'VALUES ("%s","%s","%s","%s","%s")'
                        ) % (
                           account_name, biz, title, content_time, content_url)
                print sql4
                mysql_dao.execute(sql4)

        get_nextpageInfo(account_name, biz, pass_ticket, nextpage_id)



if __name__ == '__main__':
    url = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz=MjM5NTE0NDczNQ==&devicetype=android-22&version=26050733&lang=zh_CN&nettype=WIFI&ascene=3&pass_ticket=3ctNc%2FGTSQstHj09GWDO0fLMkoyiW5m3SeBR%2Be1Qy4xLLDJMt77aFR8SO8Ru5CBK&wx_header=1'
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/WIFI Language/zh_CN',
        'x-wechat-uin': 'NzIzNDEwMjIw',
        'x-wechat-key': '8b4eac29ab45a16cb4bb569a43b8fad4b3cc8da5867980f4d2619fb95262b89e266057d0e45ba3ebabc66207b5fdb69da00977c265cf21df9bca475500a158bff46ade1b4ef3f76327d732bbcb16bf3c',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/sharpp,*/*;q=0.8",
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        # 'Cookie': 'rewardsn=36e7d6fe2704515124c4; wxtokenkey=8e2316a6101f11f2b67511578047f5434c015569fde23f75d5256459a845c5a2; wxticket=2705568732; wxticketkey=7104693cb5e79b7a92e6194923c42c9c4c015569fde23f75d5256459a845c5a2; wap_sid=CKy6+dgCEkBMR0xTVWdOSG9MVjE5X3RwTVg0VWF0X2FuMFpDMVdadmlSb3hMMmw2ZmFUQXJmTW9LVzlReDlBZHowMEZvUzhpGAQg/REo/su/uwswmYHAyAU=; wap_sid2=CKy6+dgCEnB0MERVVEgwSThPeWVuUjd6QkdDYkhwaDQyeGc1RXR4Q2dlUEJhTU9UQzNCQW80YTgyQ2RHc0F2NjFzdnIwSjBWUThYZzJlZ3JMdU5JdEV2TE9hX1Z5b3lGcVhoLXRjN21uYXVaUTlUVjNpaUhBd0FBMJmBwMgF; pass_ticket=foYQOvBQnETExafe41ehqBy4KJAuVfvChZlQQD2UBk7/MvgL0WEg8J4IPjfBefbS',
        'cookie': 'wxtokenkey=4ab5869c6253e4e2993cef6a2e2bb9d3f4a75c61037a8cbfa7bc58f18f75ab0a; wxticket=1584902625; wxticketkey=40e1e63343592f614fbf6a5305030d17f4a75c61037a8cbfa7bc58f18f75ab0a; wap_sid=CKy6+dgCEkBENzJFSGVadGxzU1JHejNjbjZ0M0ppWXEyQ0Voek9MSzVJOUFfU2pkMUQxMy1wb1g5M3lNdDNrSVRhOVYxSEQzGAQg/BEoocPEnAwwp4TPyAU=; wap_sid2=CKy6+dgCElxhVTBESEhjUEtnbWVRZDhBcWhQcVQtOEkwMnlBYzgwdTdocXJNOGgtRFRqbVRKa0w0ZlpDeHR5QUFnaVJaQ0h4ZmxaRWVNNFVtVWdtVEpNZkNTUXlxSWdEQUFBfjCnhM/IBQ==; pass_ticket=3ctNc/GTSQstHj09GWDO0fLMkoyiW5m3SeBR+e1Qy4xLLDJMt77aFR8SO8Ru5CBK; rewardsn=aaf9608db19a1ddab19a',
        'Q-UA2': 'QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.7&TBSVC=43101&CO=BK&COVC=043220&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= OPPOR9m &RL=1080*1920&OS=5.1&API=22',
        'Q-GUID': '418422abad49d5cdf489bc8f13b788cb',
        'Q-Auth': '31045b957cf33acf31e40be2f3e71c5217597676a9729f1b'
    }
    res = requests.get(url, headers=headers)
    req1 = res.text
    req = req1.encode('utf-8')

    account_name = ''
    selector = etree.HTML(req)
    account_names = selector.xpath('//div[@class="profile_info appmsg"]/strong[@class="profile_nickname"]/text()')
    if account_names:
        account_name = account_names[0].strip()

    match1 = re.search(r"var msgList = '", req)
    start_position = match1.start()
    match2 = re.search(r"}]}'", req)
    end_position = match2.end()
    json_chuan = req[start_position + 15: end_position - 1]
    json_chuanchuan = json_chuan.replace('&quot;','').replace('&nbsp;','')
    print json_chuanchuan
    # print json_chuanchuan
    titles = re.findall('title:(.*?),digest:', json_chuanchuan)
    content_times = re.findall('datetime:(.*?),', json_chuanchuan)
    content_urls = re.findall('content_url:(.*?),source_url:',json_chuanchuan)

    bizs = re.findall('__biz=(.*?)&', url)
    biz = bizs[0]
    pass_tickets = re.findall('pass_ticket=(.*?)&', url)
    pass_ticket = pass_tickets[0]
    nextpage_ids = re.findall('comm_msg_info:{id:(.*?),', json_chuanchuan)
    nextpage_id = nextpage_ids[-1]

    for title,content_time1,content_url in zip(titles,content_times,content_urls):
        content_url = content_url.replace('\\','').replace('amp;amp;','')
        time_local = time.localtime(int(content_time1))   ######time.struct_time(tm_year=2017, tm_mon=5, tm_mday=4, tm_hour=17, tm_min=34, tm_sec=38, tm_wday=3, tm_yday=124, tm_isdst=0)
        content_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 2017-05-04 17:34:38


        # print account_name,biz,title,content_time,content_url
        sql1 = ('INSERT IGNORE INTO `wechat_OfficiaAaccount_ArticleList`'
                '(`account_name`,`account_biz`,`title`,`content_time`,`content_url`)'
                'VALUES ("%s","%s","%s","%s","%s")'
                ) % (
                   account_name, biz, title, content_time, content_url)
        print sql1
        mysql_dao.execute(sql1)



    # get_nextpageInfo(account_name,biz,pass_ticket,nextpage_id)