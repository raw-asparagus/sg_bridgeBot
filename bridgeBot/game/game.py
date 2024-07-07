from .core import Deck
from .setup import BaseGame

class RoundSet():
    """
    Represents each set result of each round.

    Attributes:
        owner (Player):         The player that won the set
        cards (list of Card):   The Cards in the set
    """
    def __init__(self, owner, cards):
        self.owner = owner
        self.cards = cards

class GamePhase(BaseGame):
    """
    Manages the gameplay phase of the Bridge game, handling the rounds, scoring, and determining the game winner based on the contract.
    
    Inherits from BaseGame and initializes using data from BiddingPhase.
    """
    def __init__(self, biddingPhaseObj):
        """
        Initializes the GamePhase with data from the bidding phase.

        Args:
            biddingPhaseObj (BiddingPhase): The BiddingPhase object containing relevant game state information.
        """
        # Initialize the base game state using the player list from BiddingPhase
        super().__init__([ player.name for player in biddingPhaseObj.players ])

        # Use existing players from BiddingPhase to ensure continuity of state such as hand and order
        self.players = biddingPhaseObj.players

        # Set up game properties from the bidding phase results
        self.trump_suit = biddingPhaseObj.trump_suit
        self.trump_bidder = biddingPhaseObj.trump_bidder
        self.partnership = biddingPhaseObj.partnership
        self.sets = []                  # List to store the outcome of each set
        self.set_winner = None     # To store the winner of the previous set

    def play_game(self):
        """
        Starts and manages the sequence of rounds. The first player is determined based on the presence of a trump suit.

        If there is a trump suit, the first player will be the player right in front of the trump bidder (clockwise).
        If there is no trump suit, the bid winner will be the first player.
        """
        if self.trump_suit in Deck.SUITS:   # If there is a trump suit
            starting_player_index = (self.players.index(self.trump_bidder) + 2) % len(self.players)  # Player right in front of the trump bidder
        else:  # If there is no trump suit
            starting_player_index = self.players.index(self.trump_bidder)  # The bid winner starts

        # Play sets until the game is over
        current_leader_index = starting_player_index

        while not self.is_game_over():
            self.play_round(current_leader_index)
            current_leader_index = self.players.index(self.set_winner)  # Update leader to the winner of the last set

        print(f'{self.set_winner.name} and {self.partnership[self.set_winner].name} has won!')

    def play_round(self, leader_index):
        """
        Conducts a round, with each player playing a card in turn starting from the leader.

        Args:
            leader_index (int): Index of the player who leads the set.
        """
        current_set = []
        for offset in range(len(self.players)):
            current_player = self.players[(leader_index + offset) % len(self.players)]
            card_played = self.prompt_player_for_card(current_player, current_set)
            current_set.append((current_player, card_played))
            print(f"{current_player.name} plays {card_played}")

        self.set_winner = self.resolve_set(current_set)
        self.sets.append(current_set)
        current_player.sets_won.append(current_set)
        print(f"\n{self.set_winner.name} wins the set with {[ f"{pair[0].name, pair[1]}" for pair in current_set ]}\n")
        #   Display card that won the set


    def prompt_player_for_card(self, player, current_set):
        """
        Prompts the player to choose a card to play based on the rules of following suit. If the player cannot follow suit,
        they may play a trump card, or any card if no trump or suit-matching cards are available.

        Args:
            player (Player):    The player who is to play a card.
            current_set (list): The current set being played, which determines the leading suit.

        Returns:
            Card: The card chosen by the player to play.
        """
        if current_set:
            leading_suit = current_set[0][1].suit
        else:
            leading_suit = None

        # Mapping ranks to values for sorting purposes
        rank_value = { str(num): num for num in range(2, 11) }
        rank_value.update({
            'Jack': 11,
            'Queen': 12,
            'King': 13,
            'Ace': 14
        })

        # Determine the available cards to play based on the leading suit
        suit_hand = [ card for card in player.hand if card.suit == leading_suit ] if leading_suit else player.hand

        hand = sorted(suit_hand if suit_hand else player.hand, key=lambda card: (Deck.SUITS.index(card.suit), rank_value[card.rank]))

        # Display the legal cards for player to choose from
        print(f"\n{player.name}'s turn to play. Legal cards to play:")
        for index, card in enumerate(hand, start=1):
            print(f"{index}: {card}")

        # Get player input for card selection
        card_index = int(input("Enter the number of the card you choose to play: ")) - 1
        chosen_card = hand[card_index]

        # Remove the chosen card from player's hand
        player.hand.remove(chosen_card)

        return chosen_card

    def resolve_set(self, current_set):
        """
        Determines the winner of a set based on the rules of Bridge including trump suit and the lead suit.

        Args:
            current_set (list): A list of tuples (Player, Card) representing the set played.

        Returns:
            Player: The player who wins the set.
        """
        highest_card = None
        set_winner = None

        #   Assess the highest card based on the trump and leading suits
        for player, card in current_set:
            if highest_card is None:
                #   Initialize the highest card and winner with the first card and player
                highest_card = card
                set_winner = player
            elif card.suit == self.trump_suit and (highest_card.suit != self.trump_suit or card.rank > highest_card.rank):
                #   A trump card beats any non-trump card or a lower trump card
                highest_card = card
                set_winner = player
            elif card.suit == highest_card.suit and card.rank > highest_card.rank and highest_card.suit != self.trump_suit:
                # A higher card in the leading suit, when no higher trump card has been played
                highest_card = card
                set_winner = player

        return set_winner

    def is_game_over(self):
        """
        Checks if the game is over, which occurs when one team achieves the contract or it becomes impossible for the other team to prevent this.

        Returns:
            bool: True if the game is over, otherwise False.
        """
        for player in self.players:
            print(f"{player.name}: {len(player.sets_won) + len(self.partnership[player].sets_won)}/{player.sets_threshold}", end="\t")
        
        print("\n\n" + "-" * 10 + "\n")

        for player in self.players:
            if len(player.sets_won) + len(self.partnership[player].sets_won) == player.sets_threshold:
                return True

        return all(len(player.hand) == 0 for player in self.players)
        #   Terminate when the threshold set has been reached