#海贼王吧《Grand News》期刊爬虫

>一直喜欢海贼王，常年混迹贴吧找漫画、找分析贴，偶然发现《Grand News》期刊，发现做的真不错，贴吧浏览体验太烂，自己爬了下图片，做个app方便自己浏览

[TOC]

##简介

![Alt text](https://cloud.githubusercontent.com/assets/1232834/12544413/eb1e9528-c374-11e5-8fa8-a7fcffe7d513.png)

##依赖
- `scrapy` 可以通过`easy_install scrapy`安装
- `requests` 调用http请求，可以通过`easy_install requests`安装
- `oss2` 阿里云oss的python SDK，通过`easy install oss2`安装

##使用方法
```python
git clone https://github.com/ynztyl10/grandnews_crawler.git
cd grandnews_crawler
scrapy crawl grandnews
```

上传图片到oss需要设置一下
```python
BUCKET = 'your-bucket'
# Configure Ali-OSS Storage

# access-key-id
ALI_OSS_ACCESS_KEY_ID = 'your-oss-access-key-id'
# access-key
ALI_OSS_ACCESS_KEY_SECRET = 'your-oss-access-key-secret'
# endpoint
ALI_OSS_ENDPOINT = 'http://your-endpoint'
```
*ps.目前还未设计增量抓取的方式*