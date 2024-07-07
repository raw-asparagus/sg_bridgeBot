from .core import Deck
from .setup import BaseGame

class BiddingPhase(BaseGame):
    """
    Manages the bidding phase of the game; collecting bids from players, and
    determining the winning bid and the trump suit for the gameplay phase.

    Attributes:
        active (dict):          A dictionary mapping (Player: Bool) indicating
                                if they are active bidders.
        pass_count (int):       The number of players who passed
        numeric_bid (int):      The highest numeric bid value made.
        trump_suit (str):       The trump suit.
        highest_bid (int):      The highest computed bid value (bid + suit). 
        trump_bidder (Player):  The layer who made the winning bid.
        partnership (dict):     A dictionary mapping (Player: Player) each
                                player to their partner.
    """
    def __init__(self, setupPhase):
        self.deck = setupPhase.deck
        self.players = setupPhase.players
        self.active = { player: True for player in self.players }
        self.pass_count = 0
        self.numeric_bid = 0
        self.trump_suit = None
        self.highest_bid = 0
        self.trump_bidder = None
        self.partnership = {}

    def start_bidding(self):
        """Executes the bidding process until three players have passed."""
        while self.pass_count < 3:
            for player in self.players:
                if self.active[player]:
                    if self.trump_bidder and self.pass_count == 3:
                        print(f'Bidding ended early.\nWinner: \
{self.trump_bidder.name}  with {self.trump_suit} at {self.numeric_bid} bids.')
                        return None
                    self.collect_bid(player)

    def collect_bid(self, player):
        """
        Collects a bid from the specified player. A player can either make a bid
        higher in value than the current highest or pass. If the player passes,
        their active status is set to False.
        """
        available_bids = self.calculate_available_bids()
        bid = input(f'\n{player.name} (Player {player.order}) bidding.\n\
Available bids: {available_bids}\nEnter your bid: ')
        bid = bid.title()   #   Capitalizes first letter and after every
                            #   whitespace
        if bid == 'Pass':
            self.active[player] = False
            self.pass_count += 1
        else:
            bid_number, bid_suit = bid.split(maxsplit=1)
            bid_number = int(bid_number)
            self.numeric_bid = bid_number
            self.trump_suit = bid_suit
            self.highest_bid = self.calculate_bid_value(bid_number, bid_suit)
            self.trump_bidder = player

    def calculate_available_bids(self):
        """
        Calculates and returns the list of available bids based on the current
        highest bid.

        Full truncated list: ['Pass', '1 Clubs', '1 Diamonds', '1 Hearts',
                              '1 Spades', '1 No Trump', '2 Clubs', ...,
                              '7 Spades', '7 No Trump'].
        If a bid for e.g. '1 Hearts' was made, any bids lower than or equal in
        value to '1 Hearts' will no longer be available for subsequent bids.
        """
        bids = ['Pass'] if self.pass_count < 3 else []
        #   Sets minimum bid amount of 1
        current_level = max(self.numeric_bid // 10, 1)
        for i in range(current_level, 8):
            for suit in Deck.SUITS + ["No Trump"]:
                bid_value = self.calculate_bid_value(i, suit)
                if bid_value > self.highest_bid:
                    bids.append(f"{i} {suit}")
        return bids

    def calculate_bid_value(self, bid_number, bid_suit):
        """
        Calculates a unique numeric value for a bid.

        For simplicity, adopt the score weightages:
        Bid set count:
        1 - 10 pts         Clubs - 1 pts
        2 - 20 pts      Diamonds - 2 pts
        3 - 30 pts        Hearts - 3 pts
        4 - 40 pts        Spades - 4 pts
        5 - 50 pts      No Trump - 5 pts
        6 - 60 pts
        7 - 70 pts
        """
        score = {
            'Clubs': 1,
            'Diamonds': 2,
            'Hearts': 3,
            'Spades': 4,
            'No Trump': 5,
        }
        return bid_number * 10 + score[bid_suit]

    def select_partner(self, bidding_player):
        """
        Allows the bidding winner to select a partner based on a specific card
        from other players' hands.
        """
        print(f'\n{bidding_player.name} won the bid with {self.trump_suit}.\n\
Select a partner card:')

        available_cards = Deck.sort_deck([ card for player in self.players
                                          if player != bidding_player
                                          for card in player.hand ])

        # Display the sorted cards with enumeration
        i = 0
        for idx, card in enumerate(available_cards, 1):
            print(f"{idx}: {card}".ljust(25), end='')
            if i == 2:
                print('')
                i = 0
            else:
                print(', ', end='')
                i += 1

        # Input selection of the card index
        partner_card_index = int(input("\nEnter the number of the card to " \
                                       "select as your partner's card: ")) - 1
        partner_card = available_cards[partner_card_index]

        # Display the chosen partner card
        print(f"You have selected {partner_card}. The owner of {partner_card} \
will be your partner!\n")

        # Find the owner of the partner card and establish partnership
        partner_player = None
        for player in self.players:
            if partner_card in player.hand:
                partner_player = player
                break

        team_1 = [bidding_player, partner_player]

        for player in team_1:
            player.sets_threshold = self.numeric_bid + 6

        # Set the partnership for the other two players
        team_2 = [ player for player in self.players if player not in team_1 ]

        for player in team_2:
            player.sets_threshold = 8 - self.numeric_bid

        self.partnership.update({
            bidding_player: partner_player,
            partner_player: bidding_player,
            team_2[0]: team_2[1],
            team_2[1]: team_2[0],
        })
