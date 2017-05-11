# -*- coding: utf-8 -*-

SECRET_KEY="xxxxxx"

CRAWLER_DEBUG = True

# aliyun oss2, 可以将图片和视频存储到阿里云，也可以选择不存储，爬取速度会更快。 默认不存储。
#OSS2_ENABLE = True
#OSS2_CONFIG = {
#    "ACCESS_KEY_ID": "XXXXXXXXXXXXXX",
#    "ACCESS_KEY_SECRET": "YYYYYYYYYYYYYYYYYYYYYY",
#    "ENDPOINT": "",
#    "BUCKET_DOMAIN": "oss-cn-hangzhou.aliyuncs.com",
#    "BUCKET_NAME": "XXXXX",
#    "IMAGES_PATH": "images/",
#    "VIDEOS_PATH": "videos/",
#    "CDN_DOMAIN": "XXXXXX.oss-cn-hangzhou.aliyuncs.com"
#}
# mysql 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '172.16.1.221',
        'NAME': 'wechatspider',
        'USER': 'chuanghe',
        'PASSWORD': 'chuanghe',
        'OPTIONS':{
            'charset': 'utf8mb4',
        },
    }
}
# redis配置,用于消息队列和k-v存储
REDIS_OPTIONS = {
    'host': 'localhost',
    'port': 6379,
    'password': '',
    'db': 4
}