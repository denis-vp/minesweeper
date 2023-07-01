from game import Game, GameError


class ConsoleUi:

    def __init__(self, game: Game):
        self.__game = game

    def run_ui(self):
        commands = {
            "help": ConsoleUi.__help,
            "exit": ConsoleUi.__exit,
            "cheat": self.__cheat,
            "reveal": self.__reveal,
            "flag": self.__flag,
            "unflag": self.__unflag,
            "dig": self.__reveal_neighbors
        }

        ConsoleUi.__print_title()

        self.__print_board()
        while not self.__game.is_game_over:
            command, arguments = ConsoleUi.__get_command()

            try:
                commands[command](*arguments)

            except KeyError:
                print("\nInvalid command!")
            except ValueError:
                print("\nInvalid arguments!")
            except GameError as error:
                print(f"\n{error}")

            except Exception as error:
                print(f"\n{error}")

        self.__game_over()

    # ----------------------------------------- #

    @staticmethod
    def __help():
        print("\nCommands:")
        print("help - prints this help")
        print("exit - exits the game")
        print("cheat - shows all mines")
        print("show row column - shows the cell at the given row and column")
        print("flag row column - flags the cell at the given row and column")
        print("unflag row column - unflags the cell at the given row and column")
        print("dig row column - reveals all the neighbors of the cell at the given row and column")

    @staticmethod
    def __exit():
        exit(1)

    def __cheat(self):
        self.__print_board(cheat=True)

    def __reveal(self, row: str, column: str):
        row, column = int(row) - 1, int(column) - 1
        self.__game.reveal(row, column)

        self.__print_board()

    def __flag(self, row: str, column: str):
        row, column = int(row) - 1, int(column) - 1
        self.__game.flag(row, column)

        self.__print_board()

    def __unflag(self, row: str, column: str):
        row, column = int(row) - 1, int(column) - 1
        self.__game.unflag(row, column)

        self.__print_board()

    def __reveal_neighbors(self, row: str, column: str):
        row, column = int(row) - 1, int(column) - 1
        self.__game.reveal_neighbors(row, column)

        self.__print_board()

    # ----------------------------------------- #

    def __game_over(self):
        if self.__game.is_game_won:
            print("\nYou won!")
        elif self.__game.is_game_lost:
            print("\nYou lost!")

    # ----------------------------------------- #

    @staticmethod
    def __get_command():
        command = input("\n>: ").strip()

        arguments = [argument.strip() for argument in command.split(" ") if argument.strip() != ""]
        if arguments[0] in ["help", "exit", "cheat"]:
            return arguments[0], []

        else:
            return arguments[0], arguments[1:]

    # ----------------------------------------- #

    @staticmethod
    def __print_title():
        print()
        print("# ----------------------------------------- #")
        print("# -------------- MINESWEEPER -------------- #")
        print("# ---------------- by Denis --------------- #")
        print("# ----------------------------------------- #")

    def __print_board(self, cheat: bool = False):
        print(f"\n{self.__game.get_board_str(cheat)}")
