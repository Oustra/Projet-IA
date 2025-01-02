# strategy.py
import random
from logic import *
import time

# TODO: When you add a new strategy, add it to the dictionary at the end of this file

class Strategy:
    def __init__(self, board, player_id):
        """
        Initialize the strategy with a reference to the game instance and player ID.

        Args:
            board (2D list): The game board
            player_id (int): The ID of the player using this strategy (1 or 2).
        """
        self.board = board
        self.player_id = player_id

    def choose_move(self):
        """
        Choose a move and a blocking action based on the strategy.

        Returns:
            tuple: (x1, y1, x2, y2) coordinates of the chosen move (x1,y1) + block (x2, y2).
        """
        raise NotImplementedError("This method should be overridden in subclasses.")

class RandomStrategy(Strategy):
    def __init__(self, board, player_id):
        super().__init__(board, player_id)

    def choose_move(self):
        """
        Choose a random move and block from the legal moves.
        
        Returns:
            tuple: (x1, y1, x2, y2) coordinates of the chosen move (x1,y1) + block (x2, y2).
        """
        legal_full_moves = get_legal_full_moves(self.board, self.player_id)
        if legal_full_moves:
            random_move = random.choice(legal_full_moves)
            print(random_move)
            return random_move
        # TODO: Implement the Random strategy
        return

#gggg
class MinimaxStrategy(Strategy):
    def __init__(self, board, player_id, max_depth=3):
        super().__init__(board, player_id)
        self.max_depth = max_depth
        self.utility_cache = {}

    def hash_board(self, board, player_id):
        # Flatten the board into a tuple of tuples to make it hashable
        board_tuple = tuple(tuple(row) for row in board)
        return (board_tuple, player_id)

    def utility(self, board):
        # Generate a unique key for the current board state and player
        board_key = self.hash_board(board, self.player_id)

        # Check if the utility for this state is already cached
        if board_key in self.utility_cache:
            return self.utility_cache[board_key]

        # Compute utility if not cached
        my_moves = get_legal_movements(board, self.player_id)
        opp_moves = get_legal_movements(board, 3 - self.player_id)
        mobility = len(my_moves) - len(opp_moves)

        board_control = len(get_legal_blocks(board))

        my_pos = get_player_position(board, self.player_id)
        opp_pos = get_player_position(board, 3 - self.player_id)
        board_size = len(board)
        
        distance_to_opp = (abs(my_pos[0] - opp_pos[0]) + abs(my_pos[1] - opp_pos[1])) / (2 * board_size)
        closeness_factor = 1 / (distance_to_opp + 0.1)

        utility_value = (
            5 * mobility +      # High weight on mobility
            3 * board_control + # Control of available spaces
            2 * closeness_factor # Strategic positioning
        )

        # Cache the computed utility value
        self.utility_cache[board_key] = utility_value

        return utility_value

    def choose_move(self):
        start = time.time()
        _, best_move = self.minimax_search(self.board, self.max_depth, True, float('-inf'), float('inf'))
        end = time.time()
        print("time :",end-start)
        return best_move

    def is_over(self, board, depth):
        return (depth == 0 or len(get_legal_movements(board, self.player_id)) == 0)

    def minimax_search(self, board, depth, is_maximizing, alpha, beta):
        
        if self.is_over(board, depth):
            return self.utility(board), None
       
        legal_moves = get_legal_full_moves(board, self.player_id if is_maximizing else 3 - self.player_id)

        sorted_moves = sorted(legal_moves,key=lambda move: self.utility(self.applymove(board, self.player_id if is_maximizing else 3 - self.player_id, move)),
        reverse=is_maximizing)

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            for move in sorted_moves:
                new_board = self.applymove(board, self.player_id, move)
                eval, _ = self.minimax_search(new_board, depth - 1, False, alpha, beta)
                if eval > max_eval:
                    max_eval, best_move = eval, move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in sorted_moves:
                new_board = self.applymove(board, 3 - self.player_id, move)
                eval, _ = self.minimax_search(new_board, depth - 1, True, alpha, beta)
                if eval < min_eval:
                    min_eval, best_move = eval, move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
    

    def applymove(self, board, player_id, move):
        new_board = copy.deepcopy(board)
        x1, y1, x2, y2 = move
        old_x, old_y = get_player_position(new_board, player_id)
        new_board[old_x][old_y] = 0
        new_board[x1][y1] = player_id
        new_board[x2][y2] = -1
        return new_board
    

# Add new strategies to this dictionary
STRATEGIES = {
    "human": None,
    "random": RandomStrategy,
    "minimax": MinimaxStrategy
}
