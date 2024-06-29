from .core import Card, Deck, Player, BaseGame, SetupPhase

class BiddingPhase(BaseGame):
    """
    Manages the bidding phase of a Bridge game, including collecting bids from players,
    and determining the winning bid and the trump suit for the gameplay phase.

    Attributes:
        active_bidders (dict):      A dictionary mapping each player to a boolean indicating if they are still active in bidding.
        pass_count (int):           Counter for the number of players who have passed in the bidding round.
        highest_numeric_bid (int):  The highest numeric value of bid made, used to compare subsequent bids.
        trump_suit (str):           Trump suit.
        highest_bid (int):          Highest bid value (bid + suit). 
        trump_bidder (Player):      Player who made the winning bid.
        partnership (dict):         Key (Player): Value - partner (Player)
    """
    def __init__(self, setupPhaseObj):
        self.players = setupPhaseObj.players
        self.active_bidders = { player: True for player in self.players }
        self.pass_count = 0             #   Track the number of passes
        self.highest_bid = 0
        self.trump_suit = None
        self.highest_numeric_bid = 0    #   Track the highest numeric level bid
        self.trump_bidder = None
        self.partnership = {}

    def start_bidding(self):
        """
        Executes the bidding process until three players have passed.
        """
        #   Loops until 3 players pass
        while self.pass_count < 3:
            for player in self.players:
                if self.active_bidders[player]:
                    if self.pass_count == 3 and self.trump_bidder:
                        # If only one active bidder remains, they automatically win
                        print(f"Bidding ended early. Winner: {self.trump_bidder.name} with {self.trump_suit} at {self.highest_numeric_bid} bids.")
                        return None
                    
                    self.collect_bid(player)

    def collect_bid(self, player):
        """
        Collects a bid from the specified player. A player can either make a bid higher than the current highest
        or pass. If the player passes, their active status is set to False.
        """
        available_bids = self.calculate_available_bids()

        bid = input(f"\n{player.name} (Player {player.order}) bidding - Available bids: {available_bids}\nEnter your bid: ")

        #   For now, assume that there are no illegal inputs

        bid = bid.title()
        if bid == 'Pass':
            self.active_bidders[player] = False
            self.pass_count += 1
        else:
            bid_number, bid_suit = bid.split(maxsplit=1)
            bid_number = int(bid_number)
            self.highest_numeric_bid = bid_number
            self.trump_suit = bid_suit
            self.highest_bid = self.calculate_bid_value(bid_number, bid_suit)
            self.trump_bidder = player

    def calculate_available_bids(self):
        """
        Calculates and returns the list of available bids based on the current highest bid.

        Full list would be ['Pass', '1 Clubs', '1 Diamonds', '1 Hearts', '1 Spades', '1 No Trump', '2 Clubs', ..., '7 Spades', '7 No Trump'].
        If a bid for e.g. '1 Hearts' was made, any bids lower than or equal in value to '1 Hearts' will no longer be available.
        """
        bids = ['Pass'] if self.pass_count < 3 else []

        current_level = max(self.highest_numeric_bid // 10, 1)

        #   Loops through numerical bid levels
        for i in range(current_level, 8):
            for suit in Deck.SUITS + ["No Trump"]:
                bid_value = self.calculate_bid_value(i, suit)
                if bid_value > self.highest_bid:
                    bids.append(f"{i} {suit}")

        return bids

    def calculate_bid_value(self, bid_number, bid_suit):
        """
        Calculates a unique numeric value for a bid based on the bid number and suit. This helps in comparing bids.

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
        Allows the bidding winner to select a partner based on a specific card from other players' hands.
        Displays all available cards from other players in a specific order (2-10, J, Q, K, A and Clubs, Diamonds, Hearts, Spades) and prompts the winner to choose one. Establishes partnerships based on the chosen card.
        """
        print(f"\n{bidding_player.name} won the bid with {self.trump_suit}. Select a partner card:")

        # Mapping ranks to values for sorting purposes
        rank_value = { str(num): num for num in range(2, 11) }
        rank_value.update({
            'Jack': 11,
            'Queen': 12,
            'King': 13,
            'Ace': 14
        })

        # Gathering and sorting cards from other players excluding the bidding player
        other_players_cards = [ card for player in self.players if player != bidding_player
                               for card in player.hand ]
        sorted_cards = sorted(other_players_cards, key=lambda card: (Deck.SUITS.index(card.suit), rank_value[card.rank]))

        # Display the sorted cards with enumeration
        for idx, card in enumerate(sorted_cards, 1):
            print(f"{idx}: {card}")

        # Input selection of the card index
        partner_card_index = int(input("Enter the number of the card to select as your partner's card: ")) - 1
        partner_card = sorted_cards[partner_card_index]

        # Display the chosen partner card
        print(f"You have selected {partner_card}. The owner of {partner_card} will be your partner!\n")

        # Find the owner of the partner card and establish partnership
        partner_player = None
        for player in self.players:
            if partner_card in player.hand:
                partner_player = player
                break

        team_1 = [bidding_player, partner_player]

        for player in team_1:
            player.sets_threshold = self.highest_numeric_bid + 6

        # Set the partnership for the other two players
        team_2 = [ player for player in self.players if player not in team_1 ]

        for player in team_2:
            player.sets_threshold = 8 - self.highest_numeric_bid

        self.partnership.update({
            bidding_player: partner_player,
            partner_player: bidding_player,
            team_2[0]: team_2[1],
            team_2[1]: team_2[0],
        })
