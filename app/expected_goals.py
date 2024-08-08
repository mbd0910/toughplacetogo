
class ExpectedGoals:
    def __init__(self, home: float, away: float):
        self.home = home
        self.away = away

    def total_goals(self):
        return self.home + self.away

    def home_handicap(self):
        return self.home - self.away

    def away_handicap(self):
        return -self.home_handicap()