# ZMON Spider
# zmon.io

import json

import scrapy

from zmon_cli.client import Zmon, ACTIVE_CHECK_DEF, ACTIVE_ALERT_DEF, SEARCH

from crawler.items import ZmonCheck, ZmonAlert, ZmonDashboard, ZmonGrafana


class ZmonSpider(scrapy.Spider):
    """ZMON spider"""

    name = 'zmon'

    oauth2 = True

    def start_requests(self):
        zmon_url = self.settings['ZMON_URL']

        # Dummy ZMON. Only used for URLs
        self._zmon = Zmon(zmon_url, token='123')

        search_url = self._zmon.endpoint(SEARCH) + '?q=""&limit=2000'

        yield scrapy.Request(self._zmon.endpoint(ACTIVE_CHECK_DEF), callback=self.parse_checks)
        yield scrapy.Request(self._zmon.endpoint(ACTIVE_ALERT_DEF), callback=self.parse_alerts)
        yield scrapy.Request(search_url, callback=self.parse_search)

    def parse_checks(self, response):
        checks = json.loads(response.body_as_unicode()).get('check_definitions')
        for check in checks[:1]:
            yield ZmonCheck.load(check)

    def parse_alerts(self, response):
        alerts = json.loads(response.body_as_unicode()).get('alert_definitions')
        for alert in alerts[:1]:
            yield ZmonAlert.load(alert)

    def parse_search(self, response):
        search = json.loads(response.body_as_unicode())

        dashboards = search['dashboards']
        grafana_dashboards = search['grafana_dashboards']

        for dashboard in dashboards[:1]:
            yield ZmonDashboard.load(dashboard)

        for grafana in grafana_dashboards[:1]:
            yield ZmonGrafana.load(dashboard)

