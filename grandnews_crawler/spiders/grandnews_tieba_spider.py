# coding=utf-8
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
import re
import requests
import logging

from grandnews_crawler.linkextractors import CustomLinkExtractor
from grandnews_crawler.items import GrandnewsCrawlerItem
from grandnews_crawler.cnnum import getResultForDigit

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s',
                    datefmt='%m-%d %H:%M:%S',
                    filename='spider.log',
                    filemode='a')
logger = logging.getLogger('spider')
vol_re = re.compile(ur"【Grand news】\s*第(.*)期")#特刊暂时忽略，目前仅有两个特刊
title_css = "h3.core_title_txt::attr(title)"
image_css = "img.BDE_Image::attr(src)"
scan_num_xpath = "//div[@id='thread_theme_5']//li[@class='l_reply_num'][1]/span[@class='red'][1]/text()"
pb_next_page_xpath = u"//li[@class='l_pager pager_theme_5 pb_list_pager']/a[contains(text(),'下一页')]//attribute::href"


class GrandNewsTiebaSpider(CrawlSpider):
    name = "grandnews"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = [
        #'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=0'
        'http://tieba.baidu.com/f?kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B&ie=utf-8&tab=good&cid=4&pn=0'
    ]
    rules = (
            Rule(CustomLinkExtractor(restrict_xpaths=(u'//a[starts-with(@title,"【Grand news】")]',),custom_param_str='?see_lz=1')
            , callback='parse_post_content'),
            Rule (CustomLinkExtractor(restrict_xpaths=(u'//a[text()="下一页"]',),custom_param_str='see_lz=1')
            , follow= True),
        )

    def parse_post_content(self, response):
        item = GrandnewsCrawlerItem()
        title = response.css(title_css).extract()[0]
        scan_num = response.xpath(scan_num_xpath).extract()[0]
        item['scan_num'] = scan_num
        item['title'] = title
        image_title_cn = vol_re.findall(title)
        image_title_num = getResultForDigit(image_title_cn[0])
        image_urls = response.css(image_css).extract()
        item['image_title'] = 'grandnews_%s' % image_title_num
        logger.info("vols.%s|vols_num:%s",item['image_title'],image_title_num)
        item['image_urls'] = image_urls
        pb_next_page_href = response.xpath(pb_next_page_xpath)
        if len(pb_next_page_href) > 0:
            for href in pb_next_page_href:
                url = response.urljoin(href.extract()+ "?see_lz=1")
                yield Request(url, callback=self.parse_post_next_page_content, meta={"item":item})

        yield item

    def parse_post_next_page_content(self, response):
        item = response.meta['item']
        image_urls = response.css(image_css).extract()
        item['image_urls'].extend(image_urls)
        return item


