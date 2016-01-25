# coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import re
import requests
import logging

from grandnews_crawler.items import GrandnewsCrawlerItem
from grandnews_crawler.cnnum import getResultForDigit

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename='spider.log',
                    filemode='a')
logger = logging.getLogger('spider')
thread_title_re = re.compile("【Grand news】.*")
vol_re = re.compile(ur"【Grand news】\s*第(.*)期")
thread_url_css = "a::attr(href)"
title_css = "h3.core_title_txt::attr(title)"
image_css = "img.BDE_Image::attr(src)"


class GrandNewsTiebaSpider(Spider):
    name = "grandnews"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        # 'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=0',
        # 'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=50',
        # 'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=100',
        # 'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=150',
        # 'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=200',
        # 'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=250',
        # 'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=300'
        'http://tieba.baidu.com/p/805618862?see_lz=1',
        'http://tieba.baidu.com/p/752375721?see_lz=1',
        'http://tieba.baidu.com/p/758880583?see_lz=1',
        'http://tieba.baidu.com/p/768687800?see_lz=1',
        'http://tieba.baidu.com/p/773089292?see_lz=1',
        'http://tieba.baidu.com/p/3611695733?see_lz=1',
        'http://tieba.baidu.com/p/898425330?see_lz=1',
        'http://tieba.baidu.com/p/898389531?see_lz=1',
        'http://tieba.baidu.com/p/2553826185?see_lz=1',
        'http://tieba.baidu.com/p/2569886025?see_lz=1',
        'http://tieba.baidu.com/p/2582843482?see_lz=1',
        'http://tieba.baidu.com/p/2595279287?see_lz=1',
        'http://tieba.baidu.com/p/2635772340?see_lz=1',
        'http://tieba.baidu.com/p/1730003924?see_lz=1',
        'http://tieba.baidu.com/p/1758514459?see_lz=1',
        'http://tieba.baidu.com/p/1773721870?see_lz=1',
        'http://tieba.baidu.com/p/1804208211?see_lz=1',
        'http://tieba.baidu.com/p/1823036846?see_lz=1',
        'http://tieba.baidu.com/p/1836845578?see_lz=1',
        'http://tieba.baidu.com/p/1853327606?see_lz=1',
        'http://tieba.baidu.com/p/1865960239?see_lz=1',
        'http://tieba.baidu.com/p/1880276165?see_lz=1',
        'http://tieba.baidu.com/p/2050607285?see_lz=1',
        'http://tieba.baidu.com/p/2063218336?see_lz=1'
    ]

    # def parse(self, response):
    #     for href in response.css("a.j_th_tit"):
    #         thread_url = self.get_grandnews_thread_url(href)
    #         if thread_url:
    #             post_url = response.urljoin(thread_url + "?see_lz=1")
    #             yield Request(post_url, callback=self.parse_post_content)

    def get_grandnews_thread_url(self, href):
        text = thread_title_re.findall(href.extract().encode('utf-8'))
        if text:
            thread_url = href.css(thread_url_css).extract()[0]
            return thread_url

    def parse(self, response):
        item = GrandnewsCrawlerItem()
        title = response.css(title_css).extract()[0]
        item['title'] = title
        image_title_cn = vol_re.findall(title)
        image_title_num = getResultForDigit(image_title_cn[0])
        image_urls = response.css(image_css).extract()
        item['image_title'] = 'grandnews_%s' % image_title_num
        item['image_urls'] = image_urls
        return item
