from odds import Odds


class MatchOdds:
    def __init__(self, home: Odds = None, draw: Odds = None, away: Odds = None):
        self.home = home
        self.draw = draw
        self.away = away

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

    def __str__(self):
        home_str = str(self.home) if self.home else "None"
        draw_str = str(self.draw) if self.draw else "None"
        away_str = str(self.away) if self.away else "None"
        return f"MatchOdds(Home: {home_str}, Draw: {draw_str}, Away: {away_str})"
