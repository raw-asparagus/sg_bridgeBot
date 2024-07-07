#   models/Card.py

from bson.objectid import ObjectId
from utils import get_collection
from game import Card, Deck

class CardModel:
    """
    Attributes:
        collection (Collection):    The retrieved MongoDB collection.
    """
    def __init__(self, collection_name='cards'):
        self.collection = get_collection(collection_name)
        #   Check if the collection is empty, if so initialize the deck
        if self.collection.count_documents({}) == 0:
            self.initialize_deck()

    def create_card(self, suit, rank):
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
        self.collection.insert_one(card)

    def initialize_deck(self):
        """
        Initializes the deck with 52 cards if the collection is empty.

        This method is called during initialization if the collection is empty.
        """
        for suit in Deck.SUITS:
            for rank in Deck.RANKS:
                self.create_card(suit, rank)

    def get_all_cards(self):
        """
        Retrieves all cards from the collection.

        Returns:
            A list of card documents.
        """
        cards = self.collection.find({})
        return [ Card(card['_id'], card['suit'], card['rank'])
                for card in cards ]

    def get_card(self, suit, rank):
        """
        Retrieves a specific card from the collection based on suit and rank.

        Arguments:
            suit (str):     The suit of the card to retrieve.
            rank (str):     The rank of the card to retrieve.

        Returns:
            The Card object or None if not found.
        """
        card = self.collection.find_one({'suit': suit, 'rank': rank})
        if card:
            return Card(card['suit'], card['rank'], card['_id'])
        return None

    def get_card_by_id(self, card_id):
        """
        Retrieves a specific card from the collection based on its `_id`.

        Arguments:
            card_id (ObjectId):     The `_id` of the card to retrieve.

        Returns:
            The Card object or None if not found.
        """
        card = self.collection.find_one({'_id': ObjectId(card_id)})
        if card:
            return Card(card['suit'], card['rank'], card['_id'])
        return None
