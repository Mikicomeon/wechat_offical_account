import requests
from lxml import etree
import json
##url='http://mp.weixin.qq.com/mp/getappmsgext?__biz=MjM5MDE0Mjc4MA==&appmsg_type=9&mid=209281297&sn=7678ea70107543ae540eaa92fa243583&idx=1&scene=4&title=%E4%BB%8EPython%E8%BF%81%E7%A7%BB%E5%88%B0Go%EF%BC%8C%E6%80%A7%E8%83%BD%E6%8F%90%E9%AB%98%E4%BA%8610%E5%80%8D%EF%BC%9B%E5%BE%AE%E8%BD%AFAzure%20Event%20Hubs%E5%8D%95%E6%9C%88%E5%A4%84%E7%90%86%E4%BA%A4%E6%98%93%E8%B6%851%E4%B8%87%E4%BA%BF%E6%AC%A1&ct=1444090786&devicetype=android-22&version=&f=json&r=0.6842831603717059&is_need_ad=1&comment_id=3313356094&is_need_reward=0&both_ad=1&reward_uin_count=0&uin=Mjk1MzQ2NDM2&key=f5c31ae61525f82ed2c28511b22576f5a4925a7158a740c0ca3f4398afbf7212492c93f3082648ff8f0d23775d591920&pass_ticket=Ka42VY2tMEGH8wRVgIL55%25252BtcsP6SNueyrtz0FfChL43cCEaJvgOqYfR20ZJmCmbH&wxtoken=4080936236&devicetype=android-22&clientversion=26030838&x5=1'
# urleasy='http://mp.weixin.qq.com/mp/getappmsgext?__biz=MjM5MDE0Mjc4MA==&mid=209281297&sn=7678ea70107543ae540eaa92fa243583&idx=1&uin=Mjk1MzQ2NDM2&key=f5c31ae61525f82e9ef15fb8e372305c3689a0a630dba4864bc8f185bcaf578805470f9a43d191abea8bfc2484eadf8a'
urleasy = 'http://mp.weixin.qq.com/s?__biz=MzA4NjkwNzE2MA==&mid=2650619316&idx=2&sn=f8e1737f2b9adb2da5b4817c1863e19b&chksm=87c81dc3b0bf94d5f86699e1c8f9d13bd4b6e25e81c76d312c1984c279c9fff99f212462042a&scene=30#wechat_redirect'

payload = {'is_only_read': '1', }
headers = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; SCL-AL00 Build/HonorSCL-AL00) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/5.4 TBS/025483 Mobile Safari/533.1 MicroMessenger/6.2.5.53_r2565f18.621 NetType/WIFI Language/zh_CN'}
r = requests.get(urleasy, params=payload, headers=headers)
req = r.content
print req
selector = etree.HTML(req)


