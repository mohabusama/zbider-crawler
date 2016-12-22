# -*- coding: utf-8 -*-

# User model

import scrapy

from crawler.common.item import ZbiderItem


def user_teams(teams, item=None):
    serialized = []
    for team in teams:
        if 'nickname' in team:
            serialized.append(team['nickname'])

    return serialized

def github_accounts(accounts, item=None):
    res = []
    if 'github' in accounts:
        for g in accounts['github']:
            res.append({'username': g['username'], 'link': 'https://github.com/{}'.format(g['username'])})

    return res

class User(ZbiderItem):

    tags_fields = ['job_title', 'email', 'login']
    default_tags_str = 'user employee'

    name = scrapy.Field()
    full_name = scrapy.Field()
    email = scrapy.Field()
    login = scrapy.Field()

    team = scrapy.Field()
    teams = scrapy.Field(serializer=user_teams)
    delivery_lead = scrapy.Field()
    cost_center = scrapy.Field()
    department = scrapy.Field()
    company = scrapy.Field()

    job_title = scrapy.Field()
    github = scrapy.Field(source='accounts', serializer=github_accounts)

    @staticmethod
    def get_name():
        return 'zbider-user'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': self['full_name'],
            'text': 'User: {}'.format(self['full_name']),
            'link': 'https://zlive.lightning.force.com/one/one.app#/sObject/00524000002WeZVAA0/view',
            'image': 'https://zlive--c.eu6.content.force.com/profilephoto/72924000000ZQE4/T',
        }
