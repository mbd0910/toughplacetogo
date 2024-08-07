from odds import Odds


class AsianHandicapOdds:
    def __init__(self,
                 home_line: float = None, home_odds: Odds = None, away_line: float = None, away_odds: Odds = None):
        self._home_line = home_line
        self._home_odds = home_odds
        self._away_line = away_line
        self._away_odds = away_odds

    # Getter and Setter for home_line
    @property
    def home_line(self):
        return self._home_line

    @home_line.setter
    def home_line(self, value):
        self._home_line = value

    # Getter and Setter for home_odds
    @property
    def home_odds(self):
        return self._home_odds

    @home_odds.setter
    def home_odds(self, value):
        self._home_odds = value

    # Getter and Setter for away_line
    @property
    def away_line(self):
        return self._away_line

    @away_line.setter
    def away_line(self, value):
        self._away_line = value

    # Getter and Setter for away_odds
    @property
    def away_odds(self):
        return self._away_odds

    @away_odds.setter
    def away_odds(self, value):
        self._away_odds = value

    # String representation (__str__ method)
    def __str__(self):
        home_line_str = f"Home Line: {self._home_line}" if self._home_line is not None else "Home Line: None"
        home_odds_str = f"Home Odds: {self._home_odds}" if self._home_odds else "Home Odds: None"
        away_line_str = f"Away Line: {self._away_line}" if self._away_line is not None else "Away Line: None"
        away_odds_str = f"Away Odds: {self._away_odds}" if self._away_odds else "Away Odds: None"
        return f"AsianHandicapOdds({home_line_str}, {home_odds_str}, {away_line_str}, {away_odds_str})"
