# -*- coding: utf-8 -*-
import pymongo
from scrapy.utils.project import get_project_settings
import redis
import json


class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self):
        project_settings = get_project_settings()
        self.mongo_uri = project_settings.get('MONGO_URI')
        self.mongo_db = project_settings.get('MONGO_DATABASE', 'items')
        self.redis = redis.Redis(host='redis', port=6379, db=0)
        # self.pub = self.redis.pubsub()

    # @classmethod
    # def from_crawler(cls, crawler):
    #     print(crawler.settings.get('MONGO_URI'))
    #     print(crawler.settings.get('MONGO_DATABASE', 'items'))
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #     )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item = self.download_item(item)
        # print(item)
        result = self.db[self.collection_name].insert_one(dict(item))
        # print(result)

        # send to download queue
        self.redis.publish('channel:download_request', json.dumps({
            'download_url': item['download_url'],
            'file_name': item['file_name']
        }))
        return item

    def download_item(self, item):
        splitted_title = item["title"].split(' ')
        item['file_name'] = splitted_title[0] + "_".join(x for x in splitted_title[1::]) + ".pdf"
        if '/' in item['file_name']:
            splitted_title = item["title"].split('/')
            item['file_name'] = splitted_title[0] + "_".join(x for x in splitted_title[1::])
        if '.pdf' not in item['file_name']:
            item['file_name'] = f'{item["file_name"]}.pdf'
        return item