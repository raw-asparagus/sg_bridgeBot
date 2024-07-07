#   main.py

from game import SetupPhase, BiddingPhase, GamePhase

def main():
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    
    #   Initialize the Setup Phase and deal cards
    setup_game = SetupPhase(player_names)
    setup_game.shuffle_and_deal()

    #   Initialize the Bidding Phase using the setup phase results
    bidding_game = BiddingPhase(setup_game)
    bidding_game.start_bidding()

    #   Check if a valid bidding result was obtained
    if bidding_game.trump_bidder is None:
        print("Bidding did not result in a trump bidder, game cannot proceed.")
        return  #   Option to start another game?

    #   Select partner based on the bidding results
    bidding_game.select_partner(bidding_game.trump_bidder)

    #   Initialize the Game Phase using the bidding results
    game_phase = GamePhase(bidding_game)
    game_phase.play_game()

if __name__ == "__main__":
    main()
