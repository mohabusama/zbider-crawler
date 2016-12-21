# -*- coding: utf-8 -*-

# GHE User
from urllib.parse import urljoin

import scrapy

from crawler.common.item import ZbiderItem


########
# USER #
########

def repos_url(accounts, item=None):
    url = item.get('url', '')

    if url:
        url = url if url.endswith('/') else url + '/'
        return urljoin(url, 'repositories')

    return ''

class GHEUser(ZbiderItem):

    default_tags_str = 'github ghe user'
    tags_fields = ('name', 'login',)

    raw_data = True

    name = scrapy.Field()
    login = scrapy.Field()
    url = scrapy.Field(source='html_url')
    repos_url = scrapy.Field(serializer=repos_url)
    followers = scrapy.Field()
    following = scrapy.Field()
    public_repos = scrapy.Field()
    avatar_url = scrapy.Field()

    @staticmethod
    def get_name():
        return 'zbider-ghe-user'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': self['name'],
            'text': 'Github User: {}'.format(self['name']),
            'link': self['url'],
            'image': self['avatar_url'],
        }

########
# REPO #
########

def repo_owner(value, item=None):
    return item.get('owner', {}).get('login', '')

class GHERepo(ZbiderItem):

    tags_fields = ('name', 'full_name', 'description',)
    default_tags_str = 'github ghe user'

    raw_data = True

    name = scrapy.Field()
    full_name = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field(source='html_url')
    fork = scrapy.Field()
    forks_count = scrapy.Field()
    watchers_count = scrapy.Field()
    stargazers_count = scrapy.Field()
    owner = scrapy.Field(serializer=repo_owner)

    @staticmethod
    def get_name():
        return 'zbider-ghe-repo'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': self['name'],
            'text': 'Github Repo: {}'.format(self['name']),
            'link': self['url'],
        }
