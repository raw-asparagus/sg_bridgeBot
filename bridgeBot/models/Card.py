#   models/Card.py
from bson.objectid import ObjectId
from utils import get_collection
from game import Card, Deck

class CardModelMeta(type):
    """
    Metaclass to handle database initialization and collection setup.

    Attribute:
        collection (Collection):    The retrieved MongoDB collection.
    """
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.collection = get_collection('cards')
        if cls.collection.count_documents({}) == 0:
            cls.initialize_deck()

class CardModel(metaclass=CardModelMeta):
    def __init__(self):
        pass

    @classmethod
    def create_card(cls, suit, rank):
        """
        Creates a card document in the collection.

        Arguments:
            suit (str):     The suit of the card.
            rank (str):     The rank of the card.
        """
        card = {
            'suit': suit,
            'rank': rank
        }
        cls.collection.insert_one(card)

    @classmethod
    def initialize_deck(cls):
        """
        Initializes the deck with 52 cards if the collection is empty.

        This method is called during initialization if the collection is empty.
        """
        for suit in Deck.SUITS:
            for rank in Deck.RANKS:
                cls.create_card(suit, rank)

    @classmethod
    def get_all_cards(cls):
        """
        Retrieves all cards from the collection.

        Returns:
            A list of card documents.
        """
        cards = cls.collection.find({})
        return [ Card(card['_id'], card['suit'], card['rank'])
                for card in cards ]

    @classmethod
    def get_card(cls, suit, rank):
        """
        Retrieves a specific card from the collection based on suit and rank.

        Arguments:
            suit (str):     The suit of the card to retrieve.
            rank (str):     The rank of the card to retrieve.

        Returns:
            The Card object or None if not found.
        """
        card = cls.collection.find_one({'suit': suit, 'rank': rank})
        if card:
            return Card(card['suit'], card['rank'], card['_id'])
        return None

    @classmethod
    def get_card_by_id(cls, card_id):
        """
        Retrieves a specific card from the collection based on its `_id`.

        Arguments:
            card_id (ObjectId):     The `_id` of the card to retrieve.

        Returns:
            The Card object or None if not found.
        """
        card = cls.collection.find_one({'_id': ObjectId(card_id)})
        if card:
            return Card(card['suit'], card['rank'], card['_id'])
        return None
