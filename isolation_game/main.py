import argparse
from game import Game
import tkinter as tk

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Play Isolation Game with configurable players and board size.")
    parser.add_argument("--size", type=int, default=4, help="Size of the board")
    parser.add_argument("--player1", choices=["human", "random", "minimax","mcts"], default="human",
                        help="Player 1 type: 'human', 'random' or 'minimax'")
    parser.add_argument("--player2", choices=["human", "random", "minimax","mcts"], default="minimax",
                        help="Player 2 type: 'human', 'random' or 'minimax'")
    parser.add_argument("--no_UI", action="store_false", help="Disable the UI")
    parser.add_argument("--random_start", action="store_true", help="Randomize the starting positions of the players")
    args = parser.parse_args()

    if args.no_UI == False:
        print("UI is disabled")
        # If no UI, we don't need to create a root window
        for i in range(100):
            game = Game(size=args.size, player1_type=args.player1, player2_type=args.player2, use_UI=args.no_UI,
                        UI_root=None, random_start=args.random_start)
            result = game.start_game()
            print(f"Game {i}: Player {result} wins!")

    else:
        # Create a root window for the UI
        root = tk.Tk()
        root.title("Isolation Game")
        game = Game(size=args.size, player1_type=args.player1, player2_type=args.player2, use_UI=args.no_UI, UI_root=root, random_start=args.random_start)
        result = game.start_game()
        root.mainloop()
        print(f"Player {result} wins!")