from odds import Odds


class AsianHandicapOdds:
    def __init__(self, home_line: float, home_odds: Odds, away_line: float, away_odds: Odds):
        self.home_line = home_line
        self.home_odds = home_odds
        self.away_line = away_line
        self.away_odds = away_odds