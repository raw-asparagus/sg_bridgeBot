import random

class Card:
    """
    Represents a single playing card with a suit and a rank.

    Attributes:
        rank (str):     The rank of the card (e.g., 'Ace', '2', ... 'King').
        suit (str):     The suit of the card (e.g., 'Clubs', 'Diamonds', 'Hearts', 'Spades').
    """
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        """Returns a string representation of the card."""
        return f"{self.rank} of {self.suit}"

class Deck:
    """
    Represents a deck of 52 playing cards.

    Attributes:
        cards (list of Card):   A list of card objects.
    """
    SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        """Initializes a new deck of 52 cards."""
        self.cards = [ Card(rank, suit) for suit in self.SUITS
                      for rank in self.RANKS ]

    def shuffle(self):
        """Shuffles the deck in place."""
        random.shuffle(self.cards)

    def deal(self, n_hands=4):
        """
        Deals the cards into a specified number of hands.

        Arguments:
            n_hands (int):          The number of hands to deal into.

        Returns:
            list of list of Card:   A list containing 'n_hands' number of card lists.
        """
        return [self.cards[i::n_hands] for i in range(n_hands)]

class Player:
    """
    Represents a player in the game.

    Attributes:
        name (str):                         The name of the player.
        order (int):                        The order of the player in the game (1st, 2nd, etc.).
        hand (list of Card):                The cards currently held by the player.
        sets_won (list of list of Card):    List of card sets won by the player.
        sets_threshold (int):               The number of sets to win to win the game
    """
    def __init__(self, name, order):
        self.name = name
        self.order = order
        self.hand = []
        self.sets_won = []
        self.sets_threshold = None

    def receive_hand(self, cards):
        """Receives a list of cards as the player's hand."""
        self.hand = cards

    def hand_value(self):
        """Calculates the value of the player's hand based on certain card values and suit distribution."""
        value_dict = {
            'Ace': 4,
            'King': 3,
            'Queen': 2,
            'Jack': 1,
        }
        value = sum( value_dict.get(card.rank, 0) for card in self.hand )

        suit_counts = { suit: 0 for suit in Deck.SUITS }
        for card in self.hand:
            suit_counts[card.suit] += 1

        #   Adds a point for any suit with 5 or more cards.
        return value + sum( 1 for count in suit_counts.values() if count >= 5 )

class BaseGame:
    """
    Represents the base class for the Bridge game, managing the deck and players.

    Attributes:
        deck (Deck):                The deck of cards used in the game.
        players (list of Player):   The list of players in the game.
        trump_suit (str):           The suit that has been selected as trump.
        trump_bidder (Player):      The player who won the bidding phase.
        highest_bid (int):          The highest bid made during the game.
    """
    def __init__(self, player_names):
        self.deck = Deck()
        self.players = [ Player(name, i + 1) for i, name in enumerate(player_names) ]

class SetupPhase(BaseGame):
    """
    Manages the setup phase of the game, ensuring each player has a valid hand.

    Inherits from BaseGame.
    """
    def __init__(self, player_names):
        super().__init__(player_names)
        self.setup()

    def setup(self):
        """Sets up the game by shuffling and dealing the cards until each player has a minimum hand value."""
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
