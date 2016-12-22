# Teams and Users Spider
import json

from urllib.parse import urljoin

import scrapy

from crawler.items import Team, User


class TeamAPI(scrapy.Spider):
    """Teams and users API spider"""

    name = 'team'

    oauth2 = True

    def start_requests(self):
        self.teams_url = self.settings['TEAM_URL']
        self.users_url = self.settings['USER_URL']
        return [scrapy.Request(self.teams_url, callback=self.parse)]

    def parse(self, response):
        teams = json.loads(response.body_as_unicode())
        for team in teams:
            yield scrapy.Request(urljoin(self.teams_url, team['team_id']), callback=self.parse_team)

    def parse_team(self, response):
        team_data = json.loads(response.body_as_unicode())
        team = Team.load(team_data)
        for member in team['members']:
            yield scrapy.Request(urljoin(self.users_url, member), callback=self.parse_user)
        yield team

    def parse_user(self, response):
        user = json.loads(response.body_as_unicode())
        yield User.load(user)

    def parse_teams_response(self, response):
        teams = json.loads(response.body_as_unicode())
        if type(teams) is list:
            for team in teams:
                yield Team.load(team)
        else:
            return Team.load(teams)
