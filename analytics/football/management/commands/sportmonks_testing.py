import json

import requests
from decouple import config
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Testing out the Sportmonks API'

    football_url_prefix = 'https://api.sportmonks.com/v3/football/'
    core_url_prefix = 'https://api.sportmonks.com/v3/core/'

    headers = {
        'Authorization': config('SPORTMONKS_API_TOKEN')
    }

    def handle(self, *args, **kwargs):
        # self.fixtures()
        # self.continents()
        self.leagues()
        # self.stages()
        # self.rounds()

    def fixtures(self):
        fixtures_endpoint = self.football_url_prefix + 'fixtures'
        self.get_endpoint(fixtures_endpoint)

    def continents(self):
        continents_endpoint = self.core_url_prefix + 'continents'
        self.get_endpoint(continents_endpoint)

    def leagues(self):
        leagues_endpoint = self.football_url_prefix + 'leagues'
        self.get_endpoint(leagues_endpoint)

    def stages(self):
        stages_endpoint = self.football_url_prefix + 'stages'
        self.get_endpoint(stages_endpoint)

    def rounds(self):
        rounds_endpoint = self.football_url_prefix + 'odds/pre-match'
        self.get_endpoint(rounds_endpoint)

    def get_endpoint(self, url):
        response = requests.get(url , headers=self.headers)

        print(json.dumps(json.loads(response.text), indent=3))