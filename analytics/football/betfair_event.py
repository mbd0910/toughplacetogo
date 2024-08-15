from datetime import datetime

class BetfairEvent:
    def __init__(self,
                 event_id: int,
                 event_name: str,
                 kickoff: datetime,
                 home_team: str,
                 away_team: str):
        self.event_id = event_id
        self.event_name = event_name
        self.kickoff = kickoff
        self.home_team = home_team
        self.away_team = away_team