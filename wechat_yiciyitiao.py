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
    while True:
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
            'cookie' : 'wxtokenkey=375f0f10a05c2270b63d380f5f674dee324b5d28744cfa94f032c6ddcf5b0b3b; wxticket=2890078309; wxticketkey=d91b424ae28371030e9d8ccfc68089ff324b5d28744cfa94f032c6ddcf5b0b3b; wap_sid=CKSZkvIBEkA3TVhUTnFITFBlTXVJTGFtMy1QTkkteV90UmViQ3NuUEJYM0hBWFpOOVFKTkxVYVpQMGhTRVJxczJJcEpMaWM5GAQgpBQoteTi9wgw8O/EyAU=; wap_sid2=CKSZkvIBElx2eWFuVlFEODdVbTk2YVplR2VGVktoZlBIWUFaTlpMM2FaSy1nc1EzYTZKVFc4S0t2WmdHUm84b0RDdW5jYlR3SVFpRGRyN0RGd3BvbndORXNEMzVqb2NEQUFBfjDw78TIBQ==; pass_ticket=JQMpooOj50E19uV6QLmqdlIY/y4Lw66kdcNBPRtpCm1k9uBj875XYnrQgMyrpugR'
            # 'cookie': 'wxtokenkey=375f0f10a05c2270b63d380f5f674dee324b5d28744cfa94f032c6ddcf5b0b3b; wxticket=2890078309; wxticketkey=d91b424ae28371030e9d8ccfc68089ff324b5d28744cfa94f032c6ddcf5b0b3b; wap_sid=CKSZkvIBEkBMRTFrTUJNckVoYm1tczgzSllvNE9Ta21UTkJoemdhX1E2WjU1SVVtME4xTXNZc3p3V0pVWE5Pa3NkZldlMzBSGAQgpBQoteTi9wgw4e7EyAU=; wap_sid2=CKSZkvIBElx2eWFuVlFEODdVbTk2YVplR2VGVktyMnpMejQzQXJMTnZDWW5kWER2eFBZZGpqYXRYUHVRbTI0dzM2eEw4QUdFemlYQy10RnZrWXY3RTBzbmhOZlMtWWNEQUFBfjDh7sTIBQ==; pass_ticket=JQMpooOj50E19uV6QLmqdlIY/y4Lw66kdcNBPRtpCm1k9uBj875XYnrQgMyrpugR'
        }
        time.sleep(3)
        res = requests.get(url,headers=headers)
        print url
        req = res.content
        json_list = req.replace('\\','').replace('amp;','').replace('&quot;','').replace('&gt;','')
        print json_list

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
            title = content_time = content_url = ''
            content_time1 = proxy_list['comm_msg_info']['datetime']
            time_local = time.localtime(int(content_time1))  ######time.struct_time(tm_year=2017, tm_mon=5, tm_mday=4, tm_hour=17, tm_min=34, tm_sec=38, tm_wday=3, tm_yday=124, tm_isdst=0)
            content_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 2017-05-04 17:34:38
            title = proxy_list['app_msg_ext_info']['title']
            content_url = proxy_list['app_msg_ext_info']['content_url']

            # print account_name, biz, title, content_time, content_url

            sql2 = ('INSERT IGNORE INTO `wechat_OfficiaAaccount_ArticleList`'
                           '(`account_name`,`account_biz`,`title`,`content_time`,`content_url`)'
                           'VALUES ("%s","%s","%s","%s","%s")'
                           ) % (
                                account_name, biz, title, content_time, content_url)
            print sql2
            mysql_dao.execute(sql2)


        get_nextpageInfo(account_name,biz,pass_ticket,nextpage_id)

        #
        #     titles = re.findall('"title":"(.*?)",', nextpage_json_chuanchuan)
        #     content_times = re.findall('"datetime":(.*?),', nextpage_json_chuanchuan)
        #
        #
        #
        #     content_urls = re.findall('"content_url":"(.*?)",', nextpage_json_chuanchuan)
        #
        #     for title,content_time1,content_url in zip(titles,content_times,content_urls):
        #
        #         time_local = time.localtime(int(content_time1))  ######time.struct_time(tm_year=2017, tm_mon=5, tm_mday=4, tm_hour=17, tm_min=34, tm_sec=38, tm_wday=3, tm_yday=124, tm_isdst=0)
        #         content_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)  # 2017-05-04 17:34:38
        #
        #         # print account_name,biz,title,content_time,content_url
        #         sql2 = ('INSERT IGNORE INTO `wechat_OfficiaAaccount_ArticleList`'
        #                '(`account_name`,`account_biz`,`title`,`content_time`,`content_url`)'
        #                'VALUES ("%s","%s","%s","%s","%s")'
        #                ) % (
        #                     account_name, biz, title, content_time, content_url)
        #         print sql2
        #         mysql_dao.execute(sql2)
        #
        #     nextpage_ids = re.findall('"id":(.*?),"', nextpage_json_chuanchuan)
        #     nextpage_id = nextpage_ids[-1]
        #
        #
        #     get_nextpageInfo(account_name,biz,pass_ticket,nextpage_id)
        # else:
        #     break







