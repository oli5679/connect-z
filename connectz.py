import sys
from functools import lru_cache

"""
Generalisation of connect 4 to arbirary board size and win-length

Classes and functions:

    WinChecker:
        checks if a board contains a win for either player

    ConnectZGame:
        tracks the state of moves in a game

    parse_and_play:
        helper_method to specified filepath and plays out game

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
}


class InvalidSysArgsError(AssertionError):
    """
    Custom exception to catch cases where the script is run with no arguments or more than one argument rather than specified 1 argument
    """

    pass


def get_sys_filepath():
    """
    Gets filepath from command-line arguments

    returns:
        input_filepath (string) path to input file passed as command-line argument
    """
    num_inputs = len(sys.argv) - 1
    if num_inputs != 1:
        # raise custom error in order to meet specified contract print message
        raise InvalidSysArgsError
    else:
        input_filepath = sys.argv[1]
        return input_filepath


def parse_input(input_file_path):
    """
    Loads game-dimensions and moves from input file - game dimensions first row, all other rows are moves

    NOTE - invalid or non-existant files raise assertion errors with message specifying reason

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
        raise AssertionError("file error")

    try:
        file_lines = file_text.split("\n")
        game_dimensions = file_lines[0].split(" ")
        moves = file_lines[1:]
        return game_dimensions, moves
    except:
        raise AssertionError("invalid file")


def parse_game_dimensions(game_dimensions):
    """
    Loads game-dimensions from raw list

    NOTE - impossible dimensions raise assertion errors with message specifying reason

    Args:
        game_dimensions (list): list of raw inputs

    Returns:
        (
            rows (int): rows of board
            columns (int): columns of board
            win_length (int): minimum connected row required to win
        )
    """
    assert len(game_dimensions) == 3, "invalid file"
    rows = int(game_dimensions[0])
    columns = int(game_dimensions[1])
    win_length = int(game_dimensions[2])
    assert min([rows, columns, win_length]) > 0, "illegal game"
    assert win_length <= min([rows, columns]), "illegal game"
    return rows, columns, win_length


def parse_and_play(file_path, verbose=False):
    """
    Parses input-file and plays out game

    NOTE - impossible games raise assertion errors with message specifying reason

    Args:
        file_path (string): path to file
        verbose (boolean, default = False): should we print out debugging info

    Returns:
        game_status (string): if valid game, status at end of game
    """
    game_dimensions_raw, moves = parse_input(file_path)
    rows, columns, win_length = parse_game_dimensions(game_dimensions_raw)
    game = ConnectZGame(rows=rows, columns=columns, win_length=win_length)
    if verbose:
        print("moves")
        print(moves)
    for move in moves:
        live_status = game.make_move(int(move) - 1)
        if verbose:
            game.show_board()
        if verbose:
            print(move)
            print(live_status)

    return game.status


@lru_cache()
def build_masks(i, j, win_length):
    """
    Builds masks to check for wins in sub-board.

    These indexes will be checked if they are all 1/-1

    Args:
        i (int): starting index
        j (int): starting index
        win_length (int): length of sequence needed to win
    """
    right_mask = [[i, j + n] for n in range(win_length)]
    down_mask = [[i + n, j] for n in range(win_length)]
    diagonal_mask = [[i + n, j + n] for n in range(win_length)]
    inverse_diagonal_mask = [[i - n + win_length - 1, j + n] for n in range(win_length)]
    return [right_mask, down_mask, diagonal_mask, inverse_diagonal_mask]


class WinChecker:
    """
    Checks if a game-board is in the following states:
        'player 1 win'
        'player 2 win'
        'draw'
        'incomplete'

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

    def _square_contains_win(self, i, j, board):
        """
        Checking if a subsquare starting at point i,j in the board
        contains a win for either player

        Args:
            i (int): subboard starting index
            j (int): subboard starting index
            board (list): board to check
        """

        # the win directions (horizontal, vertical, both diagonals) can be represented by masks of their indexes
        masks = build_masks(i, j, self.win_length)
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
        # check all cells
        for i in range(self.columns):
            for j in range(self.rows):
                square_state = self._square_contains_win(i, j, board)
                # early return winners
                if square_state != "incomplete":
                    return square_state
        # if no winners, check if every cell in board is full
        flat_board = [val for sublist in board for val in sublist]
        if 0 in flat_board:
            return "incomplete"
        else:
            return "draw"


class ConnectZGame:
    """
    Class tracking Connect-Z Game

    Args:
        rows (int): number of rows in board
        columns (int): number of columns in board
        win_length (int): connected sequence needed to win
    """

    def __init__(self, rows, columns, win_length):
        self.rows = rows
        self.columns = columns
        self.win_length = win_length
        # start with empty board, incomplete status and player-1 move
        self.board = [[0 for x in range(rows)] for y in range(columns)]
        self.status = "incomplete"
        self.turn = 1
        # track how far along columns we have got
        self.column_counters = [rows - 1 for x in range(columns)]
        self.win_checker = WinChecker(rows=rows, columns=columns, win_length=win_length)

    def validate_move(self, selected_col):
        """
        Checks that move is legal

        Returns:
            True if move is legal, otherwise raises assertion-error
        """
        assert selected_col >= 0, "illegal column"
        assert selected_col < self.columns, "illegal column"
        assert self.column_counters[selected_col] > -1, "illegal row"
        assert (
            self.status != "player 1 win" and self.status != "player 2 win"
        ), "illegal continue"

    def make_move(self, selected_col):
        """
        Args:
            selected_col (int): column to place counter NOTE - zero indexed

        Returns:
            current_status (string): game status after updating board with this move
        """
        self.validate_move(selected_col)
        row_level = self.column_counters[selected_col]
        self.board[selected_col][row_level] = self.turn
        self.status = self.win_checker.check(self.board)
        self.column_counters[selected_col] -= 1
        self.turn *= -1
        return self.status

    def show_board(self):
        """
        Helper method to display board

        NOTE - transposes because I am using lists to represent columns, to make moving easier
        """
        transposed_board = map(list, zip(*self.board))
        for row in transposed_board:
            print(row)


def main():
    try:
        # play out game and return final game state's specified code
        input_file_path = get_sys_filepath()
        final_game_status = parse_and_play(input_file_path)
        print(GAME_CODES[final_game_status])
    except InvalidSysArgsError:
        # print if wrong number of sys args
        print("Provide one input file")
    except AssertionError as e:
        # return specified code if failing specific assertion error
        error_type = str(e)
        return print(GAME_CODES[error_type])


if __name__ == "__main__":
    main()
