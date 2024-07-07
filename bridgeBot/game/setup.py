#   game/setup.py
from models import CardModel
from .core import Deck, Player

class BaseGame:
    """
    Represents the base class for a Bridge game instance, managing the deck and
    players.

    Attributes:
        deck (Deck):                The deck of cards used in the game.
        players (list of Player):   The list of players in the game.
    """
    def __init__(self, player_names):
        card_model = CardModel()
        cards = card_model.get_all_cards()
        self.deck = Deck(cards)
        self.players = [ Player(name, i + 1)
                        for i, name in enumerate(player_names) ]



class SetupPhase(BaseGame):
    """
    Manages the setup phase of the game, ensuring each player has a valid hand.
    """
    def __init__(self, player_names):
        super().__init__(player_names)
        self.setup()

    def setup(self):
        """
        Sets up the game by shuffling and dealing the cards until each player
        has a minimum hand value.
        """
        self.shuffle_and_deal()
        for player in self.players:
            while player.hand_value() < 5:
                self.shuffle_and_deal()

    def shuffle_and_deal(self):
        """Shuffles the deck and deals the cards to all players."""
        self.deck.shuffle()
        hands = self.deck.deal()
        for player, hand in zip(self.players, hands):
            player.receive_hand(hand)
