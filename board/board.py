from random import randint

from texttable import Texttable

from board.cell import Cell


class Board:

    def __init__(self, number_of_rows: int, number_of_columns: int, number_of_mines: int):
        self.__number_of_rows = number_of_rows
        self.__number_of_columns = number_of_columns
        self.__number_of_mines = number_of_mines

        self.__cells = {}

        self.__initialize_cells()
        self.__set_mines()

    def __initialize_cells(self):
        for row in range(self.__number_of_rows):
            for column in range(self.__number_of_columns):
                self.__cells[(row, column)] = Cell(row, column)

    def __set_mines(self):
        number_of_placed_mines = 0
        while number_of_placed_mines < self.__number_of_mines:
            random_row = randint(0, self.__number_of_rows - 1)
            random_column = randint(0, self.__number_of_columns - 1)

            cell = self.__cells[(random_row, random_column)]
            if not cell.is_mine:
                cell.is_mine = True
                number_of_placed_mines += 1
                self.__increment_mine_neighbors(cell)

    def __increment_mine_neighbors(self, cell: Cell):
        for row in range(cell.row - 1, cell.row + 2):
            for column in range(cell.column - 1, cell.column + 2):
                if (row, column) in self.__cells and not self.__cells[(row, column)].is_mine:
                    self.__cells[(row, column)].mine_neighbors += 1

    # ----------------------------------------- #

    @property
    def number_of_rows(self) -> int:
        return self.__number_of_rows

    @property
    def number_of_columns(self) -> int:
        return self.__number_of_columns

    @property
    def number_of_mines(self) -> int:
        return self.__number_of_mines

    @property
    def cells(self) -> list[Cell]:
        return list(self.__cells.values())

    @property
    def mines(self) -> list[Cell]:
        return [cell for cell in self.cells if cell.is_mine]

    # ----------------------------------------- #

    def get_neighbors(self, row: int, column: int) -> list[Cell]:
        neighbors = []
        for current_row in range(row - 1, row + 2):
            for current_column in range(column - 1, column + 2):
                if (current_row, current_column) in self.__cells:
                    neighbors.append(self.__cells[(current_row, current_column)])
        return neighbors

    def get_cell(self, row: int, column: int) -> Cell:
        return self.__cells[(row, column)]

    # ----------------------------------------- #

    def get_str(self, cheat) -> str:
        table = Texttable()

        table.header([" "] + [str(column) for column in range(1, self.__number_of_columns + 1)])

        for row in range(self.__number_of_rows):
            row_str = [str(row + 1)]
            for column in range(self.__number_of_columns):
                cell = self.__cells[(row, column)]
                if cell.is_revealed or cheat:
                    if cell.is_mine:
                        row_str.append("X")
                    else:
                        row_str.append(str(cell.mine_neighbors))
                elif cell.is_flagged:
                    row_str.append("F")
                else:
                    row_str.append(" ")

            table.add_row(row_str)

        return table.draw()
