from odds import Odds


class TotalGoalsOdds:
    def __init__(self, line: float = None, under_odds: Odds = None, over_odds: Odds = None):
        self._line = line
        self._under_odds = under_odds
        self._over_odds = over_odds

    # Getter and Setter for line
    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    # Getter and Setter for under_odds
    @property
    def under_odds(self):
        return self._under_odds

    @under_odds.setter
    def under_odds(self, value):
        self._under_odds = value

    # Getter and Setter for over_odds
    @property
    def over_odds(self):
        return self._over_odds

    @over_odds.setter
    def over_odds(self, value):
        self._over_odds = value

    # String representation (__str__ method)
    def __str__(self):
        line_str = f"Line: {self._line}" if self._line is not None else "Line: None"
        under_odds_str = f"Under Odds: {self._under_odds}" if self._under_odds else "Under Odds: None"
        over_odds_str = f"Over Odds: {self._over_odds}" if self._over_odds else "Over Odds: None"
        return f"TotalGoalsOdds({line_str}, {under_odds_str}, {over_odds_str})"
