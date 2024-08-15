from odds import Odds
from moneyed import Money

class MatchOdds:
    def __init__(self, home: Odds = None, draw: Odds = None, away: Odds = None, total_matched: Money = None):
        self.home = home
        self.draw = draw
        self.away = away
        self.total_matched = total_matched

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self, value):
        self._home = value

    @property
    def draw(self):
        return self._draw

    @draw.setter
    def draw(self, value):
        self._draw = value

    @property
    def away(self):
        return self._away

    @away.setter
    def away(self, value):
        self._away = value

    @property
    def total_matched(self):
        return self._total_matched

    @total_matched.setter
    def total_matched(self, value):
        self._total_matched = value

    def __str__(self):
        home_str = str(self.home) if self.home else "None"
        draw_str = str(self.draw) if self.draw else "None"
        away_str = str(self.away) if self.away else "None"
        return f"MatchOdds(Home: {home_str}, Draw: {draw_str}, Away: {away_str})"

    def total_probability(self):
        return self.home.implied_probability() + self.draw.implied_probability() + self.away.implied_probability()

    def home_fair_probability(self):
        return self.home.implied_probability() / self.total_probability()

    def draw_fair_probability(self):
        return self.draw.implied_probability() / self.total_probability()

    def away_fair_probability(self):
        return self.away.implied_probability() / self.total_probability()

    def overround(self):
        return self.total_probability() - 1.0


