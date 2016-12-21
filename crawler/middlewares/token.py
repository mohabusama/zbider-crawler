# -*- coding: utf-8 -*-

# Add OAUTH2 headers
import zign.api
import tokens


class ZbiderTokenMiddleware(object):

    def __init__(self, method='user'):
        self._method = 'user'

        if method in ('service', 'services'):
            tokens.configure()
            tokens.manage('uid')

    @classmethod
    def from_crawler(cls, crawler):
        oauth2_method = crawler.settings.get('OAUTH2_CLIENT', 'user')
        return cls(oauth2_method)

    def process_request(self, request, spider):
        if hasattr(spider, 'oauth2') and spider.oauth2:
            request.headers['Authorization'] = 'Bearer {}'.format(self._get_token())

        if hasattr(spider, 'token') and spider.token:
            request.headers['Authorization'] = 'token {}'.format(spider.token)


    def _get_token(self):
        if self._method == 'user':
            return zign.api.get_token('zbider', ['uid'])

        return tokens.get('uid')
