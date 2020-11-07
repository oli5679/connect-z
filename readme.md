# Connect-Z

## Summary

Generalisation of connect-4 to arbitrary board-size and dimensions

See more details https://en.wikipedia.org/wiki/Connect_Four

This project allows checking of connect-z file, finding the status of the game following a sequency of moves.

## Getting started

All you need to run connectz.py script is Python (version 3.6+), as instructed it has no external dependencies.

I also include a jupyter-notebook used for profiling the code, and demoing running a utility function, but this is not needed for the core program to run.

## Input file example

The first line shows the dimensions of the game

- width of board
- height of board
- length needed to win

The lines after this are the column players moved. Player 1 and Player 2 alternate

    7 6 4
    1
    2
    1
    2
    1
    2
    1

## Command-line example

    python connectz PATH_TO_FILE

## Python example

    import connectz
    connectz.parse_and_play(PATH_TO_FILE)

## Run tests

To run the tests, a version of pytest needs to be installed.

This includes the test-cases in the reference documentation, as well as some I created whilst writing the program.

    pytest .

## Output codes

The command-line script returns output-codes to st-out. Here is a description of all codes.

0 - Draw

    This happens when every possible space in the frame was filled with
    a counter, but neither player achieved a line of the required length.

1 - Win for player 1

    The first player achieved a line of the required length.

2 - Win for player 2

    The second player achieved a line of the required length.

3 - Incomplete

    The file conforms to the format and contains only legal moves, but
    the game is neither won nor drawn by either player and there are
    remaining available moves in the frame. Note that a file with only a
    dimensions line constitues an incomplete game.

4 - Illegal continue

    All moves are valid in all other respects but the game has already
    been won on a previous turn so continued play is considered an
    illegal move.

5 - Illegal row

    The file conforms to the format and all moves are for legal columns
    but the move is for a column that is already full due to previous
    moves.

6 - Illegal column

    The file conforms to the format but contains a move for a column
that is out side the dimensions of the board. i.e. the column selected
is greater than X

7 Illegal game

    The file conforms to the format but the dimensions describe a game
that can never be won.

8 Invalid file

    The file is opened but does not conform the format.

9 File error

    The file can not be found, opened or read for some reason.

## Win-checking logic

I represent the board as a list of lists, with each list being a column, and player 1/2 moves being 1/-1, whilst empty is 0.

To check for wins I check all points in the board and create 'masks'
representing indexes of rows/columns/diagonals for a particular sub-board.

I check if any of these masks are entirely 1/-1, indicating player 1/2 has won.

## performance and profiling

On my computer, it takes c. 20s to make 6 moves on a large board (500x500)

Profiling the code, a majority of the time is spent on the '_square_contains_win' logic, checking if square contains a win for either player. See simple analysis in scratchpad.ipynb.

I already added some attempts to speed this up, returning early if a win is found, and caching the creation of the 'masks' since this will be the same every move.

If I was allowed to use numpy, I would consider:
    - using np.sum and np.trace to get totals of rows columns and diagonals
    - stripping out portions of the top/bottom/left right of board that contain only zeros
    - doing win-checks on subsections of the board, and using caching to avoid repeating analysis of identical subsections

There are probably also cleverer approaches than this to increase efficiency! If I had more time, I would consider this further.

## AI

If I had some time, I think you could build a reasonable AI to play these games using the following approach.

- 1 Heuristic

develop a heuristic evaluation function for a board. A decent one might be counting the lenghts of sequences and longer sequences are better. E.g.
Sequence of 2 = 1
Sequence of 3 = 5
Sequence of 4 = 25 for player 1

Oppenent sequence of 2 = -1
Oppenent sequence of 3 = -5
Oppenent sequence of 4 = -25 for player 1

- 2 tree-search

Search the game tree to a certian depth and then evaluate the board state at this depth. Then propegate values up the game-tree using the minimax algorthm. The AI can then select the move with the highest minimax value

https://en.wikipedia.org/wiki/Minimax

There are some further improvements that could be made to this, and also potentially reenforcement learning could be used to create an AI.
