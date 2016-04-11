#coding=utf-8
from scrapy.linkextractors.lxmlhtml import *
import logging

logger = logging.getLogger('CustomLinkExtractor')


class CustomLinkExtractor(LxmlLinkExtractor):

    def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(),
                 tags=('a', 'area'), attrs=('href',), canonicalize=True,
                 unique=True, process_value=None, deny_extensions=None, restrict_css=(), custom_param_str=None):
        tags, attrs = set(arg_to_iter(tags)), set(arg_to_iter(attrs))
        tag_func = lambda x: x in tags
        attr_func = lambda x: x in attrs
        lx = LxmlParserLinkExtractor(tag=tag_func, attr=attr_func,
            unique=unique, process=process_value)
        self.custom_param_str = custom_param_str

        super(LxmlLinkExtractor, self).__init__(lx, allow=allow, deny=deny,
            allow_domains=allow_domains, deny_domains=deny_domains,
            restrict_xpaths=restrict_xpaths, restrict_css=restrict_css,
            canonicalize=canonicalize, deny_extensions=deny_extensions)

    def extract_links(self, response):
        base_url = get_base_url(response)
        if self.restrict_xpaths:
            docs = [subdoc
                    for x in self.restrict_xpaths
                    for subdoc in response.xpath(x)]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        if self.custom_param_str:
            for i in xrange(0,len(all_links)):
                all_links[i].url = all_links[i].url + "?" + self.custom_param_str if "?" not in all_links[i].url else all_links[i].url + "&" + self.custom_param_str
        return unique_list(all_links)

