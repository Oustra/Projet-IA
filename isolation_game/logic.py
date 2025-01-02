# logic.py
import copy

def is_legal_move(board, x, y):
    """
    Check if a move to position (x, y) is legal.

    Args:
        board (2D list): The game board state
        x (int): The x-coordinate of the move
        y (int): The y-coordinate of the move

    Returns:
        bool: True if the move is legal, False otherwise
    """
    if 0 <= x < len(board) and 0 <= y < len(board) and board[x][y] == 0:
        return True
    return False

def get_player_position(board, player_id):
    """
    Return the position of the player on the board.

    Args:
        board (2D list): The game board state
        player_id (int): The ID of the player

    Returns:
        tuple: (x, y) coordinates of the player
    """
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == player_id:
                return x, y
    return None

def get_legal_movements(board, player_id):
    """
    Return a list of legal movements for the current player.

    Args:
        board (2D list): The game board state
        player_id (int): The ID of the player
    """
    x, y = get_player_position(board, player_id)
    moves = []
    # Check all 8 possible moves (up, down, left, right, and diagonals)
    for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        new_x, new_y = x + dx, y + dy
        if is_legal_move(board, new_x, new_y):
            moves.append((new_x, new_y))
    return moves

def get_legal_full_moves(board, player_id):
    """
    Retourne une liste de tous les mouvements possibles pour le joueur (déplacement + blocage).

    Args:
        board (2D list): Le plateau de jeu.
        player_id (int): L'ID du joueur.

    Returns:
        list: Une liste de tuples, chacun contenant les coordonnées du déplacement et du blocage.
    """
    legal_full_moves = []
    old_x, old_y = get_player_position(board, player_id)

    # Obtenez tous les mouvements légaux
    for move in get_legal_movements(board, player_id):
        new_board = copy.deepcopy(board)
        new_board[move[0]][move[1]] = player_id
        new_board[old_x][old_y] = 0

        # Ajoutez les blocs possibles pour chaque déplacement
        for block in get_legal_blocks(new_board):
            legal_full_moves.append((*move, *block))  # Combine (move_x, move_y) et (block_x, block_y)

    return legal_full_moves


def get_legal_blocks(board):
    """
    Returns a list of all empty positions on the board where a block can be placed.

    Args:
        board (2D list): The game board state

    Returns:
        list: A list of (x, y) coordinates of empty positions on the board
    """
    legal_blocks = []
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 0:
                legal_blocks.append((x, y))
    return legal_blocks


def print_board(board):
    """
    Print the board state for debugging purposes.

    Args:
        board (2D list): The game board state
    """
    for row in board:
        print(" ".join(str(cell) if cell != 0 else '.' for cell in row))
