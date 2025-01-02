import tkinter as tk
from game import Game

def evaluate_strategies_With_UI(strategy1, strategy2, size=4, num_games=1):
    strategy1_wins = 0
    strategy2_wins = 0

    # Create a root window for the UI
    root = tk.Tk()
    root.title("Isolation Game Evaluation")

    for i in range(num_games):
        # Use unique identifiers for strategies
        player1 = {"name": strategy1, "id": 1}
        player2 = {"name": strategy2, "id": 2}
        
        # Alternate starting player
        if i % 2 == 0:
            player1_type, player2_type = player1, player2
        else:
            player1_type, player2_type = player2, player1

        # Initialize the game with player objects
        game = Game(
            size=size,
            player1_type=player1_type["name"],
            player2_type=player2_type["name"],
            use_UI=True,
            UI_root=root
        )

        result = game.start_game()

        # Allow Tkinter to process events during the game
        root.update()

        # Determine the winner based on `result` and unique identifiers
        if result == 1:
            if player1_type["id"] == 1:
                strategy1_wins += 1
                print(f"Winner strategy 1: {strategy1}")
            else:
                strategy2_wins += 1
                print(f"Winner strategy 2: {strategy2}")
        elif result == 2:
            if player2_type["id"] == 1:
                strategy1_wins += 1
                print(f"Winner strategy 1: {strategy1}")
            else:
                strategy2_wins += 1
                print(f"Winner strategy 2: {strategy2}")

    # Print the results of the evaluation
    print(f"=> {strategy1} wins: {strategy1_wins}")
    print(f"=> {strategy2} wins: {strategy2_wins}")

    if strategy1_wins > strategy2_wins:
        print(f"-> {strategy1} is the superior strategy.")
    elif strategy2_wins > strategy1_wins:
        print(f"-> {strategy2} is the superior strategy.")
    else:
        print("-> Both strategies are equally effective.")

    # Start the Tkinter event loop
    root.mainloop()


def evaluate_strategies_Without_UI(strategy1, strategy2, size=4, num_games=1):
    strategy1_wins = 0
    strategy2_wins = 0

    for i in range(num_games):
        player1_type, player2_type = (strategy1, strategy2) if i % 2 == 0 else (strategy2, strategy1)

        game = Game(size=size, player1_type=player1_type, player2_type=player2_type, use_UI=False)

        game.start_game()

        result = game.current_player  # Assuming 1 for Player 1 win, 2 for Player 2 win

        if result == 1:
            if player1_type == strategy1:
                strategy1_wins += 1
                print(f"Winner strategy 1: {strategy1}")
            else:
                strategy2_wins += 1
                print(f"Winner strategy 2: {strategy2}")
        elif result == 2:
            if player2_type == strategy1:
                strategy1_wins += 1
                print(f"Winner strategy 1: {strategy1}")
            else:
                strategy2_wins += 1
                print(f"Winner strategy 2: {strategy2}")

    # Print the results of the evaluation
    print(f"=> {strategy1} wins: {strategy1_wins}")
    print(f"=> {strategy2} wins: {strategy2_wins}")

    if strategy1_wins > strategy2_wins:
        print(f"-> {strategy1} is the superior strategy.")
    elif strategy2_wins > strategy1_wins:
        print(f"-> {strategy2} is the superior strategy.")
    else:
        print("-> Both strategies are equally effective.")


# Example usage:
if __name__ == "__main__":
    evaluate_strategies_With_UI("minimax", "minimax", size=4, num_games=10)
