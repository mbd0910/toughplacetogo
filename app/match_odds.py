from odds import Odds


class MatchOdds:
    def __init__(self, home: Odds, draw: Odds, away: Odds):
        self.home = home
        self.draw = draw
        self.away = away
