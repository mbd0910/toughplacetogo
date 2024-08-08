from typing import List
from efl_game_prediction import EFLGamePrediction


class EFLGameweekPrediction:
    def __init__(self, game_predictions: List[EFLGamePrediction] = None):
        self.game_predictions = game_predictions if game_predictions is not None else []


    def sort_teams_by_clean_sheet_chances(self):
        return []


    def sort_teams_by_scoring_highly_chances(self):
        return []