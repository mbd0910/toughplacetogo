

class Odds:
    def __init__(self, price):
        self.price = price

    def implied_probability(self):
        return 1 / self.price

    def __str__(self):
        return f"Odds: {self.price}"
