# Pipeline for ES storage

# NOTICE
# Partially based on: https://github.com/knockrentals/scrapy-elasticsearch
# http://www.apache.org/licenses/LICENSE-2.0

import logging
import copy

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk as send_bulk


class ElasticsearchPipeline:

    def __init__(self, *args, **kwargs):
        self._buffer = []
        self.__client = None

    @property
    def client(self) -> Elasticsearch:
        if not self.__client:
            self.__client = Elasticsearch(hosts=[self._es_url])

        return self.__client

    @classmethod
    def from_crawler(cls, crawler):
        es = cls()
        es.settings = crawler.settings

        es._es_url = es.settings.get('ELASTICSEARCH_URL', 'http://localhost:9200/')
        es._es_index = es.settings.get('ELASTICSEARCH_INDEX', 'zbider-index-dev')

        return es

    def process_item(self, item, spider):
        try:
            item_copy = copy.deepcopy(item)
            item_copy.pop('zbider_raw_data', None)
            self.index_item(item_copy)
        finally:
            return item

    def close_spider(self, spider):
        if len(self._buffer):
            self.send_items()

    def index_item(self, item):
        index_action = {
            '_index': self._es_index,
            '_type': item.get_name(),
            '_source': dict(item)
        }

        self._buffer.append(index_action)

        if len(self._buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 500):
            self.send_items()
            self._buffer = []

    def send_items(self):
        logging.info('Sending bulk documents ({}) to ES'.format(len(self._buffer)))
        send_bulk(self.client, self._buffer)

