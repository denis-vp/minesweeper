from dataclasses import dataclass


@dataclass
class Cell:

    __row: int
    __column: int
    is_mine: bool = False
    mine_neighbors: int = 0

    is_revealed: bool = False
    is_flagged: bool = False

    @property
    def row(self) -> int:
        return self.__row

    @property
    def column(self) -> int:
        return self.__column
