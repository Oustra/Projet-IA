# Isolation_game

An implementation of the game Isolation. 
Play a human vs. human game, play against an AI, or create your own AI strategy in `strategy.py`.

## Rules

- The game is played on a board of size `n x n`
- Each player starts with a single piece on the board
- At each turn, a player can move their piece to an adjacent square (horizontally, vertically, or diagonally). The square must be empty.
- After moving their piece, the player removes a square from the board. The square must be empty.
- The game ends when a player cannot move their piece anymore. The other player then wins.

## Run the program

```
$ python main.py -h

usage: main.py [-h] [--size SIZE] [--player1 {human,random,minimax}] [--player2 {human,random,minimax}] [--no-ui] 

Runs a game of Isolation.

options:
  -h, --help            show this help message and exit
  --size SIZE           Size of the board (Default: 7)
  --player1 {human,random,minimax}
                        Strategy for player1 (default: human)
  --player2 {human,random,minimax}
                        Strategy for player2 (default: random)
  --no-ui               GUI is not displayed. Use for running multiple games in a row between AIs.
```

## Implementing a new strategy

- 1: Extend the `Strategy` class
- 2: Implement the `choose_move()` method
- 3: Add the new strategy to the `STRATEGIES` dictionary at the end ot the `strategies.py` file
- 4: Run the game with the new strategy!

Tip: in order to debug your strategy, you should use a small board size! (4x4 for instance)