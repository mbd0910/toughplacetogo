from odds import Odds


class TotalGoalsOdds:
    def __init__(self, line: float, under_odds: Odds, over_odds: Odds):
        self.line = line
        self.under_odds = under_odds
        self.over_odds = over_odds