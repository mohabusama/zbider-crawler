# -*- coding: utf-8 -*-

# ZMON model
import scrapy
from scrapy.utils.project import get_project_settings

from crawler.common.item import ZbiderItem

from zmon_cli.client import Zmon


def zmon_url(value, item=None):
    return item['zbider_fields'].get('link', '')


class ZmonCheck(ZbiderItem):

    tags_fields = ('team', 'name',)
    default_tags_str = 'zmon check'

    raw_data = True

    id = scrapy.Field()
    url = scrapy.Field(serializer=zmon_url)
    name = scrapy.Field()
    team = scrapy.Field(source='owning_team')
    owning_team = scrapy.Field()
    last_modified_by = scrapy.Field()
    command = scrapy.Field()
    description = scrapy.Field()

    def __init__(self, *args, **kwargs):
        zmon_url = get_project_settings().get('ZMON_URL', 'https://demo.zmon.io')
        self._zmon = Zmon(zmon_url, token='123')

        super().__init__(*args, **kwargs)

    @staticmethod
    def get_name():
        return 'zbider-zmon-check'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': self['name'],
            'text': self['description'],
            'link': self._zmon.check_definition_url(self['zbider_raw_data']),
        }


class ZmonAlert(ZbiderItem):

    tags_fields = ('team', 'name', 'responsible_team',)
    default_tags_str = 'zmon alert'

    raw_data = True

    id = scrapy.Field()
    url = scrapy.Field(serializer=zmon_url)
    name = scrapy.Field()
    team = scrapy.Field(source='owning_team')
    responsible_team = scrapy.Field()
    last_modified_by = scrapy.Field()
    condition = scrapy.Field()
    description = scrapy.Field()
    priority = scrapy.Field()

    def __init__(self, *args, **kwargs):
        zmon_url = get_project_settings().get('ZMON_URL', 'https://demo.zmon.io')
        self._zmon = Zmon(zmon_url, token='123')

        super().__init__(*args, **kwargs)

    @staticmethod
    def get_name():
        return 'zbider-zmon-alert'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': self['name'],
            'text': self['description'],
            'link': self._zmon.alert_details_url(self['zbider_raw_data']),
        }

class ZmonDashboard(ZbiderItem):

    tags_fields = ('title',)
    default_tags_str = 'zmon dashboard'

    raw_data = True

    title = scrapy.Field()
    url = scrapy.Field(serializer=zmon_url)

    def __init__(self, *args, **kwargs):
        zmon_url = get_project_settings().get('ZMON_URL', 'https://demo.zmon.io')
        self._zmon = Zmon(zmon_url, token='123')

        super().__init__(*args, **kwargs)

    @staticmethod
    def get_name():
        return 'zbider-zmon-dashboard'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': self['title'],
            'text': self['title'],
            'link': self._zmon.dashboard_url(self['zbider_raw_data']['id']),
        }

class ZmonGrafana(ZbiderItem):

    tags_fields = ('title',)
    default_tags_str = 'zmon grafana'

    raw_data = True

    title = scrapy.Field()
    url = scrapy.Field(serializer=zmon_url)

    def __init__(self, *args, **kwargs):
        zmon_url = get_project_settings().get('ZMON_URL', 'https://demo.zmon.io')
        self._zmon = Zmon(zmon_url, token='123')

        super().__init__(*args, **kwargs)

    @staticmethod
    def get_name():
        return 'zbider-zmon-grafana'

    def set_zbider_fields(self):
        self['zbider_fields'] = {
            'title': self['title'],
            'text': self['title'],
            'link': self._zmon.grafana_dashboard_url(self['zbider_raw_data']),
        }

