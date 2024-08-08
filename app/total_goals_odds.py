from odds import Odds


class TotalGoalsOdds:
    def __init__(self, line: float = None, under: Odds = None, over: Odds = None):
        self._line = line
        self._under = under
        self._over = over

    # Getter and Setter for line
    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._line = value

    # Getter and Setter for under_odds
    @property
    def under(self):
        return self._under

    @under.setter
    def under(self, value):
        self._under = value

    # Getter and Setter for over_odds
    @property
    def over(self):
        return self._over

    @over.setter
    def over(self, value):
        self._over = value

    # String representation (__str__ method)
    def __str__(self):
        line_str = f"Line: {self._line}" if self._line is not None else "Line: None"
        under_odds_str = f"Under Odds: {self._under}" if self._under else "Under Odds: None"
        over_odds_str = f"Over Odds: {self._over}" if self._over else "Over Odds: None"
        return f"TotalGoalsOdds({line_str}, {under_odds_str}, {over_odds_str})"

    def total_probability(self):
        return self.under.implied_probability() + self.over.implied_probability()

    def over_fair_probability(self):
        return self.over.implied_probability() / self.total_probability()

    def under_fair_probability(self):
        return self.under.implied_probability() / self.total_probability()
