import sys

"""
Generalisation of connect 4 to arbirary board-size and win-length

Classes and functions:

    StatusChecker:
        checks if a board contains a win for either player, drawn or incomplete

    Game:
        tracks the state of moves in a game

    parse_and_play:
        helper_method to load specified filepath and play out game

Command-line example

    python connectz PATH_TO_FILE
"""

# specified gamecodes to return - see readme.md for more details
GAME_CODES = {
    "draw": 0,
    "player 1 win": 1,
    "player 2 win": 2,
    "incomplete": 3,
    "illegal continue": 4,
    "illegal row": 5,
    "illegal column": 6,
    "illegal game": 7,
    "invalid file": 8,
    "file error": 9,
    "invalid sys args": "Provide one input file",
}


def get_sys_filepath():
    """
    Gets filepath from command-line arguments

    Returns:
        input_filepath (string) path to input file passed as command-line argument
    """
    assert len(sys.argv) == 2, "invalid sys args"
    return sys.argv[1]


def parse_input(input_file_path):
    """
    Loads game-dimensions and moves from input file - game dimensions first row, all other rows are moves

    Args:
        input_file_path (string): path to text file with game

    Returns:
        (
            game_dimensions (list): dimensions of game-board, and win length,
            moves (list): moves to be mode
        )
    """
    try:
        with open(input_file_path, "r") as input_file:
            file_text = input_file.read()
    except:
        # using assertion-errors so I can print right codes
        raise AssertionError("file error")
    try:
        file_lines = file_text.split("\n")
        game_dimensions = file_lines[0].split(" ")
        moves = file_lines[1:]
        return game_dimensions, moves
    except:
        # using assertion-errors so I can print right codes
        raise AssertionError("invalid file")


def parse_game_dimensions(game_dimensions_raw):
    """
    Loads game-dimensions from raw list

    Args:
        game_dimensions_raw (list): list of raw inputs

    Returns:
        game_dimensions (tuple): list of game dimensions converted to integers, and validated game is legal     
    """
    assert len(game_dimensions_raw) == 3, "invalid file"
    rows = int(game_dimensions_raw[0])
    columns = int(game_dimensions_raw[1])
    win_length = int(game_dimensions_raw[2])
    assert min([rows, columns, win_length]) > 0, "illegal game"
    assert win_length <= max([rows, columns]), "illegal game"
    return rows, columns, win_length


def parse_and_play(file_path, verbose=False):
    """
    Parses input-file and plays out game

    Args:
        file_path (string): path to file
        verbose (boolean, default = False): should we print out debugging info

    Returns:
        game_status (string): if valid game, status at end of game
    """
    game_dimensions_raw, moves = parse_input(file_path)
    rows, columns, win_length = parse_game_dimensions(game_dimensions_raw)
    game = Game(rows=rows, columns=columns, win_length=win_length)
    if verbose:
        print("moves")
        print(moves)
    for move in moves:
        live_status = game.make_move(int(move) - 1)
        if verbose:
            game.show_board()
            print(move)
            print(live_status)
    return game.status


