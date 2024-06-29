#   Import classes from submodules to make them available at the package level
from .core import Card, Deck, Player, BaseGame, SetupPhase
from .bidding import BiddingPhase
from .game import GamePhase

#   Explicitly define classes available to import from the package
__all__ = [
    "Card",
    "Deck",
    "Player",
    "BaseGame",
    "BiddingPhase",
    "GamePhase"
]
