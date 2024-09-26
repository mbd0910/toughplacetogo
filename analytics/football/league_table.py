from football.models import Team

class LeagueTable:
    def __init__(self, rows=None):
        if rows is None:
            rows = {}
        self.rows = rows

    def get_team_row(self, team: Team):
        team_name = team.name
        if team_name not in self.rows:
            self.rows[team_name] = LeagueTableRow(team)

        return self.rows[team_name]

    def __str__(self):
        return "\n".join(row.__str__() for row in self.rows.values())


class GamePOV:
    def __init__(self, team: Team, opposition: Team, scored: int, conceded: int, is_home: bool):
        self.team = team
        self.opposition = opposition
        self.scored = scored
        self.conceded = conceded
        self.is_home = is_home


class LeagueTableRow:
    def __init__(self, team: Team):
        self.team = team
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.scored = 0
        self.conceded = 0
        self.game_povs = []


    def games_played(self):
        return self.wins + self.draws + self.losses

    def points(self):
        return 3 * self.wins + self.draws

    def goal_difference(self):
        return self.scored - self.conceded

    def add_game_pov(self, game_pov: GamePOV):
        self.game_povs.append(game_pov)
        goals_scored = game_pov.scored
        goals_conceded = game_pov.conceded
        self.scored += goals_scored
        self.conceded += goals_conceded

        if goals_scored > goals_conceded:
            self.wins += 1
        elif goals_scored == goals_conceded:
            self.draws += 1
        else:
            self.losses += 1

    def __str__(self):
        return f"{self.team.name} {self.games_played()} {self.wins} {self.draws} {self.losses} {self.scored} {self.conceded} {self.points()}"
