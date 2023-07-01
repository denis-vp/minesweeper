from board.board import Board
from board.cell import Cell


class Game:

    def __init__(self, board: Board):
        self.__board = board

        self.__is_game_won = False
        self.__is_game_lost = False

        self.__reveal_one_safe_cell()

        self.__is_game_won = False
        self.__is_game_lost = False

    def __reveal_one_safe_cell(self):
        middle_row = self.__board.number_of_rows // 2
        middle_column = self.__board.number_of_columns // 2

        for row_offset in range(0, self.__board.number_of_rows - middle_row):
            for column_offset in range(0, self.__board.number_of_columns - middle_column):
                cell_1 = self.__board.get_cell(middle_row + row_offset, middle_column + column_offset)
                cell_2 = self.__board.get_cell(middle_row - row_offset, middle_column - column_offset)

                if not cell_1.is_mine and cell_1.mine_neighbors == 0:
                    self.reveal(cell_1.row, cell_1.column)
                    return
                elif not cell_2.is_mine and cell_2.mine_neighbors == 0:
                    self.reveal(cell_2.row, cell_2.column)
                    return

    @property
    def is_game_over(self) -> bool:
        return self.__is_game_lost or self.__is_game_won

    # ----------------------------------------- #

    @property
    def number_of_rows(self) -> int:
        return self.__board.number_of_rows

    @property
    def number_of_columns(self) -> int:
        return self.__board.number_of_columns

    @property
    def number_of_mines(self) -> int:
        return self.__board.number_of_mines

    @property
    def is_game_won(self) -> bool:
        return self.__is_game_won

    @property
    def is_game_lost(self) -> bool:
        return self.__is_game_lost

    @property
    def cells(self) -> list[Cell]:
        return self.__board.cells

    def get_board_str(self, cheat: bool) -> str:
        return self.__board.get_str(cheat)

    # ----------------------------------------- #

    def reveal(self, row: int, column: int):
        cell = self.__board.get_cell(row, column)

        if cell.is_revealed:
            raise GameError("Cell is already revealed!")
        elif cell.is_flagged:
            raise GameError("Cell is flagged!")
        cell.is_revealed = True

        if cell.mine_neighbors == 0 and not cell.is_mine:
            neighbors = self.__board.get_neighbors(row, column)
            for neighbor in neighbors:
                if not neighbor.is_mine and not neighbor.is_revealed and not neighbor.is_flagged:
                    if neighbor.mine_neighbors == 0:
                        self.reveal(neighbor.row, neighbor.column)
                    else:
                        neighbor.is_revealed = True

        if cell.is_mine:
            self.__is_game_lost = True
            self.__reveal_all_mines()
            return
        self.__check_game_win()

    def reveal_neighbors(self, row: int, column: int):
        cell = self.__board.get_cell(row, column)
        if not cell.is_revealed:
            raise GameError("Cell is not revealed!")

        neighbors = self.__board.get_neighbors(row, column)
        for neighbor in neighbors:
            try:
                self.reveal(neighbor.row, neighbor.column)
            except GameError:
                pass

    def __reveal_all_mines(self):
        for mine in self.__board.mines:
            mine.is_revealed = True

    def flag(self, row: int, column: int):
        cell = self.__board.get_cell(row, column)

        if cell.is_revealed:
            raise GameError("Cell is already revealed!")
        elif cell.is_flagged:
            raise GameError("Cell is already flagged!")
        cell.is_flagged = True

        self.__check_game_win()

    def unflag(self, row: int, column: int):
        cell = self.__board.get_cell(row, column)

        if cell.is_revealed:
            raise GameError("Cell is already revealed!")
        elif not cell.is_flagged:
            raise GameError("Cell is not flagged!")
        cell.is_flagged = False

    # ----------------------------------------- #

    def __check_game_win(self):
        for cell in self.__board.cells:
            if cell.is_mine and not cell.is_flagged:
                break
            if not cell.is_mine and cell.is_flagged:
                break
        else:
            self.__is_game_won = True
            return

        for cell in self.__board.cells:
            if not cell.is_revealed and not cell.is_mine:
                break
        else:
            self.__is_game_won = True


class GameError(Exception):
    pass
