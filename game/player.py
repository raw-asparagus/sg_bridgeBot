from .deck import Deck

class Player:
    points_values = {'A': 4, 'K': 3, 'Q': 2, 'J': 1}

    def __init__(self, hand):
        self.hand = hand

    def calculate_points(self):
        points = 0
        suits_count = { suit: 0 for suit in Deck.suits }

        for card in self.hand:
            points += self.points_values.get(card.rank, 0)
            suits_count[card.suit] += 1
        
        points += sum(1 for count in suits_count.values() if count >= 5)
        
        return points
