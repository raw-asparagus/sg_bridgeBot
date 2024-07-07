#   game/core.py

import random

class Card:
    """
    Represents a single playing card with its MongoDB `_id`, a suit and a rank.

    Attributes:
        id (str):       The MongoDB `_id` field of the document containing the
                        card.
        suit (str):     The suit of the card.
        rank (str):     The rank of the card.
    """
    def __init__(self, card_id, suit, rank):
        self.id = card_id
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        """Returns a string representation of the card."""
        return f"{self.rank} of {self.suit}"



class Deck:
    """
    Represents a deck of 52 playing cards.

    Constants:
        SUITS (list of str):    List of suits.
        RANKS (list of str):    List of ranks.

    Attributes:
        cards (list of Card):   A list of card objects.
    """
    SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen',
             'King', 'Ace']

    def __init__(self, cards):
        """Initializes a new deck of 52 cards."""
        self.cards = cards

    def shuffle(self):
        """Shuffles the deck in place."""
        random.shuffle(self.cards)

    def deal(self, n_hands=4):
        """
        Deals the cards into a specified number of hands.

        Arguments:
            n_hands (int):          The number of hands to deal into.

        Returns:
            list of list of Card:   A list containing 'n_hands' number of list
            of cards.
        """
        return [ self.cards[i::n_hands] for i in range(n_hands) ]

    @classmethod
    def sort_deck(cls, cards):
        """
        Sorts deck.

        Arguments:
            cards (list of Card):   A list of card objects.

        Returns:
            The sorted deck of cards.
        """
        sort_fn = lambda card: (cls.SUITS.index(card.suit),
                                cls.RANKS.index(card.rank))
        cards.sort(key=sort_fn)
        return cards



class Player:
    """
    Represents a player in the game instance.

    Attributes:
        name (str):                         The name of the player.
        order (int):                        The order of the player in the game
                                            (1st -> 1, 2nd -> 2, etc.).
        hand (list of Card):                The cards currently held by the
                                            player.
        sets_won (list of list of Card):    List of card sets won by the player.
        sets_threshold (int):               The number of sets to possess to win
                                            the game.
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
        """
        Calculates the value of the player's hand.
        
        Returns:
            The value of the player's hand
        """
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
