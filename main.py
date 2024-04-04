from game.deck import Deck
from game.player import Player

def main():
    deck = Deck()
    hands = deck.deal(4)
    players = [Player(hand) for hand in hands]

    for index, player in enumerate(players, start=1):
        points = player.calculate_points()
        print(f"Player {index}'s hand: {[str(card) for card in player.hand]} - Points: {points}")

if __name__ == "__main__":
    main()