class StatusChecker:
    """
    Checks if a game-board is won/drawn/incomplete

    Methods:
        check (board):
            find state of board
    """

    def __init__(self, rows, columns, win_length):
        """
        Args:
            rows (int): number of rows in board
            columns (int): number of columns in board
            win_length (int): connected sequence needed to win
        """
        self.rows = rows
        self.columns = columns
        self.win_length = win_length

    def _build_masks(self, i, j):
        """
        Builds masks to check for wins in sub-board (horizontal, vertical and both diagonals).

        These indexes will be checked if they are all 1/-1

        Args:
            i (int): starting column index
            j (int): starting row index
        """
        right_mask = [[i, j + n] for n in range(self.win_length)]
        down_mask = [[i + n, j] for n in range(self.win_length)]
        diagonal_mask = [[i + n, j + n] for n in range(self.win_length)]
        inverse_diagonal_mask = [
            [i - n + self.win_length - 1, j + n] for n in range(self.win_length)
        ]
        return [right_mask, down_mask, diagonal_mask, inverse_diagonal_mask]

    def _square_contains_win(self, i, j, board):
        """
        Checking if a subsquare starting at point i,j in the board
        contains a win for either player

        Args:
            i (int): subboard starting column index
            j (int): subboard starting row index
            board (list): board to check
        """
        masks = self._build_masks(i, j)
        for mask in masks:
            try:
                # if a mask sums to +- the win-length, this player has won
                total = sum((board[mx][my] for mx, my in mask))
                if total == self.win_length:
                    return "player 1 win"
                if total == -self.win_length:
                    return "player 2 win"
            except IndexError:
                # means we are off the board for this mask
                pass
        return "incomplete"

    def check(self, board):
        """
        Checks state of baord

        Args:
            board (list): list of lists, with empty = 0, player-1 = 1, player-2 = -1

        Returns:
            board_state (string): is board a win for either player, draw, or incomplete?
        """
        # find the columns with the most counters in.
        # The board above this can be discarded, since it contains only zeros.
        highest_non_zero = max((sum((abs(x) for x in c)) for c in board))
        filtered_board = [row[0:highest_non_zero] for row in board]
        # check all cells
        for i in range(self.columns):
            for j in range(highest_non_zero):
                square_state = self._square_contains_win(i, j, filtered_board)
                # early return winners
                if square_state != "incomplete":
                    return square_state
        # if no winners, check if every cell in board is full
        flat_board = [val for sublist in board for val in sublist]
        if 0 in flat_board:
            return "incomplete"
        else:
            return "draw"


class Game:
    """
    Class tracking state of Connect-Z Game

    Args:
        rows (int): number of rows in board
        columns (int): number of columns in board
        win_length (int): connected sequence needed to win

    Methods:
        make_move - update game state
        show_board - print out game board
    """

    def __init__(self, rows, columns, win_length):
        self.rows = rows
        self.columns = columns
        self.win_length = win_length
        # start with empty board, 'incomplete' status, player-1 to move and 0 counters in every col
        self.board = [[0 for x in range(rows)] for y in range(columns)]
        self.status = "incomplete"
        self.turn = 1
        self.column_counters = [0 for x in range(columns)]
        self.status_checker = StatusChecker(
            rows=rows, columns=columns, win_length=win_length
        )

    def _validate_move(self, selected_col):
        """
        Checks that move is legal

        Returns:
            True if move is legal, otherwise raises AssertionError
        """
        assert selected_col >= 0, "illegal column"
        assert selected_col < self.columns, "illegal column"
        assert self.column_counters[selected_col] < self.rows, "illegal row"
        assert not (self.status in ["player 1 win", "player 2 win"]), "illegal continue"
        return True

    def make_move(self, selected_col):
        """
        Makes a move, updating self.board

        Each column is represented by a list, filled up index zero onwards

        The player 1/2 to play is represented by turn = +1/-1

        Args:
            selected_col (int): column to place counter NOTE - zero indexed

        Returns:
            current_status (string): game status after updating board with this move
        """
        self._validate_move(selected_col)
        self.board[selected_col][self.column_counters[selected_col]] = self.turn
        self.status = self.status_checker.check(self.board)
        # next move in column one position higher
        self.column_counters[selected_col] += 1
        # next move other player (1/-1)
        self.turn *= -1
        return self.status

    def show_board(self):
        """
        Helper method to print out board
        """
        # flips and transposes because lists represent columns, to make moving easier
        # but want to show different orientation when printing
        flipped_board = [columm[::-1] for columm in self.board]
        transposed_board = map(list, zip(*flipped_board))
        for row in transposed_board:
            print(row)


def main():
    try:
        # play out game and return final game state's specified code
        input_file_path = get_sys_filepath()
        final_game_status = parse_and_play(input_file_path)
        print(GAME_CODES[final_game_status])
    except AssertionError as error_type:
        # return specified code if failing specific assertion error
        print(GAME_CODES[str(error_type)])


if __name__ == "__main__":
    main()