if __name__ == '__main__':
    # url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA3NzU2MzkwMg==&scene=124&devicetype=android-22&version=26050733&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=x8NlFcxzx9sBsNiiiZ6%2BY2nHeUQIm7Y%2BuDngnJA8SKTmsvTwLgFGo1Jaj616swOu&wx_header=1'
    url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5ODY2MzIyMQ==&scene=124&devicetype=android-22&version=26050733&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=JQMpooOj50E19uV6QLmqdlIY%2Fy4Lw66kdcNBPRtpCm1k9uBj875XYnrQgMyrpugR&wx_header=1'
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1; OPPO R9m Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043220 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/WIFI Language/zh_CN',
        'x-wechat-uin': 'NTA3ODA4OTMy',
        'x-wechat-key': '3d2888d0bfda9d5e2883eaac49215d0a777872697db0aaef56603dbab58c59056bdc8f196b97222b3f42baaf93c554563bb2a0917295a78f92c2ee74b34e1e4a5c1e3737c7d949f9497787270e9846e1',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/sharpp,*/*;q=0.8",
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        # 'Cookie': 'rewardsn=36e7d6fe2704515124c4; wxtokenkey=8e2316a6101f11f2b67511578047f5434c015569fde23f75d5256459a845c5a2; wxticket=2705568732; wxticketkey=7104693cb5e79b7a92e6194923c42c9c4c015569fde23f75d5256459a845c5a2; wap_sid=CKy6+dgCEkBMR0xTVWdOSG9MVjE5X3RwTVg0VWF0X2FuMFpDMVdadmlSb3hMMmw2ZmFUQXJmTW9LVzlReDlBZHowMEZvUzhpGAQg/REo/su/uwswmYHAyAU=; wap_sid2=CKy6+dgCEnB0MERVVEgwSThPeWVuUjd6QkdDYkhwaDQyeGc1RXR4Q2dlUEJhTU9UQzNCQW80YTgyQ2RHc0F2NjFzdnIwSjBWUThYZzJlZ3JMdU5JdEV2TE9hX1Z5b3lGcVhoLXRjN21uYXVaUTlUVjNpaUhBd0FBMJmBwMgF; pass_ticket=foYQOvBQnETExafe41ehqBy4KJAuVfvChZlQQD2UBk7/MvgL0WEg8J4IPjfBefbS',
        'cookie': 'wxtokenkey=375f0f10a05c2270b63d380f5f674dee324b5d28744cfa94f032c6ddcf5b0b3b; wxticket=2890078309; wxticketkey=d91b424ae28371030e9d8ccfc68089ff324b5d28744cfa94f032c6ddcf5b0b3b; wap_sid=CKSZkvIBEkBlSzAzTGxwdGdPSU42N3VENzc5TUlKVWI5cVRPYXBoVGZCdWdCd0hiU0JnRUdRTWk3OUFsSlNNaVlwTXJZRmlBGAQg/REoteTi9wgw4O7EyAU=; wap_sid2=CKSZkvIBElx2eWFuVlFEODdVbTk2YVplR2VGVktsbUtxbmFoT0xoV2tLR2xxV2wxbTVmU3BMUVdvTTJ5OGFtdHFTNmRjNVpDZWhpY0dES1ZNQmUzV3l0UHJLbkZVb2NEQUFBfjDg7sTIBQ==; pass_ticket=JQMpooOj50E19uV6QLmqdlIY/y4Lw66kdcNBPRtpCm1k9uBj875XYnrQgMyrpugR',
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



    get_nextpageInfo(account_name,biz,pass_ticket,nextpage_id)