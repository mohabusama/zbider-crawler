# Pipeline for ZZ service
import logging

from urllib.parse import urljoin

import requests


class IgnoreException(Exception):
    pass


class ZZPipeline:

    def __init__(self, *args, **kwargs):
        self._buffer = []
        self.__session = requests.Session()

        self.__session.headers = {'User-Agent': 'zbider'}

    @property
    def session(self):
        return self.__session

    @classmethod
    def from_crawler(cls, crawler):
        zz = cls()
        zz.settings = crawler.settings

        zz._zz_url = zz.settings.get('ZZ_API_URL', 'http://localhost:7272/top/api/v1/')

        return zz

    def register_url(self):
        return urljoin(self._zz_url, 'url')

    def reap_url(self):
        return urljoin(self._zz_url, 'reap')

    def close_spider(self, spider):
        if len(self._buffer):
            self.send_items()

    def process_item(self, item, spider):
        try:
            data = self._extract_data(item)
            self._buffer.append(data)
            if len(self._buffer) > 100:
                self.send_items()
        finally:
            return item

    def send_items(self):
        logging.info('Sending bulk items ({}) to ZZ'.format(len(self._buffer)))
        if self._buffer:
            self.session.post(self.register_url(), json=self._buffer, timeout=30)
            self._buffer = []

    def _extract_data(self, item):
        if not item.get('url', None):
            raise IgnoreException

        return {
            'url': item['url'],
            'tags': item.get_tags(),
            'description': item.get('description', ''),
        }

