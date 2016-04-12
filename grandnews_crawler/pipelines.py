#coding=utf-8

import oss2
import requests
import logging
logger = logging.getLogger(__name__)


class OssPipeline(object):
    
    def __init__(self,endpoint,bucket_name,access_key_id,access_key_secret):
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            endpoint=crawler.settings.get('ALI_OSS_ENDPOINT'),
            bucket_name=crawler.settings.get('BUCKET'),
            access_key_id = crawler.settings.get('ALI_OSS_ACCESS_KEY_ID'),
            access_key_secret = crawler.settings.get('ALI_OSS_ACCESS_KEY_SECRET')
        )

    def open_spider(self, spider):
        self.bucket = oss2.Bucket(self.auth,self.endpoint,self.bucket_name)
        

    def process_item(self, item, spider):
        image_title = item['image_title']
        for i,image in enumerate(item['image_urls']):
            #trick resolve *.jpg.jpg bugs
            if image[-8:] == '.jpg.jpg':
                image = image[:-4]
            input = requests.get(image)
            logger.info("get image %s",image)
            image_name = '%s/%d.jpg' % (image_title,i)
            result = self.bucket.put_object(image_name, input)
            if result.status != 200:
                logger.warning('upload to server error! image_url : %s|bucket : %s|image_index : %d',image, image_title, i)
        logger.debug('upload end %s',image_title)
        return item

        