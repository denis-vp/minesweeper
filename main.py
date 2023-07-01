"""

author: @denis916

"""


from configparser import RawConfigParser

from board.board import Board
from game import Game
from ui.console_ui import ConsoleUi
from ui.gui import Gui

SETTINGS_PATH = "settings.properties"


def get_properties(settings_path: str) -> tuple[int, int, int, type]:
    config = RawConfigParser()
    config.read(settings_path)

    number_of_rows = int(config.get("Board", "board.number_of_rows"))
    number_of_columns = int(config.get("Board", "board.number_of_columns"))
    number_of_mines = int(config.get("Board", "board.number_of_mines"))

    ui_types = {
        "console": ConsoleUi,
        "gui": Gui
    }
    ui_type = ui_types[config.get("Ui", "ui.type")]

    return number_of_rows, number_of_columns, number_of_mines, ui_type


if __name__ == "__main__":
    rows, columns, mines, ui = get_properties(SETTINGS_PATH)

    board = Board(rows, columns, mines)
    game = Game(board)
    ui = ui(game)

    ui.run_ui()
