# -*- coding: utf-8 -*-

# Team model

import scrapy

from crawler.common.item import ZbiderItem


def infrastructure_account(accounts, item=None):
    serialized = []
    for account in accounts:
        serialized.append({'name': account['name'], 'provider': account['provider'], 'id': account['id']})

    return serialized


class Team(ZbiderItem):

    tags_fields = []
    default_tags_str = 'team'

    id = scrapy.Field()
    team_id = scrapy.Field()
    team_type = scrapy.Field(source='type')

    name = scrapy.Field()
    description = scrapy.Field()
    mail = scrapy.Field()
    alias = scrapy.Field(source='id_name')

    members = scrapy.Field(source='member')
    delivery_lead = scrapy.Field()
    cost_center = scrapy.Field()

    infrastructure_accounts = scrapy.Field(serializer=infrastructure_account, source='infrastructure-accounts')

    @staticmethod
    def get_name():
        return 'zbider-team'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': '{} - ({})'.format(self['name'], self['alias']),
            'text': self['description'] or self['name'],
            'link': 'https://zlive.lightning.force.com/one/one.app#/sObject/a0I58000000xXjEEAU/view',
        }
