# game.py
from ui import GameUI
from strategy import STRATEGIES
import time
from logic import *
import random

class Game:
    def __init__(self, size=7, player1_type="human", player2_type="random", use_UI = True, UI_root = None, random_start = True):
        """
        Initialization of a new game.

        Args:
            size (int): The size of the board (default 7x7)
            player1_type (str): The type of player 1: 'human', 'random' or 'minimax' (add other strategies if needed)
            player2_type (str): The type of player 2: 'human', 'random' or 'minimax' (add other strategies if needed)
            use_UI (bool): Whether to use the UI or not
            UI_root (tk.Tk): The root window for the UI
        """
        self.size = size  # The size of the board (default 7x7)
        self.board = [[0 for _ in range(size)] for _ in range(size)]  # 0 means empty


        self.current_player = 1
        self.has_moved = False  # Tracks if the current player has moved but not yet blocked


        # Initialization of the board with starting positions of the players
        if random_start:
        # TODO: Ensure fairness by checking the amount of available moves for each player
            # Initialization of the board with random positions of the players
            self.board[random.randint(0, size - 1)][random.randint(0, size - 1)] = 1
            # Ensuring that the second player is not placed in the same position as the first player
            while True:
                x = random.randint(0, size - 1)
                y = random.randint(0, size - 1)
                if self.board[x][y] == 0:
                    self.board[x][y] = 2
                    break
        else:
            self.board[0][0] = 1
            self.board[size - 1][size - 1] = 2


        # This variable stores the positions of the players on the board, in order to avoid to call logic.get_player_position too often
        self.players = {1: get_player_position(self.board, 1),
                        2: get_player_position(self.board, 2)}  # Player 1 starts at (0, 0), Player 2 at the opposite corner.

        # Initialize player strategies
        self.player1 = self.initialize_player(player1_type, player_id=1)
        self.player2 = self.initialize_player(player2_type, player_id=2)

        self.use_UI = use_UI
        if self.use_UI:
            self.UI = GameUI(UI_root, self.size)
            self.UI.create_ui_board(self.on_click)
            self.UI.update_board(self.board)
        else:
            self.UI = None

    def start_game(self):
        """
        Start the game and let AI Player 1 make the first move if not human.
        """
        winner = None

        # The game loop runs until a winner is determined
        while winner is None:
            # Update the UI if it's enabled
            if self.use_UI:
                self.UI.root.update_idletasks()
                self.UI.root.update()

            # Check if the current player is AI and execute their turn
            if (self.current_player == 1 and self.player1 is not None) or (
                    self.current_player == 2 and self.player2 is not None):
                print(f"Player {self.current_player}'s turn")
                self.execute_turn()
            else:
                # If it's a human's turn, rely on `on_click` to proceed
                pass

            # Check if the game is over (no legal moves for the opponent)
            if len(get_legal_movements(self.board, 3 - self.current_player)) == 0:
                winner = self.current_player
                if self.UI is not None:
                    self.UI.display_winner(self.current_player)
                    self.UI.root.update()
                    self.UI.update_board(self.board)
                    time.sleep(5)
                    self.UI.root.quit()
                    self.UI.root.destroy()
        return winner

    def on_click(self, x, y):
        """
        Handle a click event for the current player's move and blocking action.

        Args:
            x (int): The x-coordinate of the clicked cell
            y (int): The y-coordinate of the clicked cell
        """
        if (self.current_player == 1 and self.player1 is None) or (self.current_player == 2 and self.player2 is None):
            self.human_turn(x, y)

    def initialize_player(self, player_type, player_id):
        """
        Initialize the player strategy based on type.

        Args:
            player_type (str): The strategy of the player. The options should be keys in the STRATEGIES dictionary.
            player_id (int): The ID of the player (1 or 2)
        """
        if player_type in STRATEGIES:
            strategy_constructor = STRATEGIES[player_type]
            return strategy_constructor(self.board, player_id) if strategy_constructor else None
        else:
            raise ValueError(f"Invalid player type: {player_type}")


    def human_turn(self, x, y):
        """
        Execute a human turn with move and blocking action.

        Args:
            x (int): The x-coordinate of the clicked cell
            y (int): The y-coordinate of the clicked cell
        """
        if not self.has_moved:
            # First click: Move current player
            if self.move_player(self.current_player, x, y):
                if self.UI is not None:
                    self.UI.update_board(self.board)
        else:
            # Second click: Block a position
            if self.block_position(x, y):
                self.UI.update_board(self.board)
                if len(get_legal_movements(self.board, 3 - self.current_player)) == 0: # Check if no legal moves left for the other player
                    return self.current_player # End the game
                else:
                    # Switch to the next player and execute turn if AI
                    self.current_player = 3 - self.current_player
                    self.has_moved = False
                    self.execute_turn()

    def execute_turn(self):
        """
        Execute a turn based on the current player's type (AI or Human).
        """
        # Check if the current player is controlled by AI
        current_strategy = self.player1 if self.current_player == 1 else self.player2
        if current_strategy is not None:  # Current player is AI
            self.ai_turn(current_strategy)

    def ai_turn(self, strategy):
        """
        Execute AI turn for the given strategy.

        Args:
            strategy (Strategy): The strategy object for the current player
        """
        strategy.board = copy.deepcopy(self.board)  # Copy the current board state. This is important to avoid modifying the original board when exploring future moves.
        full_move = strategy.choose_move()
        position_move = (full_move[0], full_move[1])
        block = (full_move[2], full_move[3])

        if position_move:
            self.move_player(self.current_player, *position_move)
            if self.UI is not None:
                self.UI.update_board(self.board)

        if block:
            self.block_position(*block)
            if self.UI is not None:
                self.UI.update_board(self.board)

        # Check for game over at the end of AI's move
        if len(get_legal_movements(self.board, 3 - self.current_player)) == 0: # If no legal moves left
            return self.current_player # End the game
        else:
            # Switch to the next player and execute the next turn
            self.current_player = 3 - self.current_player
            self.has_moved = False
            self.execute_turn()


    def move_player(self, player, x, y):
        """
        Move the player to a new position and make the old one available.

        Args:
            player (int): The ID of the player to move
            x (int): The x-coordinate of the new position
            y (int): The y-coordinate of the new position

        Returns:
            bool: True if the move was successful, False otherwise
        """
        if (x, y) in get_legal_movements(self.board, player):
            # Get the player's current position
            old_x, old_y = self.players[player]

            # Move player to the new position
            self.players[player] = (x, y)
            self.board[x][y] = player

            # Free up the old position
            self.board[old_x][old_y] = 0

            # Indicate that the player has moved but still needs to block a position
            self.has_moved = True
            return True
        return False

    def block_position(self, x, y):
        """
        Block a specific position on the board.

        Args:
            x (int): The x-coordinate of the position to block
            y (int): The y-coordinate of the position to block
        """
        if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == 0:
            self.board[x][y] = -1  # Mark as blocked
            return True
        return False