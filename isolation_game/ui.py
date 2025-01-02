# ui.py
import tkinter as tk

class GameUI:
    def __init__(self, root, size):
        self.root = root
        self.size = size
        self.buttons = [[None for _ in range(size)] for _ in range(size)]

    def create_ui_board(self, on_click):
        """
        Create the board with buttons.

        Args:
            on_click (function): The function to call when a button is clicked.
        """
        for i in range(self.size):
            for j in range(self.size):
                button = tk.Button(self.root, text="", width=4, height=2,
                                   command=lambda x=i, y=j: on_click(x, y))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def update_board(self, board):
        """
        Update the buttons to reflect the current board state.

        Args:
            board (2D list): The game board state.
        """
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 1:
                    self.buttons[i][j].config(text="P1", bg="blue", state="disabled")
                elif board[i][j] == 2:
                    self.buttons[i][j].config(text="P2", bg="red", state="disabled")
                elif board[i][j] == -1:
                    self.buttons[i][j].config(text="X", bg="black", state="disabled")
                else:
                    self.buttons[i][j].config(text="", bg="white", state="normal")


    def display_winner(self, winner):
        """
        Display the winner and end the game.

        Args:
            winner (int): The ID of the winning player.
        """
        result = tk.Label(self.root, text=f"Player {winner} wins!", font=("Arial", 16))
        result.grid(row=self.size, column=0, columnspan=self.size)
        # Disable all buttons
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(state="disabled")

