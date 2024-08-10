from typing import List
from efl_game_prediction import EFLGamePrediction


class EFLGameweekPrediction:
    def __init__(self, game_predictions: List[EFLGamePrediction] = None):
        self.game_predictions = game_predictions if game_predictions is not None else []

    def sort_teams_by_clean_sheet_chances(self):
        # Create a list of tuples with (team_name, clean_sheet_probability)
        team_probabilities = []
        for prediction in self.game_predictions:
            team_probabilities.append(
                (prediction,
                 prediction.betfair_event.home_team,
                 prediction.scoreline_probability_distribution.home_clean_sheet_probability())
            )
            team_probabilities.append(
                (prediction,
                 prediction.betfair_event.away_team,
                 prediction.scoreline_probability_distribution.away_clean_sheet_probability())
            )

        # Sort the list of tuples by the clean sheet probability in descending order
        team_probabilities.sort(key=lambda x: x[2], reverse=True)

        return team_probabilities

    def sort_home_teams_by_clean_sheet_chances(self):
        # Create a list of tuples with (home_team_name, home_clean_sheet_probability)
        home_team_probabilities = [
            (prediction,
             prediction.betfair_event.home_team,
             prediction.scoreline_probability_distribution.home_clean_sheet_probability())
            for prediction in self.game_predictions
        ]

        # Sort the list of tuples by the clean sheet probability in descending order
        home_team_probabilities.sort(key=lambda x: x[2], reverse=True)

        return home_team_probabilities

    def sort_away_teams_by_clean_sheet_chances(self):
        # Create a list of tuples with (home_team_name, home_clean_sheet_probability)
        away_team_probabilities = [
            (prediction,
             prediction.betfair_event.away_team,
             prediction.scoreline_probability_distribution.away_clean_sheet_probability())
            for prediction in self.game_predictions
        ]

        # Sort the list of tuples by the clean sheet probability in descending order
        away_team_probabilities.sort(key=lambda x: x[2], reverse=True)

        return away_team_probabilities

    def sort_teams_by_scoring_highly_chances(self):
        return []

    def sort_teams_by_points(self):
        # Create a list of tuples with (team_name, points)
        team_points = []
        for prediction in self.game_predictions:
            team_points.append(
                (prediction,
                 prediction.betfair_event.home_team,
                 prediction.expected_home_points)
            )
            team_points.append(
                (prediction,
                 prediction.betfair_event.away_team,
                 prediction.expected_away_points)
            )

        # Sort the list of tuples by the points in descending order
        team_points.sort(key=lambda x: x[2], reverse=True)

        return team_points

    def sort_home_teams_by_points(self):
        return []

    def sort_away_teams_by_points(self):
        return []

    def sort_by_biggest_points_difference(self):
        return []

    def add_game_prediction(self, efl_game_prediction: EFLGamePrediction):
        self.game_predictions.append(efl_game_prediction)
