"""
Config and fixtures for connect-z test cases
"""

TWO_SYS_ARGS = ["script.py", "first_arg", "second_arg"]

NO_SYS_ARGS = ["script.py"]

ONE_SYS_ARGS = ["script.py", "test_path"]

NO_MOVES_DIMS = ["3", "3", "1"]

VALID_COMPLETE_DIMS = ["7", "6", "4"]

VALID_COMPLETE_MOVES = ["1", "2", "1", "2", "1", "2", "1"]

TEN_BY_TWO_BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

LEGAL_GAMES = [
    ("test/games/valid_draw.txt", "draw"),
    ("test/games/valid_incomplete.txt", "incomplete"),
    ("test/games/valid_no_move.txt", "incomplete"),
    ("test/games/valid_win_player_1.txt", "player 1 win"),
    ("test/games/valid_win_player_2.txt", "player 2 win"),
]

ILLEGAL_GAMES = [
    ("test/games/illegal_column.txt", "illegal column"),
    ("test/games/illegal_continue.txt", "illegal continue"),
    ("test/games/illegal_row.txt", "illegal row"),
    ("test/games/illegal_game.txt", "illegal game"),
    ("test/games/invalid_file.txt", "invalid file"),
    ("banana", "file error"),
]

EXPECTED_LEGAL_MOVE_BOARD = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, -1, 1],
    [0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
