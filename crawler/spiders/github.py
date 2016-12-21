# Spider for GHE API
import logging

import json
from urllib.parse import urljoin

import scrapy

from crawler.items import GHEUser, GHERepo


class GHE(scrapy.Spider):
    """GHE API spider"""

    name = 'ghe'

    token = ''

    def user_url(self, u):
        return urljoin(self.ghe_url, 'users/{}'.format(u))

    def start_requests(self):
        self.ghe_url = self.settings['GHE_URL']
        self.token = self.settings['GHE_TOKEN']
        self.ghe_url = self.ghe_url if self.ghe_url.endswith('/') else self.ghe_url + '/'

        self.users = self.settings['GHE_USERS']
        for u in self.users:
            yield scrapy.Request(self.user_url(u), callback=self.parse)

    def parse(self, response):
        user = json.loads(response.body_as_unicode())

        yield scrapy.Request(user['repos_url'], callback=self.parse_user_repos)

        yield GHEUser.load(user)

    def parse_user_repos(self, response):
        repos = json.loads(response.body_as_unicode())

        for repo in repos:
            yield GHERepo.load(repo)
