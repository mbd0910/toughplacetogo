

class ScorelineProbabilityDistribution:
    def __init__(self, probability_dictionary):
        self.probability_dictionary = probability_dictionary

    def home_clean_sheet_probability(self):
        return sum(self.probability_dictionary[home_goals][0] for home_goals in self.probability_dictionary)

    def away_clean_sheet_probability(self):
        return sum(self.probability_dictionary[0][away_goals] for away_goals in self.probability_dictionary[0])

    def home_win_probability(self):
        return sum(
            self.probability_dictionary[home_goals][away_goals]
            for home_goals in self.probability_dictionary
            for away_goals in self.probability_dictionary[home_goals]
            if home_goals > away_goals
        )

    def away_win_probability(self):
        return sum(
            self.probability_dictionary[home_goals][away_goals]
            for home_goals in self.probability_dictionary
            for away_goals in self.probability_dictionary[home_goals]
            if away_goals > home_goals
        )

    def draw_probability(self):
        return sum(
            self.probability_dictionary[home_goals][away_goals]
            for home_goals in self.probability_dictionary
            for away_goals in self.probability_dictionary[home_goals]
            if home_goals == away_goals
        )

    def home_two_or_more_goals_probability(self):
        return sum(
            self.probability_dictionary[home_goals][away_goals]
            for home_goals in self.probability_dictionary
            for away_goals in self.probability_dictionary[home_goals]
            if home_goals >= 2
        )

    def away_two_or_more_goals_probability(self):
        return sum(
            self.probability_dictionary[home_goals][away_goals]
            for home_goals in self.probability_dictionary
            for away_goals in self.probability_dictionary[home_goals]
            if away_goals >= 2
        )