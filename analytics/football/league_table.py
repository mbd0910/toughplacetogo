

class LeagueTable:
    def __init__(self, rows=None):
        if rows is None:
            rows = {}
        self.rows = rows

    def get_team_row(self, team_name):
        if team_name not in self.rows:
            self.rows[team_name] = LeagueTableRow(team_name)

        return self.rows[team_name]

    def __str__(self):
        return "\n".join(row.__str__() for row in self.rows.values())



class LeagueTableRow:
    def __init__(self, team_name, wins = 0, draws = 0, losses = 0, scored = 0, conceded = 0):
        self.team_name = team_name
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.scored = scored
        self.conceded = conceded

    def games_played(self):
        return self.wins + self.draws + self.losses

    def points(self):
        return 3 * self.wins + self.draws

    def goal_difference(self):
        return self.scored - self.conceded

    def add_result(self, goals_scored, goals_conceded):
        self.scored += goals_scored
        self.conceded += goals_conceded

        if goals_scored > goals_conceded:
            self.wins += 1
        elif goals_scored == goals_conceded:
            self.draws += 1
        else:
            self.losses += 1

    def __str__(self):
        return f"{self.team_name} {self.games_played()} {self.wins} {self.draws} {self.losses} {self.scored} {self.conceded} {self.points()}"