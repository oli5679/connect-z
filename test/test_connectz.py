import pytest
import sys
from unittest.mock import patch

from connectZ import connectz
from . import fixtures

"""
Connect-z unit tests
"""


def test_get_input_filepath_two_arguments():
    """
    Error with two command line args
    """
    with pytest.raises(AssertionError, match="invalid sys args"):
        with patch.object(sys, "argv", fixtures.TWO_SYS_ARGS):
            connectz.get_sys_filepath()


def test_get_input_filepath_no_arguments():
    """
    Error with no command line args
    """
    with pytest.raises(AssertionError, match="invalid sys args"):
        with patch.object(sys, "argv", fixtures.NO_SYS_ARGS):
            connectz.get_sys_filepath()


def test_get_input_filepath_one_argument():
    """
    Returns the argument if 1 command line arg
    """

    with patch.object(sys, "argv", fixtures.ONE_SYS_ARGS):
        file_path = connectz.get_sys_filepath()
        assert file_path == "test_path"


def test_parse_input_filepath_no_moves_input():
    """
    Gets correct game-dimensions for a game with no moves
    """
    game_dimensions, moves = connectz.parse_input("test/games/valid_no_move.txt")
    assert game_dimensions == fixtures.NO_MOVES_DIMS
    assert moves == []


def test_parse_input_filepath_valid_complete_game():
    """
    Gets correct game-dimensions and moves for a sample game
    """
    game_dimensions, moves = connectz.parse_input("test/games/complete_game.txt")
    assert game_dimensions == fixtures.VALID_COMPLETE_DIMS
    assert moves == fixtures.VALID_COMPLETE_MOVES


def test_board_shape():
    """
    Builds correct board shape when initialized
    """
    game = connectz.ConnectZGame(rows=10, columns=2, win_length=3)
    assert game.board == fixtures.TEN_BY_TWO_BOARD


def test_illegal_game():
    """
    Correct error when game has too low 'win_length'
    """
    with pytest.raises(AssertionError, match="illegal game"):
        game = connectz.parse_game_dimensions(["7", "6", "0"])


def test_illegal_game_2():
    """
    Correct error when game has too high 'win_length'
    """
    with pytest.raises(AssertionError, match="illegal game"):
        game = connectz.parse_game_dimensions(["7", "6", "10"])


def test_illegal_column():
    """
    Correct error when move has invalid column number
    """
    game = connectz.ConnectZGame(7, 6, 4)
    with pytest.raises(AssertionError, match="illegal column"):
        game.make_move(-1)


def test_illegal_column_2():
    """
    Correct error when move has invalid column number (2)
    """
    game = connectz.ConnectZGame(7, 6, 4)
    with pytest.raises(AssertionError, match="illegal column"):
        game.make_move(8)


def test_illegal_row():
    """
    Correct error when row is overfilled
    """
    game = connectz.ConnectZGame(7, 6, 4)
    with pytest.raises(AssertionError, match="illegal row"):
        for _ in range(8):
            game.make_move(1)


def test_legal_moves():
    """
    Correct boardstate for sequence of moves
    """
    game = connectz.ConnectZGame(7, 6, 4)
    for move in [1, 1, 2]:
        game.make_move(move)
    assert game.board == fixtures.EXPECTED_LEGAL_MOVE_BOARD


def test_win_check_empty_board():
    """
    Empty board should be incomplete game-state
    """
    win_checker = connectz.WinChecker(5, 5, 3)
    test_board = [[0 for x in range(5)] for y in range(5)]
    assert win_checker.check(test_board) == "incomplete"


def test_win_check_single_move():
    """
    Single move should be incomplete game-state
    """
    win_checker = connectz.WinChecker(5, 5, 3)
    test_board = [[0 for x in range(5)] for y in range(5)]
    test_board[0][0] = 1
    assert win_checker.check(test_board) == "incomplete"


def test_win_check_vertical():
    """
    Check win_checker identifies vertical wins
    """
    win_checker = connectz.WinChecker(5, 6, 3)
    test_board = [[0 for x in range(5)] for y in range(6)]
    test_board[1][1] = 1
    test_board[1][2] = 1
    test_board[1][3] = 1
    assert win_checker.check(test_board) == "player 1 win"


def test_win_check_horizonal():
    """
    Check win_checker identifies horizontal wins
    """
    win_checker = connectz.WinChecker(5, 6, 3)
    test_board = [[0 for x in range(5)] for y in range(6)]
    test_board[2][1] = -1
    test_board[3][1] = -1
    test_board[4][1] = -1
    assert win_checker.check(test_board) == "player 2 win"


def test_win_check_vertical_2():
    """
    Check win_checker identifies vertical wins (2)
    """
    wc = connectz.WinChecker(5, 4, 3)
    t = [[0 for x in range(5)] for y in range(4)]
    t[1][1] = 1
    t[1][2] = 1
    t[1][3] = 1
    wc.check(t)
    assert wc.check(t) == "player 1 win"


def test_win_check_diagonal():
    """
    Check win_checker identifies diagonal wins
    """
    wc = connectz.WinChecker(9, 6, 2)
    t = [[0 for x in range(9)] for y in range(6)]
    t[1][1] = 1
    t[2][2] = 1
    wc.check(t)
    assert wc.check(t) == "player 1 win"


def test_win_check_diagonal_2():
    """
    Check win_checker identifies diagonal wins (2)
    """
    wc = connectz.WinChecker(10, 8, 4)
    t = [[0 for x in range(7)] for y in range(6)]
    t[4][3] = -1
    t[3][4] = -1
    t[2][5] = -1
    t[1][6] = -1
    wc.check(t)
    assert wc.check(t) == "player 2 win"


@pytest.mark.parametrize("test_input,expected", fixtures.LEGAL_GAMES)
def test_play_legal_games(test_input, expected):
    """
    Check correctly parses and plays out legal game examples in reference
    """
    final_game_status = connectz.parse_and_play(test_input)
    assert final_game_status == expected


@pytest.mark.parametrize("test_input,expected", fixtures.ILLEGAL_GAMES)
def test_play_illegal_games(test_input, expected):
    """
    Check correctly parses and plays out illegal game examples in reference
    """
    with pytest.raises(AssertionError, match=expected):
        final_game_status = connectz.parse_and_play(test_input)
